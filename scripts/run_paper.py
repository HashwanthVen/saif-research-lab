"""Orchestrator entry-point.

Usage:
    python scripts/run_paper.py 01                   # drive paper 01 through one phase
    python scripts/run_paper.py 01 --loop            # keep advancing until halt condition
    python scripts/run_paper.py --all --report       # print status for every paper
    python scripts/run_paper.py 02 --phase critic    # force-dispatch a specific role
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "papers"
AGENTS_DIR = REPO_ROOT / ".agents"


def list_paper_ids() -> list[str]:
    return sorted(
        p.name
        for p in PAPERS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith("_") and (p / "status.json").exists()
    )


def load_status(paper_id: str) -> dict:
    return json.loads((PAPERS_DIR / paper_id / "status.json").read_text(encoding="utf-8"))


def save_status(paper_id: str, status: dict) -> None:
    status["last_updated"] = datetime.now(timezone.utc).isoformat()
    (PAPERS_DIR / paper_id / "status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )


def load_role_prompt(role: str) -> str:
    f = AGENTS_DIR / f"{role}.md"
    if not f.exists():
        raise FileNotFoundError(f"No agent role file: {f}")
    return f.read_text(encoding="utf-8")


PHASE_TO_ROLE = {
    "literature_review": "researcher",
    "plan_critique": "critic",
    "senior_review_plan": "senior-reviewer",
    "experimentation": "experiment-runner",
    "results_critique": "critic",
    "drafting": "paper-writer",
    "mock_peer_review": "peer-reviewer",
    "rebuttal_loop": "rebuttal-author",
    "senior_review_final": "senior-reviewer",
}


def dispatch_hint(paper_id: str, status: dict) -> str:
    """Print a dispatch hint. The hosting coding-agent is expected to read this
    and actually invoke the LLM role with the prompt + paper context."""
    phase = status.get("phase", "literature_review")
    role = PHASE_TO_ROLE.get(phase)
    if role is None:
        return f"[halt] Paper {paper_id} is in terminal phase '{phase}'."
    prompt_path = AGENTS_DIR / f"{role}.md"
    return (
        f"[dispatch] paper={paper_id} phase={phase} role={role}\n"
        f"  prompt_file={prompt_path}\n"
        f"  paper_dir={PAPERS_DIR / paper_id}\n"
        f"  brief={(PAPERS_DIR / paper_id / 'PAPER_BRIEF.md')}\n"
        f"  status={(PAPERS_DIR / paper_id / 'status.json')}\n"
    )


def print_report() -> None:
    rows = []
    for pid in list_paper_ids():
        s = load_status(pid)
        rows.append(
            (
                pid,
                s.get("phase", "?"),
                s.get("target_venue", "?"),
                s.get("target_deadline", "?"),
                s.get("scores", {}).get("weighted_total", "?"),
                len(s.get("scoop_alerts", [])),
                len(s.get("blockers", [])),
            )
        )
    print(f"{'paper':40} {'phase':22} {'venue':14} {'deadline':14} {'score':6} {'scoops':6} {'blocks':6}")
    print("-" * 110)
    for r in rows:
        print(f"{r[0]:40} {r[1]:22} {r[2]:14} {str(r[3]):14} {str(r[4]):6} {str(r[5]):6} {str(r[6]):6}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paper_id", nargs="?", help="Paper id, e.g. 01 or 01-latent-cot-tabular")
    ap.add_argument("--all", action="store_true", help="Operate on all papers")
    ap.add_argument("--report", action="store_true", help="Print status table and exit")
    ap.add_argument("--phase", help="Force-dispatch a specific phase / role")
    ap.add_argument("--loop", action="store_true", help="Keep advancing (host must implement actual dispatch)")
    args = ap.parse_args()

    if args.report or (args.all and not args.paper_id):
        print_report()
        return 0

    paper_ids = list_paper_ids()
    if not paper_ids:
        print("No papers found under papers/.")
        return 1

    if args.paper_id:
        target = None
        for pid in paper_ids:
            if pid == args.paper_id or pid.startswith(f"{args.paper_id}-"):
                target = pid
                break
        if target is None:
            print(f"Unknown paper: {args.paper_id}. Available: {paper_ids}")
            return 2
        targets = [target]
    elif args.all:
        targets = paper_ids
    else:
        print("Specify a paper id or --all.")
        return 3

    for pid in targets:
        status = load_status(pid)
        if args.phase:
            status["phase"] = args.phase
            save_status(pid, status)
        print(dispatch_hint(pid, status))

    return 0


if __name__ == "__main__":
    sys.exit(main())
