"""Minimal interactive annotation CLI for Paper 03 responses.

Reads a responses.csv table and writes one JSONL row per annotated response:
{"work_id": "...", "f_codes": ["F1", "F3"], "notes": "..."}
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

VALID_CODES = {"F1", "F2", "F3", "F4"}
EXPERIMENTS_DIR = Path(__file__).resolve().parents[1]
PAPER_DIR = EXPERIMENTS_DIR.parent
DEFAULT_RESPONSES = PAPER_DIR / "results" / "tables" / "responses.csv"
DEFAULT_ANNOTATIONS_DIR = PAPER_DIR / "annotations"


def load_done(path: Path) -> set[str]:
    """Load already annotated work_ids from an existing JSONL file."""
    done: set[str] = set()
    if not path.exists():
        return done
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("work_id"):
                done.add(str(obj["work_id"]))
    return done


def load_responses(path: Path) -> list[dict[str, Any]]:
    """Read responses.csv as dictionaries."""
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def response_body(row: dict[str, Any]) -> str:
    """Return the best available response text for display."""
    return row.get("response_text") or row.get("extracted_answer") or ""


def parse_codes(raw: str) -> list[str]:
    """Parse comma-separated F-codes, allowing blank for no code."""
    if not raw.strip():
        return []
    codes = [part.strip().upper() for part in raw.split(",") if part.strip()]
    invalid = [code for code in codes if code not in VALID_CODES]
    if invalid:
        raise ValueError(f"Invalid code(s): {', '.join(invalid)}. Use F1,F2,F3,F4 or blank.")
    return sorted(set(codes))


def prompt_for_annotation(row: dict[str, Any]) -> dict[str, Any] | None:
    """Interactively collect one annotation; return None when user quits."""
    print("\n" + "=" * 80)
    print(f"work_id: {row.get('work_id')}  cli_id: {row.get('cli_id')}  domain: {row.get('domain')}")
    print(f"prompt_id: {row.get('prompt_id')}  seed: {row.get('seed')}")
    print("-" * 80)
    print(response_body(row) or "[no response text available in CSV]")
    print("-" * 80)
    while True:
        raw = input("F-codes (comma-separated F1,F2,F3,F4; blank=none; q=quit): ").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            return None
        try:
            codes = parse_codes(raw)
            break
        except ValueError as exc:
            print(exc)
    notes = input("Notes (optional): ").strip()
    record: dict[str, Any] = {"work_id": row.get("work_id"), "f_codes": codes}
    if notes:
        record["notes"] = notes
    return record


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--responses", type=Path, default=DEFAULT_RESPONSES)
    ap.add_argument("--annotations-dir", type=Path, default=DEFAULT_ANNOTATIONS_DIR)
    ap.add_argument("--annotator", required=True)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--filter-domain", default="")
    ap.add_argument("--filter-cli", default="")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the interactive annotation loop."""
    args = parse_args(argv)
    if not args.responses.exists():
        print(f"responses.csv not found: {args.responses}", file=sys.stderr)
        return 2
    args.annotations_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.annotations_dir / f"{args.annotator}.jsonl"
    done = load_done(out_path) if args.resume else set()
    rows = load_responses(args.responses)
    if args.filter_domain:
        rows = [r for r in rows if r.get("domain") == args.filter_domain]
    if args.filter_cli:
        rows = [r for r in rows if r.get("cli_id") == args.filter_cli]
    if done:
        rows = [r for r in rows if str(r.get("work_id")) not in done]

    print(f"Annotator: {args.annotator}")
    print(f"Output   : {out_path}")
    print(f"Queue    : {len(rows)} responses")
    annotated = 0
    with out_path.open("a", encoding="utf-8") as fh:
        for row in rows:
            ann = prompt_for_annotation(row)
            if ann is None:
                break
            fh.write(json.dumps(ann, sort_keys=True) + "\n")
            fh.flush()
            annotated += 1
    print(f"Annotated {annotated} responses.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
