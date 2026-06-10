# Paper 03 — Experimental Plan

## Critical urgency note
**This paper has the HIGHEST scoop risk in the lab.** 6-9 month window before competing lab teams publish. Target arXiv preprint within 6 weeks of starting.

## Phase 1: Benchmark curation (week 1)

- [ ] Pull M-ARC (contact Kim et al. or use replication subset)
- [ ] Pull CUAD (public)
- [ ] Pull ClaimBuster (public)
- [ ] Curate **FSAR-Argue** from public NRC ADAMS FSAR excerpts (target: 200 argument-completeness items)
- [ ] Curate **EDGAR-Q** from SEC 10-K/10-Q risk-factor sections post-2024-cutoff (target: 200 items)
- [ ] Annotator-agreement pilot: 20 items × 2 annotators on each benchmark → require κ ≥ 0.7 on the **primary** F-code (see § Annotation rubric)
- [ ] Prompt-leakage check: for each of the 1,000 prompts, compute a SHA256 of the normalized prompt text and grep public dump indices (Common Crawl, OpenWebText2, RedPajama). Any prompt with an exact hash match in a known training corpus is flagged and replaced.

## Phase 2: Model evaluation (week 2)

- [ ] Run **all** model evaluation through `experiments/scripts/eval_runner.ps1` (hard constraint — no other path produces records eligible for the manuscript). `experiments/src/mock_smoke.py` is for cross-platform CI smoke tests only.
- [ ] 8 GHC CLI models active (4 thinking + 4 non-thinking baselines per `experiments/configs/models.json`); $0 spend.
- [ ] Run 200 prompts × 5 domains × 8 models × 3 seeds = 24,000 runs through the PS1 harness, resumable via `-Resume`.
- [ ] Capture: prompt, reasoning trace (where surfaced by the CLI), final answer, self-reported confidence (0–1 scale; elicited via a fixed suffix appended to every prompt — see § Confidence elicitation).
- [ ] All artifacts land in `results/runs/<UTC>_<sha>/` with code commit hash, config snapshot, raw logs, seed, model ID.

### Phase 2b: Long-context position ablation (required for F3 testability)

To make F3 (Context Compression) **falsifiable** rather than post-hoc, every prompt has a designated **diagnostic span** — the token-span whose deletion changes the ground-truth answer. We run three position variants per prompt:

- **early**: diagnostic span placed in the first 25% of the prompt
- **middle**: diagnostic span in the middle 50%
- **late**: diagnostic span in the final 25%

Per-position accuracy collapse (early ≫ late) is the operational signature of F3. A response coded F3-primary must show the model failing on at least one position where a model of the same family succeeded on a different position, OR must explicitly fail to reference the diagnostic span in its reasoning trace.

Cost: 3× prompt count for the F3-eligible subset (~50 prompts/domain × 5 domains = 250 prompts × 3 positions = 750 extra prompts). At 8 models × 3 seeds this is 18,000 additional runs through PS1. Still $0 on GHC CLI.

## Phase 3: Failure annotation (weeks 3-4)

### Annotation rubric (frozen before any annotator opens a response)

**Primary code (exactly one per wrong response).** Apply the decision tree in order; the first rule that fires wins. F1 → F3 → F2 → F4.

```
START: is the final answer wrong against the ground-truth source?
  NO  → not coded (correct response; recorded for accuracy but no F-code)
  YES → continue

Q1 (F1): does the response contain at least one declarative claim about a
         named entity, number, date, citation, statute, dose, or rule that
         is (a) NOT entailed by the prompt AND (b) demonstrably FALSE
         against the ground-truth source?
  YES → PRIMARY = F1. Record the fabricated token(s) verbatim in the
        annotation row. STOP.
  NO  → continue.

Q2 (F3): is the wrong answer correctable by re-presenting the prompt with
         the diagnostic span moved to the early position (per Phase 2b
         ablation), OR does the reasoning trace fail to reference the
         diagnostic span?
  YES → PRIMARY = F3. Record the diagnostic span and the position-variant
        accuracies. STOP.
  NO  → continue.

Q3 (F2): is the wrong answer the *correct* answer to a *different, more
         frequently encountered* version of the question (e.g., adult vs
         pediatric, US vs UK law, post-2024 vs pre-2024 reg)?
  YES → PRIMARY = F2. Record the "shadow question" the model appears to
        have answered. STOP.
  NO  → continue.

Q4 (F4): is self-reported confidence in the top quartile (≥ 0.75 on the
         0–1 scale)?
  YES → PRIMARY = F4.
  NO  → PRIMARY = F0 (unclassifiable; exclude from H1/H2; report in
        Limitations as denominator).
```

**Secondary codes (zero or more).** After the primary code is set, walk the same four questions again and record any additional codes that fire. Secondary F4 is recorded on *every* wrong response with top-quartile confidence regardless of primary code; H3's ECE analysis uses this secondary distribution.

**Confidence elicitation.** Every prompt has the fixed suffix:
> "After your final answer, on a new line write exactly: `CONFIDENCE: <p>` where `<p>` is your probability that your answer is correct, as a decimal between 0.00 and 1.00."

If the model does not produce a parseable `CONFIDENCE:` line, the response is excluded from F4 / H3 (but still annotated for F1/F2/F3).

### Worked examples (one per code, per domain — abbreviated)

