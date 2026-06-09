# AGENTS.md — Top-Level Agent Contract

> This file is the canonical entrypoint for any coding agent (GitHub Copilot, Claude Code, Cursor, Codex, Devin, etc.) operating on this repository. Read this first, then `.github/copilot-instructions.md`, then the file in `.agents/` corresponding to your current role.

## Mission

Drive each paper in `papers/NN-*/` from idea to submission-ready manuscript with as little human intervention as possible, while respecting:

1. **Compute envelope** — every experiment must fit on a single NVIDIA RTX 4070 (12 GB VRAM). See `shared/compute-envelope.md`.
2. **Scientific integrity** — no p-hacking, no benchmark cheating, all claims supported by reproducible experiments.
3. **Venue acceptability** — target balanced-reputation venues (TMLR, COLM, ACL/EMNLP Findings, NeurIPS workshops, BMVC, WACV). See `shared/venue-calendar.md`.
4. **The rubric** — `shared/rubric.md` defines what "a good paper" means here. Re-score the paper periodically; if weighted score drops below 6.5, surface this to the human.

## Agent roles (read the per-role files in `.agents/` for full prompts)

| Role | File | When to invoke |
|------|------|----------------|
| Orchestrator | `.agents/orchestrator.md` | Top-level — you start here |
| Researcher | `.agents/researcher.md` | Literature review, gap analysis, related work, novelty check |
| Critic | `.agents/critic.md` | Hostile review of any artifact (plan, code, claim, paper draft) |
| Senior reviewer | `.agents/senior-reviewer.md` | Final sanity-check before expensive GPU runs and before submission |
| Experiment runner | `.agents/experiment-runner.md` | Writes PyTorch / HF code, runs training/eval, logs to results/ |
| Paper writer | `.agents/paper-writer.md` | LaTeX/markdown manuscript drafting and revision |
| Peer reviewer | `.agents/peer-reviewer.md` | Mock 3-reviewer panel simulating ACL/NeurIPS/TMLR reviewers |
| Rebuttal author | `.agents/rebuttal-author.md` | Drafts author response to reviewer comments |
| arXiv scout | `.agents/arxiv-scout.md` | Daily scan for newly published related work / scoop alerts |

## Lifecycle of a paper

```
ideate → literature review → critique loop → experimental plan → senior-review →
  → run experiments → analyze → critique loop → draft manuscript → mock peer review →
  → rebuttal/revision loop → final sanity check → human go-ahead → submission
```

State is persisted in `papers/<id>/status.json` so any agent can resume after a crash.

## Critical rules

1. **Never invent results.** If an experiment hasn't run, `results/` must not contain numbers for it.
2. **Always update `papers/<id>/status.json`** after every phase transition.
3. **Always log experimental artifacts** to `papers/<id>/results/runs/<timestamp>/` (code commit hash, config, raw logs, seed, GPU model).
4. **Run the critic on every major artifact** — plan, code, results, manuscript. Document the critic's findings under `papers/<id>/reviews/critic-<phase>-<date>.md`.
5. **Re-run the arXiv scout weekly.** If a paper appears that scoops > 60% of the contribution, halt and surface to human.
6. **Never push to `main` without a human-readable diff summary** in the commit message.
7. **Compute budget per paper**: max 168 GPU-hours / week. If hitting the wall, escalate to human, do not silently reduce experiment quality.
8. **For dual-use / safety topics**: read `shared/coding-standards.md` § Ethics before running.

## Status JSON schema

```json
{
  "paper_id": "01-latent-cot-tabular",
  "phase": "experimentation | drafting | mock_review | rebuttal | ready_for_submission | submitted",
  "last_updated": "2026-06-10T10:00:00Z",
  "current_score": 9.16,
  "target_venue": "TMLR",
  "target_deadline": "rolling",
  "next_actions": ["..."],
  "blockers": [],
  "scoop_alerts": []
}
```

## Multi-paper parallelism

Agents working on different `papers/NN-*` folders are independent. They share only:
- `shared/` (read-only)
- `.agents/` (read-only)
- the venue-calendar (read-only)

There is **no cross-paper data sharing**. If both papers want the same GPU at the same time, the orchestrator must serialise them by paper id (lower first).

## Halt conditions — surface to human immediately

- A scoop is detected (arXiv scout flags > 60% overlap).
- Critic returns "fundamentally flawed" twice in a row.
- A reviewer agent's score on the manuscript falls below 4/10.
- Compute budget exhausted with no publishable result.
- An ethics concern is raised by any agent.
