# Critic review — plan — 2026-06-10

## Verdict: major revision

Not fundamentally dead, but the current plan is not publishable. It confuses a plausible paper idea with a validated evaluation protocol. The largest risks are not implementation details: the taxonomy is not operational, two benchmarks do not exist yet, contamination is mostly hand-waved, and the statistical plan cannot support the cross-domain/model claims.

## Top-3 weaknesses

1. **What:** The F1–F4 taxonomy is not mutually distinct or operationalized. **Why:** `plan.md` says: "Develop F-code rubric: F1 hallucination, F2 rigidity, F3 compression, F4 miscalibration" and `PAPER_BRIEF.md` defines F1 as "model asserts a fact not present in the prompt", F2 as "model applies a stereotyped template inappropriately", F3 as "model loses information embedded earlier in the prompt", F4 as "high stated confidence on incorrect answers". A single wrong answer can be all four; no decision tree, examples, exclusion rules, or primary-code rule exists. **Severity:** 5. **Fix-cost:** 4.
2. **What:** Core benchmarks are imaginary or contamination-prone. **Why:** `plan.md` promises "Curate **FSAR-Argue**" and "Curate **EDGAR-Q**" in one week, while `PAPER_BRIEF.md` admits they are "we curate from public NRC ADAMS FSAR excerpts" and "we curate from SEC 10-K/10-Q risk factor sections". M-ARC, CUAD, and ClaimBuster are pre-cutoff/public datasets; `PAPER_BRIEF.md` itself says "o1/R1 may have seen M-ARC, CUAD, ClaimBuster in training." **Severity:** 5. **Fix-cost:** 5.
3. **What:** Statistical design cannot support H1–H3. **Why:** `plan.md` says "Run 200 prompts × 5 models × 5 domains = 5,000 responses" and "2 annotators code 1000 responses each (subset overlap for κ)" with no power analysis, no CI plan, no mixed-effects model, no multiple-comparison correction, no ECE bucket specification, and no κ method for overlapping multi-label codes. **Severity:** 5. **Fix-cost:** 4.

## List of false / unsupported claims

- Quote: `PAPER_BRIEF.md`: "Three independent 2025 studies found these models fail in distinct, domain-specific ways, but no work has produced a *cross-domain failure taxonomy*." Counter-evidence: no literature folder exists for this paper; `literature/` is empty. The plan contains no search protocol, inclusion criteria, or 2024–2026 cross-check. This is an unsupported novelty claim.
- Quote: `plan.md`: "**This paper has the HIGHEST scoop risk in the lab.** 6-9 month window before competing lab teams publish." Counter-evidence: no citation, scout report, search log, or named overlapping preprint is provided. `PAPER_BRIEF.md` only speculates: "Multiple AI lab safety teams ... likely working on this."
- Quote: `PAPER_BRIEF.md`: "No human subjects." Counter-evidence: the plan requires "2 annotators code 1000 responses each" and possibly "$500 if Prolific". Human annotation is human participation; at minimum IRB/exemption status and consent/data-handling need analysis.
- Quote: `plan.md`: "Benchmark curation | 1 wk | $0". Counter-evidence: two full benchmarks are not datasets yet: "FSAR-Argue" and "EDGAR-Q" must be designed, sampled, de-duplicated, answered, licensed, validated, and documented. One week is fantasy.
- Quote: `plan.md`: "API runs (5 × 1000 × ~6k token reasoning) | 1 wk | $1,500". Counter-evidence: `HANDOFF.md` changes the design to "5 domains × 200 prompts × 8 models × 3 seeds = **24,000 runs**" and says serial execution is "~200 hours". The plan is stale and under-costed.
- Quote: `plan.md`: "Capture: prompt, reasoning trace, final answer, self-reported confidence (1-5 or 0-1)". Counter-evidence: most production reasoning APIs do not reliably expose raw chain-of-thought; confidence is not native for these models. The plan does not define elicitation wording, parsing rules, refusals, or calibration mapping.
- Quote: `PAPER_BRIEF.md`: "If H1-H3 hold, this becomes the canonical 'where reasoning models fail in professional contexts' reference — cited by every clinical AI deployment guideline..." Counter-evidence: planned sample is 200 items/domain, partially synthetic/curated, with no practitioner validation. This is marketing, not a supported claim.
- Quote: `PAPER_BRIEF.md`: "Failure-mode dominance is **domain-specific**, not model-specific". Counter-evidence: no statistical model is specified to separate domain effects from model-family effects, prompt effects, benchmark effects, or interaction terms.
- Quote: `PAPER_BRIEF.md`: "Confidence miscalibration is **uniformly high** across all five domains (calibration error > 0.15 in all cases)". Counter-evidence: ECE threshold and bucket count are not justified; no confidence extraction protocol exists.

