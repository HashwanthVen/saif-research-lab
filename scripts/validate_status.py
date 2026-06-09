"""Validate every papers/*/status.json against the expected schema."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_KEYS = {
    "paper_id",
    "phase",
    "last_updated",
    "target_venue",
    "target_deadline",
    "next_actions",
    "blockers",
    "scoop_alerts",
    "scores",
}

VALID_PHASES = {
    "literature_review",
    "plan_critique",
    "senior_review_plan",
    "experimentation",
    "results_critique",
    "drafting",
    "mock_peer_review",
    "rebuttal_loop",
    "senior_review_final",
    "ready_for_submission",
    "submitted",
    "parked",
}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    for status_path in (root / "papers").glob("*/status.json"):
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{status_path}: invalid JSON ({e})")
            continue
        missing = REQUIRED_KEYS - set(data.keys())
        if missing:
            errors.append(f"{status_path}: missing keys {missing}")
        if data.get("phase") not in VALID_PHASES:
            errors.append(f"{status_path}: invalid phase '{data.get('phase')}'")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: validated {len(list((root / 'papers').glob('*/status.json')))} status files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