- **F1 (medicine):** Prompt asks the recommended first-line agent for community-acquired pneumonia in a 34-year-old without comorbidities. Model answers "moxifloxacin 400 mg PO daily, per the 2024 IDSA guideline section 3.2.1." There is no IDSA 2024 section 3.2.1; the actual IDSA first-line for outpatient CAP in this population is amoxicillin or doxycycline. The fabricated citation triggers F1.
- **F2 (legal):** Prompt is a CUAD clause that limits indemnification to "direct damages excluding consequential, special, or punitive." Model answers as if the clause used the *broader* "any and all damages" template common in older contracts. Facts are individually defensible but the wrong template was applied → F2.
- **F3 (nuclear):** A 4,800-token FSAR excerpt has a single sentence late in the document stating "the auxiliary feedwater pump is **not** safety-related." The model answers "yes, safety-related." Moving that sentence to the first paragraph (early position) flips the answer to correct → F3 confirmed.
- **F4 (finance):** Model gives a wrong answer to an EDGAR-Q risk-factor question with no fabricated facts, no shadow-question, no diagnostic-span miss; states `CONFIDENCE: 0.92`. → F4.

### Ambiguous cases (and how the precedence rule resolves them)

- **F1 + F3 co-occurrence (journalism):** Model fabricates a quote ("according to a Reuters report dated March 14") *and* misses the diagnostic span (the prompt explicitly says the article is from AP, not Reuters). Both Q1 and Q2 would fire. Precedence F1 → F3 means **primary = F1**, secondary = F3.
- **F2 + F1 boundary (medicine):** Model applies the adult dosing template to a pediatric case (looks like F2) but the specific dose it states ("acetaminophen 1000 mg q6h") is fabricated for a 4-year-old — no published pediatric guideline contains that dose at that frequency for that age. Q1 fires before Q3 → **primary = F1**, secondary = F2.
- **F3 vs F2 (legal):** Model misses a definitional clause early in a long contract and then applies the wrong template downstream. Looks like F2 in the reasoning trace, but the ablation shows moving the missed clause to the late position **does not** change the answer (the model misses it either way). Q2 does not fire under the operational test; Q3 does → **primary = F2**, secondary = F3.

### Inter-annotator protocol

- 2 annotators code independently, blinded to model identity (model name redacted from the response before display).
- 20% overlap sample drawn uniformly at random per domain; Cohen's κ computed on the primary code.
- **Hard gate: κ ≥ 0.7 on every domain before the full corpus is coded.** If κ < 0.7 on any domain, the rubric is revised and the pilot is re-run on a fresh 20-item sample.
- Disagreements on the overlap sample: third pass with both annotators present; if no consensus → primary = F0, item excluded from H1/H2 statistics.
- All annotation decisions, including the verbatim fabricated tokens / shadow questions / diagnostic spans, recorded in `results/annotations/coded.csv`.

- [ ] Freeze rubric and decision tree (this document is the frozen artifact; any change requires a `reviews/rubric-change-<date>.md` justification)
- [ ] Pilot annotation: 20 items × 2 annotators × 5 domains → compute κ per domain
- [ ] If κ ≥ 0.7 on all domains → proceed; else iterate on rubric and re-pilot
- [ ] Full annotation: 2 annotators code 24,000 / 3 = 8,000 (prompt, model, seed-1) responses each, with 20% overlap
- [ ] Adjudicate disagreements; record F0 exclusions
- [ ] Output `results/annotations/coded.csv` with columns: work_id, prompt_id, domain, model, seed, primary_code, secondary_codes, fabricated_tokens, shadow_question, diagnostic_span, annotator_a, annotator_b, adjudicated

## Phase 4: Analysis (week 5)

- [ ] Compute per-model per-domain accuracy (with bootstrap 95% CIs, B=10,000)
- [ ] Compute per-model per-domain **primary** F-code distribution (F1–F4 fractions; F0 reported as denominator)
- [ ] Test H1: confusion-matrix-style distinguishability of the four primary codes (per-domain inter-rater κ on the overlap sample is the headline statistic; supplemented by per-code precision/recall against the adjudicated gold)
- [ ] Test H2: χ² independence test of domain × primary-F-code distribution; Holm-Bonferroni correction across the 5 × 4 = 20 cell post-hocs; bootstrap CIs on each cell
- [ ] Test H3: ECE per (model, domain) using the **secondary** F4 distribution + correctness; 10 equal-width confidence bins; reliability diagrams per (model, domain)
- [ ] Position-ablation analysis (F3): per-model accuracy curves over {early, middle, late}; report slope and significance
- [ ] CoT trace inspection: find lexical / structural features predictive of each primary F-code
- [ ] Generate all figures + tables listed in `PAPER_BRIEF.md` § Output artifacts

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

Compute is **$0** because all model calls go through the GHC Copilot CLI on the author's seat (see `HANDOFF.md` § 3). The only spend item is optional Prolific annotation.

| Phase | Wall-time | Cost |
|-------|-----------|------|
| Benchmark curation + prompt-leakage check | 1 wk | $0 |
| GHC CLI runs (24,000 main + 18,000 position-ablation = 42,000 runs via `eval_runner.ps1`) | 1–2 wk | $0 |
| Annotation (pilot + full corpus + adjudication) | 2 wk | $0 (solo+partner) or $500 (Prolific) |
| Analysis + figures | 1 wk | $0 |
| Manuscript | 1 wk | $0 |
| **Total** | **6–7 wk** | **$0–$500** |

## Deliverable

- arXiv preprint within 6 weeks of start
- ICLR 2027 Evaluation track submission Sep 19, 2026
- Open-source code + benchmark + annotation guidelines
- Companion blog post explaining clinical / legal / nuclear / financial / journalism implications for each domain's practitioner audience
