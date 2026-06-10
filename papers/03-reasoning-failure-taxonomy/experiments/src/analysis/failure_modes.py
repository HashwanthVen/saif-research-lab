"""Compute F-code distributions per (cli_id, domain) from annotations."""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

F_CODES = ["F1", "F2", "F3", "F4"]
PAPER_DIR = Path(__file__).resolve().parents[3]
DEFAULT_ANNOTATIONS = PAPER_DIR / "annotations"
DEFAULT_RESPONSES = PAPER_DIR / "results" / "tables" / "responses.csv"
DEFAULT_OUT = PAPER_DIR / "results" / "tables" / "failure_mode_distribution.csv"


def load_responses(path: Path) -> dict[str, dict[str, Any]]:
    """Load response rows keyed by work_id."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as fh:
        return {str(row.get("work_id")): row for row in csv.DictReader(fh) if row.get("work_id")}


def iter_annotations(path: Path):
    """Yield annotation objects from a JSONL file or directory of JSONLs."""
    if not path.exists():
        return
    files = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    for file_path in files:
        with file_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                yield json.loads(line)


def write_empty(out: Path) -> None:
    """Create an empty CSV with headers."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerow(["cli_id", "domain", "f_code", "count", "total_annotated", "fraction"])


def main() -> int:
    """CLI entry point."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--annotations-dir", type=Path, default=DEFAULT_ANNOTATIONS)
    ap.add_argument("--responses", type=Path, default=DEFAULT_RESPONSES)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    responses = load_responses(args.responses)
    if not responses:
        print(f"TODO: no responses found at {args.responses}; skipping failure-mode distribution.")
        write_empty(args.out)
        return 0

    totals: dict[tuple[str, str], int] = defaultdict(int)
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    matched = 0
    for ann in iter_annotations(args.annotations_dir) or []:
        work_id = str(ann.get("work_id", ""))
        row = responses.get(work_id)
        if not row:
            continue
        matched += 1
        cli = str(row.get("cli_id", ""))
        domain = str(row.get("domain", ""))
        totals[(cli, domain)] += 1
        for code in set(str(c).upper() for c in ann.get("f_codes", [])):
            if code in F_CODES:
                counts[(cli, domain, code)] += 1

    if matched == 0:
        print(f"TODO: no matching annotations in {args.annotations_dir}; wrote empty table.")
        write_empty(args.out)
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["cli_id", "domain", "f_code", "count", "total_annotated", "fraction"])
        for cli, domain in sorted(totals):
            total = totals[(cli, domain)]
            for code in F_CODES:
                count = counts.get((cli, domain, code), 0)
                w.writerow([cli, domain, code, count, total, round(count / total, 6) if total else ""])
    print(f"Wrote {args.out} ({matched} annotations matched).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
