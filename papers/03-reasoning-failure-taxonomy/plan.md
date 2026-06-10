# Paper 03 — Experimental Plan

## Critical urgency note
**This paper has the HIGHEST scoop risk in the lab.** 6-9 month window before competing lab teams publish. Target arXiv preprint within 6 weeks of starting.

## Phase 1: Benchmark curation (week 1)

- [ ] Pull M-ARC (contact Kim et al. or use replication subset)
- [ ] Pull CUAD (public)
- [ ] Pull ClaimBuster (public)
- [ ] Curate **FSAR-Argue** from public NRC ADAMS FSAR excerpts (target: 200 argument-completeness items)
- [ ] Curate **EDGAR-Q** from SEC 10-K/10-Q risk-factor sections post-2024-cutoff (target: 200 items)
- [ ] Annotator-agreement pilot: 20 items × 2 annotators on each benchmark → require κ ≥ 0.7

## Phase 2: Model evaluation (week 2)

- [ ] Wire up API clients for o3-mini, DeepSeek-R1, Claude 3.7 Thinking, Gemini 2.5 Pro Thinking, o1
- [ ] Run 200 prompts × 5 models × 5 domains = 5,000 responses
- [ ] Capture: prompt, reasoning trace, final answer, self-reported confidence (1-5 or 0-1)
- [ ] Token + cost accounting; abort if any model > $400 budget
- [ ] Save all responses to `results/runs/<UTC>_<sha>/responses.jsonl`

## Phase 3: Failure annotation (weeks 3-4)

- [ ] Develop F-code rubric: F1 hallucination, F2 rigidity, F3 compression, F4 miscalibration
- [ ] 2 annotators code 1000 responses each (subset overlap for κ)
- [ ] Resolve disagreements via consensus pass
- [ ] Calibrate confidence buckets for ECE calculation

## Phase 4: Analysis (week 5)

- [ ] Compute per-model per-domain accuracy
- [ ] Compute per-model per-domain failure-mode distribution (F1-F4 fractions)
- [ ] Compute ECE per model per domain
- [ ] CoT trace inspection: find lexical / structural features predictive of each F-code
- [ ] Generate all 4 figures + 3 tables

## Phase 5: Manuscript + critique (week 6)

- [ ] Critic agent on results
- [ ] Senior reviewer Checkpoint A (before drafting)
- [ ] Paper-writer drafts manuscript (8-10 pages)
- [ ] Mock peer review
- [ ] Rebuttal pass
- [ ] Senior reviewer Checkpoint B
- [ ] **PRIORITY**: arXiv preprint by end of week 6
- [ ] Then commit to ICLR 2027 Evaluation track

## Compute estimates

| Phase | Wall-time | Cost |
|-------|-----------|------|
| Benchmark curation | 1 wk | $0 |
| API runs (5 × 1000 × ~6k token reasoning) | 1 wk | $1,500 |
| Annotation | 2 wk | $0 (solo+partner) or $500 (Prolific) |
| Analysis + figures | 1 wk | $0 |
| Manuscript | 1 wk | $0 |
| **Total** | **6 wk** | **$1,500-$2,000** |

## Deliverable

- arXiv preprint within 6 weeks of start
- ICLR 2027 Evaluation track submission Sep 19, 2026
- Open-source code + benchmark + annotation guidelines
- Companion blog post explaining clinical / legal / nuclear / financial / journalism implications for each domain's practitioner audience
