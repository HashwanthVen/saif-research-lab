"""Compute per-F-code and overall Cohen's kappa for two annotator JSONL files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

F_CODES = ["F1", "F2", "F3", "F4"]
PAPER_DIR = Path(__file__).resolve().parents[3]
DEFAULT_OUT = PAPER_DIR / "results" / "tables" / "inter_annotator_kappa.md"


def load_annotations(path: Path) -> dict[str, set[str]]:
    """Load annotation JSONL as work_id -> set(F-codes)."""
    annotations: dict[str, set[str]] = {}
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            if not line.strip():
                continue
            obj = json.loads(line)
            work_id = obj.get("work_id")
            if not work_id:
                raise ValueError(f"Missing work_id at {path}:{line_no}")
            annotations[str(work_id)] = {str(c).upper() for c in obj.get("f_codes", [])}
    return annotations


def kappa(pairs: Iterable[tuple[bool, bool]]) -> tuple[float, int, float, float]:
    """Compute Cohen's kappa from binary label pairs.

    Returns (kappa, n, observed_agreement, expected_agreement).
    """
    data = list(pairs)
    n = len(data)
    if n == 0:
        return float("nan"), 0, float("nan"), float("nan")
    agree = sum(1 for a, b in data if a == b) / n
    p_a_yes = sum(1 for a, _ in data if a) / n
    p_a_no = 1.0 - p_a_yes
    p_b_yes = sum(1 for _, b in data if b) / n
    p_b_no = 1.0 - p_b_yes
    expected = p_a_yes * p_b_yes + p_a_no * p_b_no
    if expected == 1.0:
        return (1.0 if agree == 1.0 else float("nan")), n, agree, expected
    return (agree - expected) / (1.0 - expected), n, agree, expected


def fmt(x: float) -> str:
    """Format report float values."""
    return "NA" if x != x else f"{x:.3f}"


def build_report(a_path: Path, b_path: Path, a: dict[str, set[str]], b: dict[str, set[str]]) -> str:
    """Build markdown kappa report."""
    common = sorted(set(a) & set(b))
    lines = [
        "# Inter-annotator Cohen's kappa",
        "",
        f"Annotator A: `{a_path}`",
        f"Annotator B: `{b_path}`",
        f"Overlapping responses: {len(common)}",
        "",
        "| Label | n | observed agreement | expected agreement | kappa |",
        "|---|---:|---:|---:|---:|",
    ]
    all_pairs: list[tuple[bool, bool]] = []
    for code in F_CODES:
        pairs = [(code in a[wid], code in b[wid]) for wid in common]
        all_pairs.extend(pairs)
        kap, n, obs, exp = kappa(pairs)
        lines.append(f"| {code} | {n} | {fmt(obs)} | {fmt(exp)} | {fmt(kap)} |")
    kap, n, obs, exp = kappa(all_pairs)
    lines.extend([
        f"| overall micro-binary | {n} | {fmt(obs)} | {fmt(exp)} | {fmt(kap)} |",
        "",
        "Overall treats every (response, F-code) decision as a binary label.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("annotator_a", type=Path)
    ap.add_argument("annotator_b", type=Path)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--write", action="store_true", help="Write markdown report to --out")
    ap.add_argument("--print", dest="print_report", action="store_true", default=True, help="Print report to stdout (default)")
    return ap.parse_args()


def main() -> int:
    """Entry point."""
    args = parse_args()
    a = load_annotations(args.annotator_a)
    b = load_annotations(args.annotator_b)
    report = build_report(args.annotator_a, args.annotator_b, a, b)
    if args.print_report:
        print(report, end="")
    if args.write:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