## List of missing baselines / ablations

- Missing non-reasoning baselines in `plan.md`: the plan lists only five reasoning models. `models.json` has 8 active models, including non-thinking baselines, but `plan.md` has not been updated. Without this, "reasoning model" effects are unidentifiable.
- Missing human/professional baseline or at least benchmark-author baseline for high-stakes domains.
- Missing retrieval/no-retrieval ablation for legal, finance, nuclear, and medical questions where model memory contamination is central.
- Missing prompt-format ablation: confidence before answer vs after answer; forced JSON vs free text; answer-only vs reasoning-enabled.
- Missing long-context position ablation for F3; otherwise "Context Compression" is not testable.
- Missing post-cutoff-only ablation for contamination defense. FSAR/EDGAR are claimed as defenses, but no pre/post cutoff split is defined.
- Missing model-family ablation: OpenAI/Anthropic/Google/DeepSeek effects confounded with model capability and hidden system prompts.
- Missing seed/stability ablation in `plan.md`; `HANDOFF.md` mentions 3 seeds, but the reviewed artifact still says 5,000 responses, not 24,000.
- Missing annotator-rubric ablation or adjudication sensitivity: distributions before vs after consensus.
- Missing ECE sensitivity ablation over bucket counts and adaptive vs fixed bins.

## List of statistical concerns

- **n:** 200 items/domain is asserted, not powered. No minimum detectable effect for domain-vs-model dominance.
- **Seeds:** `plan.md` has no seeds. `HANDOFF.md` adds `NumSeeds=3`, but that changes the experiment to 24,000 runs and is not integrated into statistical analysis.
- **Significance:** no confidence intervals, bootstrap plan, Bayesian model, mixed-effects regression, or permutation test.
- **Multiple comparisons:** at least 5 domains × 5/8 models × 4 failure codes × accuracy/ECE comparisons. No correction plan.
- **κ adequacy:** "κ ≥ 0.7" with 2 annotators is weak for overlapping multi-label codes. Standard Cohen's κ assumes categorical labels; this needs per-code binary κ, prevalence-adjusted κ, Krippendorff's α, or multi-label agreement. No per-code minimum is specified.
- **Subset overlap:** `plan.md` says "2 annotators code 1000 responses each (subset overlap for κ)" but not the overlap size. A small overlap makes κ unstable.
- **Class imbalance:** failure modes will be rare/uneven; κ and F-code fractions will be prevalence-sensitive.
- **Consensus bias:** "Resolve disagreements via consensus pass" can erase uncertainty if pre-consensus and post-consensus results are not both reported.
- **ECE:** bucket count, confidence scale, empty-bin handling, and sensitivity are unspecified. ECE is fragile at small n per model-domain cell.
- **Unit of analysis:** response, prompt, seed, and model are not independent. The plan treats them as if they are.

## List of reproducibility gaps

- No committed YAML config per run, despite `shared/coding-standards.md`: "Every run is fully described by a single YAML config."
- No `requirements.txt` / `pyproject.toml` pinning plan.
- No `scripts/replicate.py`, despite `shared/reproducibility-checklist.md` requiring it.
- No dataset fetch scripts for M-ARC, CUAD, ClaimBuster, ADAMS, or EDGAR.
- No license verification workflow. ClaimBuster is CC BY-NC 4.0; this matters for open benchmark release.
- No benchmark item schema, answer-key format, validation protocol, duplicate checking, or contamination audit.
- No model version pinning. Names like "o3-mini", "Claude 3.7 Thinking", and "Gemini 2.5 Pro Thinking" are mutable service labels.
- No plan for unavailable raw reasoning traces. The output artifact `figures/cot_failure_examples.{pdf,png}` assumes access that APIs may not provide.
- No parser specification for final answers or self-reported confidence.
- No audit trail for human annotation: annotator IDs, blinded order, instructions, timestamps, adjudication logs.
- No environment capture for PowerShell, Copilot CLI version, OS, rate limits, or API/backend changes.
- `eval_runner.ps1` has a known `Start-Job` bug per `HANDOFF.md`, yet `plan.md` does not allocate time to fix or validate the harness.
- The compute envelope is under-specified. `PAPER_BRIEF.md` says "Pure API — no local GPU required", so it likely does not conflict with GPU-bound papers 01/02, but the 24,000-run GHC/Copilot plan may conflict on rate limits, account quotas, and shared host wall time. No cross-paper scheduling or quota policy exists.

## One question the author cannot easily answer

If F1, F2, F3, and F4 can co-occur on the same wrong response, and confidence must be elicited by the same prompt that induces the answer, what exact blinded coding rule lets two annotators distinguish "pattern rigidity" from "context compression" without reading the model's unavailable private reasoning trace—and how would that rule survive a reviewer rerunning the same prompt with a different API model version?
