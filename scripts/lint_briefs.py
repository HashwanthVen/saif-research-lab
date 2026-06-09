"""Smoke-lint paper briefs: every PAPER_BRIEF.md must contain the required sections."""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## One-line summary",
    "## Hypotheses",
    "## Experimental plan",
    "## Target venue",
    "## Compute envelope",
    "## Keywords",
    "## Related arXiv IDs",
    "## Ethics",
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    for brief in (root / "papers").glob("*/PAPER_BRIEF.md"):
        text = brief.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{brief}: missing section '{section}'")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: linted {len(list((root / 'papers').glob('*/PAPER_BRIEF.md')))} paper briefs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
