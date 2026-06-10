"""SMOKE-ONLY deterministic mock runner for Paper 03.

==============================================================================
WARNING — THIS SCRIPT IS NOT THE CANONICAL EVALUATION RUNNER.

All REAL model evaluation for Paper 03 MUST go through:

    papers/03-reasoning-failure-taxonomy/experiments/scripts/eval_runner.ps1

That PowerShell runner is the deterministic, idempotent, resumable harness
that talks to the GitHub Copilot CLI on the author's Windows host. It is the
single source of truth for the determinism contract (see HANDOFF.md § 3) and
the only path whose outputs may appear in `results/runs/` for the manuscript.

This Python module exists ONLY to:
  1. Provide a cross-platform smoke test of the work-id / build-plan / resume
     / record-schema logic on CI hosts that have neither PowerShell nor the
     `copilot` CLI installed (for example, the GitHub-hosted Linux runner).
  2. Mirror the PowerShell runner's JSON record schema so the aggregator
     (`aggregate_results.py`) can be unit-tested against synthetic input.

It deliberately CANNOT invoke any real CLI. There is no `subprocess` import
and no network access; every "response" is a deterministic SHA256-derived
placeholder. Records produced by this module are clearly tagged
(`script_version` starts with "mock_smoke.py", `response_text` starts with
"[MOCK]") so they can never be confused with real evaluation outputs.

If you are tempted to add a real-CLI path here: DON'T. Add it to the PS1
runner instead, and update HANDOFF.md § 3.
==============================================================================
"""
from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import platform
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCRIPT_VERSION = "mock_smoke.py v1.0.0 (SMOKE-ONLY; canonical = eval_runner.ps1)"

EXPERIMENTS_DIR = Path(__file__).resolve().parents[1]
PAPER_DIR = EXPERIMENTS_DIR.parent
DEFAULT_PROMPTS = EXPERIMENTS_DIR / "configs" / "prompts_sample.jsonl"
DEFAULT_MODELS = EXPERIMENTS_DIR / "configs" / "models.json"
# NOTE: the default output directory is intentionally a smoke-only subtree so
# that mock records cannot accidentally land in the real results corpus.
DEFAULT_OUT_DIR = PAPER_DIR / "results" / "smoke_runs"


def iso_utc() -> str:
    """Return an ISO-8601 UTC timestamp with millisecond precision."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def compute_work_id(prompt_id: str, cli_id: str, seed: int) -> str:
    """Compute first 16 hex chars of SHA256(prompt_id\\0cli_id\\0seed).

    Must stay bit-for-bit identical to the PowerShell runner's work_id formula
    so smoke artifacts and real artifacts share an addressing scheme.
    """
    key = f"{prompt_id}\0{cli_id}\0{seed}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load a JSONL file, ignoring blank lines."""
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def load_models(path: Path, models_filter: str = "") -> list[dict[str, Any]]:
    """Load included models, or all explicitly filtered models."""
    with path.open("r", encoding="utf-8") as fh:
        doc = json.load(fh)
    models = list(doc.get("models", []))
    if models_filter:
        wanted = {part.strip() for part in models_filter.split(",") if part.strip()}
        return [m for m in models if m.get("cli_id") in wanted]
    return [m for m in models if m.get("include") is True]


def apply_prompt_filter(prompts: list[dict[str, Any]], prompts_filter: str = "") -> list[dict[str, Any]]:
    """Apply optional comma-separated prompt_id filter."""
    if not prompts_filter:
        return prompts
    wanted = {part.strip() for part in prompts_filter.split(",") if part.strip()}
    return [p for p in prompts if p.get("prompt_id") in wanted]


def build_plan(
    prompts: Iterable[dict[str, Any]],
    models: Iterable[dict[str, Any]],
    num_seeds: int,
    out_dir: Path,
    resume: bool,
) -> tuple[list[dict[str, Any]], int]:
    """Build deterministic work plan and count resume skips."""
    plan: list[dict[str, Any]] = []
    skipped = 0
    for prompt in prompts:
        for model in models:
            for seed in range(num_seeds):
                prompt_id = str(prompt["prompt_id"])
                cli_id = str(model["cli_id"])
                work_id = compute_work_id(prompt_id, cli_id, seed)
                out_file = out_dir / f"{work_id}.json"
                if resume and out_file.exists():
                    skipped += 1
                    continue
                plan.append(
                    {
                        "work_id": work_id,
                        "prompt": prompt,
                        "model": model,
                        "seed": seed,
                        "out_file": out_file,
                    }
                )
    return plan, skipped


def mock_response(work_id: str, prompt: dict[str, Any], model: dict[str, Any], seed: int) -> str:
    """Return a clearly fake deterministic response for smoke tests.

    The leading "[MOCK]" tag and the "not a real model evaluation" footer are
    load-bearing: any downstream tool that ingests a record produced here can
    filter on them to refuse to treat the response as scientific evidence.
    """
    digest = hashlib.sha256(
        f"mock\0{work_id}\0{prompt.get('prompt_text', '')}\0{model.get('cli_id')}\0{seed}".encode("utf-8")
    ).hexdigest()[:24]
    keywords = prompt.get("ground_truth_keywords") or []
    answer = "; ".join(str(k) for k in keywords[:2]) if keywords else "synthetic placeholder"
    conf = (int(digest[:2], 16) % 101) / 100.0
    return (
        f"[MOCK] deterministic fake response hash={digest}\n"
        f"ANSWER: {answer}\n"
        f"CONFIDENCE: {conf:.2f}\n"
        "This smoke-test output is not a real model evaluation."
    )


