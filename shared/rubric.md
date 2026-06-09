# Idea / Paper Scoring Rubric

Every paper in `papers/` is periodically re-scored against this rubric. If the weighted score drops below **6.5**, the orchestrator surfaces a re-evaluation prompt to the human.

## Metrics (weights sum to 1.0)

| Metric | Weight | Description | Scoring guide |
|--------|--------|-------------|---------------|
| novelty | 0.18 | How original / underexplored in 2025–2026 | 1 = trivial reproduction, 5 = incremental delta, 7 = genuinely new framing, 10 = field-shifting |
| compute_feasibility | 0.18 | Can it run end-to-end on RTX 4070 in ≤ 4 weeks wall time | 1 = impossible, 5 = compromised, 8 = comfortable, 10 = ideal |
| genuine_value | 0.16 | Does the result advance knowledge or just produce numbers | 1 = vanity, 5 = useful artifact, 8 = clear insight, 10 = community will build on it |
| venue_acceptability | 0.14 | Likelihood of acceptance at the target venue | 1 = rejected everywhere, 5 = workshop only, 7 = findings / TMLR realistic, 10 = main-conf realistic |
| solo_executability | 0.10 | Can ONE person execute it without lab / RA / co-authors | 1 = needs team, 5 = hard solo, 8 = clean solo, 10 = designed for solo |
| reproducibility | 0.08 | Open data, open weights, deterministic, cheap to verify | 1 = closed, 5 = partial, 10 = fully open + cheap |
| time_to_first_submission | 0.08 | Weeks from now to first submittable draft (lower = better) | 1 = >16 wk, 5 = 8–12 wk, 8 = 6–8 wk, 10 = ≤ 4 wk |
| risk_of_being_scooped | 0.04 | How likely a bigger lab publishes the same idea first (higher score = safer) | 1 = imminent scoop, 5 = moderate, 10 = niche |
| learning_value_for_author | 0.04 | Skill / career upside even if paper underperforms | 1 = none, 5 = moderate, 10 = large CV/skill boost |

## Computation

```
weighted_score = Σ (metric_score * weight)
```

Range: 1.0 to 10.0.

## Thresholds

- ≥ 8.0 → Top priority; pursue aggressively.
- 6.5 – 8.0 → Healthy; continue.
- 5.0 – 6.5 → Re-evaluate; consider pivot or venue downgrade.
- < 5.0 → Park.

## Re-scoring cadence

- Initial: at PAPER_BRIEF.md creation.
- Weekly: by the orchestrator after the weekly arXiv scout.
- Triggered: whenever the critic returns "major revision" or worse.
- Pre-submission: by the senior-reviewer at Checkpoint B.

## Where to record

In `papers/<id>/status.json` under:
```json
"scores": {
  "novelty": 9,
  "compute_feasibility": 10,
  ...
  "weighted_total": 9.16,
  "last_scored": "2026-06-09T15:00:00Z"
}
```
