"""Compute confidence calibration ECE per (cli_id, domain).

Confidence extraction contract: search response_text for a line matching
`CONFIDENCE: <x>` (case-insensitive). Values in [0, 1] are used directly;
values in (1, 100] are interpreted as percentages and divided by 100. If no
line is present or the value is outside range, confidence is NaN and skipped.
Correctness proxy: an annotated response with no F-codes is treated as correct;
any F-code means incorrect/failed. This script does not infer correctness from
model text.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

CONF_RE = re.compile(r"^\s*CONFIDENCE\s*:\s*([0-9]+(?:\.[0-9]+)?)\s*%?\s*$", re.IGNORECASE | re.MULTILINE)
PAPER_DIR = Path(__file__).resolve().parents[3]
DEFAULT_ANNOTATIONS = PAPER_DIR / "annotations"
DEFAULT_RESPONSES = PAPER_DIR / "results" / "tables" / "responses.csv"
DEFAULT_OUT = PAPER_DIR / "results" / "tables" / "confidence_calibration_ece.csv"


def extract_confidence(text: str) -> float:
    """Extract normalized confidence from response text, or NaN."""
    match = CONF_RE.search(text or "")
    if not match:
        return float("nan")
    value = float(match.group(1))
    if 0.0 <= value <= 1.0:
        return value
    if 1.0 < value <= 100.0:
        return value / 100.0
    return float("nan")


def load_responses(path: Path) -> dict[str, dict[str, Any]]:
    """Load response rows by work_id."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as fh:
        return {str(row.get("work_id")): row for row in csv.DictReader(fh) if row.get("work_id")}


def load_annotations(path: Path) -> dict[str, set[str]]:
    """Load all annotations from a JSONL file or directory."""
    anns: dict[str, set[str]] = {}
    if not path.exists():
        return anns
    files = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    for file_path in files:
        with file_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                obj = json.loads(line)
                wid = obj.get("work_id")
                if wid:
                    anns[str(wid)] = {str(c).upper() for c in obj.get("f_codes", [])}
    return anns


def bin_index(conf: float, bins: int) -> int:
    """Return ECE bin index in [0, bins-1]."""
    return min(bins - 1, max(0, int(conf * bins)))


def write_empty(out: Path) -> None:
    """Write an empty ECE CSV with headers."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerow(["cli_id", "domain", "n", "n_with_confidence", "ece", "bins"])


def main() -> int:
    """CLI entry point."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--annotations-dir", type=Path, default=DEFAULT_ANNOTATIONS)
    ap.add_argument("--responses", type=Path, default=DEFAULT_RESPONSES)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--bins", type=int, default=10)
    args = ap.parse_args()

    responses = load_responses(args.responses)
    annotations = load_annotations(args.annotations_dir)
    if not responses or not annotations:
        print("TODO: responses or annotations are empty; skipping calibration ECE.")
        write_empty(args.out)
        return 0

    grouped: dict[tuple[str, str], list[tuple[float, float]]] = defaultdict(list)
    total_seen: dict[tuple[str, str], int] = defaultdict(int)
    for wid, codes in annotations.items():
        row = responses.get(wid)
        if not row:
            continue
        key = (str(row.get("cli_id", "")), str(row.get("domain", "")))
        total_seen[key] += 1
        text = row.get("response_text") or row.get("extracted_answer") or ""
        conf = extract_confidence(text)
        if math.isnan(conf):
            continue
        correct = 1.0 if not codes else 0.0
        grouped[key].append((conf, correct))

    if not total_seen:
        print("TODO: no annotations matched responses; wrote empty calibration table.")
        write_empty(args.out)
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    bins_out = args.out.with_name("confidence_calibration_bins.csv")
    with args.out.open("w", encoding="utf-8", newline="") as ece_fh, bins_out.open("w", encoding="utf-8", newline="") as bin_fh:
        ece_w = csv.writer(ece_fh)
        bin_w = csv.writer(bin_fh)
        ece_w.writerow(["cli_id", "domain", "n", "n_with_confidence", "ece", "bins"])
        bin_w.writerow(["cli_id", "domain", "bin", "bin_low", "bin_high", "n", "accuracy", "mean_confidence"])
        for key in sorted(total_seen):
            pairs = grouped.get(key, [])
            cli, domain = key
            if not pairs:
                ece_w.writerow([cli, domain, total_seen[key], 0, "", args.bins])
                continue
            buckets: dict[int, list[tuple[float, float]]] = defaultdict(list)
            for conf, correct in pairs:
                buckets[bin_index(conf, args.bins)].append((conf, correct))
            ece = 0.0
            for idx in range(args.bins):
                vals = buckets.get(idx, [])
                if not vals:
                    continue
                acc = sum(v[1] for v in vals) / len(vals)
                avg_conf = sum(v[0] for v in vals) / len(vals)
                weight = len(vals) / len(pairs)
                ece += weight * abs(acc - avg_conf)
                bin_w.writerow([cli, domain, idx, round(idx / args.bins, 3), round((idx + 1) / args.bins, 3), len(vals), round(acc, 6), round(avg_conf, 6)])
            ece_w.writerow([cli, domain, total_seen[key], len(pairs), round(ece, 6), args.bins])
    print(f"Wrote {args.out} and {bins_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
