"""Aggregate per-run JSON outputs from eval_runner.ps1 into a single CSV
suitable for analysis, plotting, and inclusion in the paper.

Usage:
    python aggregate_results.py --runs-dir ../../results/runs --out-dir ../../results/tables

Outputs:
    responses.csv          - one row per (prompt, model, seed) run
    by_model.csv           - one row per (model, domain) aggregate
    response_stability.csv - per (prompt, model) Jaccard agreement across seeds

Determinism: reads JSON files in --runs-dir in sorted order; output is a function
of the input directory only.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ANSWER_RE = re.compile(r"ANSWER\s*:\s*(.+?)(?:\n|$)", re.IGNORECASE | re.DOTALL)


def extract_answer(text: str) -> str:
    if not text:
        return ""
    m = ANSWER_RE.search(text)
    return (m.group(1) if m else text).strip()


def tokens(s: str) -> set[str]:
    return set(re.findall(r"\w+", s.lower())) if s else set()


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def keyword_hit_rate(answer: str, keywords: list[str]) -> float:
    if not keywords:
        return float("nan")
    ans_lower = answer.lower()
    hits = sum(1 for k in keywords if k.lower() in ans_lower)
    return hits / len(keywords)


def load_runs(runs_dir: Path) -> list[dict]:
    runs = []
    for f in sorted(runs_dir.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            runs.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"WARN: failed to load {f.name}: {e}")
    return runs


def write_responses_csv(runs: list[dict], out: Path) -> None:
    cols = [
        "work_id", "prompt_id", "domain", "difficulty", "cli_id", "display",
        "tier", "thinking", "seed", "exit_code", "timed_out", "duration_sec",
        "response_chars", "response_text", "extracted_answer", "started_at",
    ]
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in runs:
            ans = extract_answer(r.get("response_text", ""))
            w.writerow({
                "work_id": r.get("work_id"),
                "prompt_id": r.get("prompt_id"),
                "domain": r.get("domain"),
                "difficulty": r.get("difficulty"),
                "cli_id": r.get("cli_id"),
                "display": r.get("display"),
                "tier": r.get("tier"),
                "thinking": r.get("thinking"),
                "seed": r.get("seed"),
                "exit_code": r.get("exit_code"),
                "timed_out": r.get("timed_out"),
                "duration_sec": r.get("duration_sec"),
                "response_chars": len(r.get("response_text") or ""),
                "response_text": r.get("response_text") or "",
                "extracted_answer": ans,
                "started_at": r.get("started_at"),
            })
    print(f"Wrote {out} ({len(runs)} rows)")


def write_by_model_csv(runs: list[dict], prompts_jsonl: Path | None, out: Path) -> None:
    kw_lookup: dict[str, list[str]] = {}
    if prompts_jsonl and prompts_jsonl.exists():
        for line in prompts_jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            j = json.loads(line)
            kw_lookup[j["prompt_id"]] = j.get("ground_truth_keywords", []) or []

    agg: dict[tuple[str, str], dict] = defaultdict(lambda: {
        "n": 0, "ok": 0, "fail": 0, "total_dur": 0.0, "kw_hit_sum": 0.0, "kw_n": 0,
    })
    for r in runs:
        key = (r.get("cli_id"), r.get("domain"))
        a = agg[key]
        a["n"] += 1
        if r.get("exit_code") == 0 and not r.get("timed_out"):
            a["ok"] += 1
        else:
            a["fail"] += 1
        a["total_dur"] += float(r.get("duration_sec") or 0)
        kws = kw_lookup.get(r.get("prompt_id"), [])
        if kws:
            ans = extract_answer(r.get("response_text", ""))
            a["kw_hit_sum"] += keyword_hit_rate(ans, kws)
            a["kw_n"] += 1

    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["cli_id", "domain", "n_runs", "ok", "fail",
                    "avg_duration_sec", "avg_keyword_hit_rate"])
        for (cli, dom), a in sorted(agg.items()):
            avg_dur = a["total_dur"] / a["n"] if a["n"] else 0
            avg_kw = a["kw_hit_sum"] / a["kw_n"] if a["kw_n"] else float("nan")
            w.writerow([cli, dom, a["n"], a["ok"], a["fail"],
                        round(avg_dur, 3), round(avg_kw, 4) if avg_kw == avg_kw else ""])
    print(f"Wrote {out}")


def write_stability_csv(runs: list[dict], out: Path) -> None:
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in runs:
        if r.get("exit_code") != 0:
            continue
        ans = extract_answer(r.get("response_text", ""))
        grouped[(r.get("prompt_id"), r.get("cli_id"))].append(ans)

    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["prompt_id", "cli_id", "n_seeds", "mean_pairwise_jaccard"])
        for (pid, cli), answers in sorted(grouped.items()):
            if len(answers) < 2:
                w.writerow([pid, cli, len(answers), ""])
                continue
            toks = [tokens(a) for a in answers]
            sims = []
            for i in range(len(toks)):
                for j in range(i + 1, len(toks)):
                    sims.append(jaccard(toks[i], toks[j]))
            mean_j = sum(sims) / len(sims) if sims else 0
            w.writerow([pid, cli, len(answers), round(mean_j, 4)])
    print(f"Wrote {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--prompts", type=Path, default=None,
                    help="Optional path to prompts_sample.jsonl for keyword-hit metric")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    runs = load_runs(args.runs_dir)
    if not runs:
        print(f"No JSON runs found in {args.runs_dir}")
        return

    write_responses_csv(runs, args.out_dir / "responses.csv")
    write_by_model_csv(runs, args.prompts, args.out_dir / "by_model.csv")
    write_stability_csv(runs, args.out_dir / "response_stability.csv")
    print(f"\nDone. {len(runs)} runs aggregated.")


if __name__ == "__main__":
    main()