def invoke_once(
    *,
    work_id: str,
    prompt: dict[str, Any],
    model: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    """Produce one deterministic mock record. Never touches a real CLI."""
    started = time.monotonic()
    stdout = mock_response(work_id, prompt, model, seed)
    return {
        "stdout": stdout,
        "stderr": "",
        "exit_code": 0,
        "timed_out": False,
        "duration_sec": round(time.monotonic() - started, 3),
    }


def build_record(
    item: dict[str, Any],
    result: dict[str, Any],
    started_at: str,
    finished_at: str,
) -> dict[str, Any]:
    """Build JSON record with the PowerShell schema plus python_version.

    The `cli_invocation` field is intentionally a synthetic marker rather than
    a real command line, so the record is self-describing as smoke output.
    """
    prompt = item["prompt"]
    model = item["model"]
    cli_id = str(model.get("cli_id", ""))
    return {
        "work_id": item["work_id"],
        "prompt_id": prompt.get("prompt_id"),
        "domain": prompt.get("domain"),
        "difficulty": prompt.get("difficulty"),
        "cli_id": cli_id,
        "display": model.get("display"),
        "tier": model.get("tier"),
        "thinking": model.get("thinking"),
        "seed": item["seed"],
        "prompt_text": prompt.get("prompt_text"),
        "response_text": result["stdout"],
        "stderr": result["stderr"],
        "exit_code": result["exit_code"],
        "timed_out": result["timed_out"],
        "duration_sec": result["duration_sec"],
        "started_at": started_at,
        "finished_at": finished_at,
        "cli_invocation": "MOCK (no CLI invoked; canonical runner is eval_runner.ps1)",
        "machine": socket.gethostname() or platform.node(),
        "user": getpass.getuser(),
        "python_version": platform.python_version(),
        "script_version": SCRIPT_VERSION,
    }


def write_json(path: Path, record: dict[str, Any]) -> None:
    """Write one JSON record."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def append_progress(log_file: Path, item: dict[str, Any], status: str) -> None:
    """Append one tab-separated progress line."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    prompt = item["prompt"]
    model = item["model"]
    line = "\t".join(
        [
            iso_utc(),
            str(item["work_id"]),
            str(prompt.get("prompt_id", "")),
            str(model.get("cli_id", "")),
            str(item["seed"]),
            status,
        ]
    )
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments. There is no real-CLI mode; all runs are mock."""
    ap = argparse.ArgumentParser(
        description=(
            "SMOKE-ONLY mock runner. Real evaluation MUST use "
            "experiments/scripts/eval_runner.ps1."
        ),
    )
    ap.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    ap.add_argument("--models", type=Path, default=DEFAULT_MODELS)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--num-seeds", type=int, default=3)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--models-filter", default="", help="Comma-separated cli_ids to run")
    ap.add_argument("--prompts-filter", default="", help="Comma-separated prompt_ids to run")
    ap.add_argument("--log-file", type=Path, default=None)
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the smoke harness. Always mock; never invokes a real CLI."""
    args = parse_args(argv)
    if args.num_seeds < 1:
        raise SystemExit("--num-seeds must be >= 1")
    if not args.prompts.exists():
        raise SystemExit(f"Prompts file not found: {args.prompts}")
    if not args.models.exists():
        raise SystemExit(f"Models file not found: {args.models}")

    prompts = apply_prompt_filter(load_jsonl(args.prompts), args.prompts_filter)
    models = load_models(args.models, args.models_filter)
    log_file = args.log_file or (args.out_dir / "_progress.tsv")
    plan, skipped = build_plan(prompts, models, args.num_seeds, args.out_dir, args.resume)
    total_work = len(prompts) * len(models) * args.num_seeds

    print("=== mock_smoke.py (SMOKE-ONLY; canonical runner is eval_runner.ps1) ===")
    print(f"Prompts     : {args.prompts} ({len(prompts)} prompts)")
    print(f"Models      : {args.models} ({len(models)} models)")
    print(f"OutputDir   : {args.out_dir}")
    print(f"NumSeeds    : {args.num_seeds}   TotalWork: {total_work}")
    print(f"Resume={args.resume}  DryRun={args.dry_run}  Mock=True (always)")
    print(f"Planned     : {len(plan)} runs ({skipped} skipped via resume)")

    if args.dry_run:
        for item in plan[:5]:
            print(
                "DRYRUN  {wid}  {pid:<26} {mid:<30} seed={seed}".format(
                    wid=item["work_id"],
                    pid=item["prompt"].get("prompt_id", ""),
                    mid=item["model"].get("cli_id", ""),
                    seed=item["seed"],
                )
            )
        if len(plan) > 5:
            print(f"  (... {len(plan) - 5} more)")
        print("DryRun complete.")
        return 0

    completed = 0
    for idx, item in enumerate(plan, start=1):
        prompt = item["prompt"]
        model = item["model"]
        print(
            f"[{idx}/{len(plan)}] {item['work_id']}  "
            f"{prompt.get('prompt_id', ''):<26} {model.get('cli_id', ''):<30} seed={item['seed']} ..."
        )
        started_at = iso_utc()
        result = invoke_once(
            work_id=str(item["work_id"]),
            prompt=prompt,
            model=model,
            seed=int(item["seed"]),
        )
        finished_at = iso_utc()
        record = build_record(item, result, started_at, finished_at)
        write_json(item["out_file"], record)
        append_progress(log_file, item, "ok")
        completed += 1
        print(f"  OK   exit=0 dur={result['duration_sec']}s out={len(result['stdout'])}b")

    print("\n=== Done (smoke) ===")
    print(f"Completed   : {completed}")
    print(f"Skipped     : {skipped} (resume)")
    print(f"Output dir  : {args.out_dir}")
    print(f"Progress log: {log_file}")
    print("REMINDER: these are MOCK records. Real evaluation = eval_runner.ps1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
