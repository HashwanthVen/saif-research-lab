# Paper 03 — Cross-Domain Reasoning Model Failure Taxonomy

> **For the paper-agent**: Read `HANDOFF.md` first. It is the single source of truth.

## Quick navigation

| File | Purpose |
|---|---|
| [`HANDOFF.md`](./HANDOFF.md) | **Start here.** Comprehensive end-to-end orchestration guide. |
| [`PAPER_BRIEF.md`](./PAPER_BRIEF.md) | Canonical paper definition: hypotheses, plan, target venues, risks |
| [`plan.md`](./plan.md) | 6-week execution plan, phase-by-phase |
| [`status.json`](./status.json) | Machine-readable phase state |
| [`VENUE_STRATEGY.md`](./VENUE_STRATEGY.md) | arXiv-first + ICLR 2027 Evaluation + TMLR + Lancet companion |
| [`SYSTEM_RESOURCES.md`](./SYSTEM_RESOURCES.md) | What APIs / data / tools to use and how |
| [`experiments/`](./experiments/) | GHC CLI eval runner + aggregator + 10 seed prompts |

## One-liner for a fresh paper-agent session

```text
You are the orchestrator for papers/03-reasoning-failure-taxonomy in the
saif-research-lab repo (https://github.com/HashwanthVen/saif-research-lab).
Read in order: AGENTS.md, .github/copilot-instructions.md,
papers/03-reasoning-failure-taxonomy/HANDOFF.md, then the brief, plan, status,
venue-strategy, and system-resources. Drive this paper through its 6-week
lifecycle to an arXiv preprint and ICLR 2027 Evaluation track submission.
Halt and surface to me when status.json.phase reaches "ready_for_submission"
or any halt condition fires.
```

## Why this paper exists

8 frontier reasoning models × 5 high-stakes professional domains (medicine, law, nuclear engineering, finance, journalism) × 4 failure modes (hallucination, pattern rigidity, context compression, confidence miscalibration). No published cross-domain unification exists despite 3 independent 2025 studies showing domain-specific failures. We build the canonical taxonomy.

Score under demand-weighted rubric: **8.70 / 10** (highest in lab).
Compute cost: **$0** (GHC CLI seat-included).
Time to arXiv preprint: **6 weeks**.
Scoop window: **6-9 months** — move fast.
