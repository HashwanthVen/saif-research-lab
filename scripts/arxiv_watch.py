"""Nightly arXiv scout (CI entrypoint).

Reads every papers/*/PAPER_BRIEF.md, extracts keywords, queries arXiv for new
submissions since the last run, scores each candidate, and writes a digest to
papers/<id>/literature/arxiv-scout-<YYYYMMDD>.md.

This is a thin scaffold; the full implementation is delegated to the arXiv
scout agent at runtime. CI uses this stub for dry-run sanity checks.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import arxiv  # type: ignore
except ImportError:
    arxiv = None  # type: ignore


def extract_keywords(brief_text: str) -> list[str]:
    m = re.search(r"## Keywords\s*\n(.+?)(?:\n##|\Z)", brief_text, re.S)
    if not m:
        return []
    return [k.strip() for k in re.split(r"[,\n]", m.group(1)) if k.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="24h")
    ap.add_argument("--emit-issues", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    briefs = list((root / "papers").glob("*/PAPER_BRIEF.md"))
    if not briefs:
        print("No briefs found; nothing to scout.")
        return 0

    if arxiv is None:
        print("[stub] arxiv package not installed; CI dry-run only.")
        return 0

    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    for brief in briefs:
        keywords = extract_keywords(brief.read_text(encoding="utf-8"))
        if not keywords:
            continue
        query = " OR ".join(f'"{k}"' for k in keywords[:5])
        search = arxiv.Search(query=query, max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate)
        digest_path = brief.parent / "literature" / f"arxiv-scout-{today}.md"
        digest_path.parent.mkdir(parents=True, exist_ok=True)
        with digest_path.open("w", encoding="utf-8") as fh:
            fh.write(f"# arXiv scout digest — {today}\n\nKeywords: {keywords}\n\n")
            for r in search.results():
                fh.write(f"## {r.title}\n- {r.entry_id}\n- Submitted: {r.published}\n- {r.summary[:400]}...\n\n")
        print(f"Wrote {digest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
