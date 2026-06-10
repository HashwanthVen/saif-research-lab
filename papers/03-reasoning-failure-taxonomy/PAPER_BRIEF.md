# Paper 03 — Reasoning Model Reliability: Cross-Domain Failure Taxonomy in Professional Contexts

## One-line summary
Reasoning models (o1, o3-mini, DeepSeek-R1, Claude 3.7 Sonnet Thinking, Gemini 2.5) are being deployed in medicine, law, nuclear safety review, financial audit, and journalism fact-checking — five domains where failure has high real-world stakes. Three independent 2025 studies found these models fail in distinct, domain-specific ways, but no work has produced a *cross-domain failure taxonomy*. We build one.

## Hypotheses

- **H1** — Reasoning models exhibit at least 4 distinguishable failure modes that span domains: (a) feature hallucination (inventing facts not present in the prompt), (b) pattern rigidity (over-applying memorized templates), (c) context compression (losing critical information in long contexts), (d) confidence miscalibration (overconfident wrong answers).
- **H2** — Failure-mode dominance is **domain-specific**, not model-specific: e.g., medical reasoning is dominated by pattern rigidity, legal reasoning by feature hallucination, nuclear safety review by context compression.
- **H3** — Confidence miscalibration is **uniformly high** across all five domains (calibration error > 0.15 in all cases), making confidence a poor stopgap regardless of domain.

## Experimental plan

### Models (5)
- **OpenAI o3-mini** (via API)
- **OpenAI o1** (via API, fallback if o3-mini incomplete)
- **DeepSeek-R1** (via API or Together AI)
- **Anthropic Claude 3.7 Sonnet Thinking** (via API)
- **Google Gemini 2.5 Pro Thinking** (via API)

### Domains + Benchmarks (5)
| Domain | Benchmark | Source | License |
|--------|-----------|--------|---------|
| Medicine | M-ARC (Medical Abstraction & Reasoning Corpus) | Kim et al. arxiv:2502.03411 | Open via authors |
| Legal | CUAD (Contract Understanding Atticus Dataset) | atticusprojectai.org/cuad | CC BY 4.0 |
| Nuclear Safety | FSAR-Argue (we curate from public NRC ADAMS FSAR excerpts) | NRC ADAMS | Public domain |
| Financial Audit | EDGAR-Q (we curate from SEC 10-K/10-Q risk factor sections) | sec.gov/edgar | Public domain |
| Journalism | ClaimBuster | idir.uta.edu/claimbuster | CC BY-NC 4.0 |

### Failure taxonomy (4 codes)
1. **F1 — Feature Hallucination**: model asserts a fact not present in the prompt
2. **F2 — Pattern Rigidity**: model applies a stereotyped template inappropriately
3. **F3 — Context Compression**: model loses information embedded earlier in the prompt
4. **F4 — Confidence Miscalibration**: high stated confidence on incorrect answers

Each failed response is coded with one or more F-codes by 2 independent annotators (Cohen's κ ≥ 0.7 required).

### Methodology
1. Sample 200 instances per domain (1,000 total per model; 5,000 total responses)
2. Each response: collect reasoning trace + final answer + self-reported confidence
3. Annotate each failure (by both authors) with F-codes
4. Per-domain failure-mode distribution; per-model failure-mode distribution
5. Mechanistic analysis: chain-of-thought inspection to identify trace-level features predictive of each failure mode
6. Confidence-calibration analysis: ECE per domain per model

### Output artifacts
- `results/tables/per_domain_per_model_failure_rates.csv`
- `results/tables/failure_mode_distribution.csv`
- `results/tables/confidence_calibration_ece.csv`
- `figures/failure_mode_heatmap.{pdf,png}` (5 models × 5 domains)
- `figures/calibration_curves.{pdf,png}`
- `figures/cot_failure_examples.{pdf,png}` (annotated reasoning traces)

### Wall-time + cost
| Phase | Time | Cost |
|-------|------|------|
| Benchmark curation (FSAR-Argue + EDGAR-Q) | 1 wk | $0 |
| API runs (5 models × 1000 prompts × ~6k tokens reasoning) | 1 wk | ~$1,500 |
| Annotation (2 annotators × 1000 responses) | 2 wk | $0 if solo+collaborator, $500 if Prolific |
| Analysis + figures | 1 wk | $0 |
| Manuscript | 1 wk | $0 |
| **Total** | **6 wk** | **~$1,500–$2,000** |

## Target venue

- **PRIMARY**: ICLR 2027 Evaluation track (~Sep 19, 2026 abstract est.)
- **SECONDARY**: NeurIPS 2026 D&B (~May deadline PAST → NeurIPS 2027)
- **TERTIARY (high-impact path)**: *The Lancet Digital Health* op-ed companion + *Nature Medicine* perspective for the medical-domain finding
- **FALLBACK**: TMLR (rolling) — perfect fit for evaluation-methodology paper

## Compute envelope

- **Pure API** — no local GPU required.
- Compatible with RTX 4070 if local inference of DeepSeek-R1-Distill-Qwen-7B is added as a sixth open-weight baseline (4-bit, fits in 12 GB).

## Keywords

reasoning models, o1, o3, DeepSeek-R1, Claude Thinking, Gemini Thinking, failure modes, cross-domain evaluation, AI safety, confidence calibration, professional deployment

## Related arXiv IDs

- 2502.03411 — Kim et al., *LLMs vs. Physicians on M-ARC* (Feb 2025) — medical reasoning failures
- 2505.XXXXX — Heyman & Zylberberg, *Reasoning Models Hallucinate Graph Edges* (May 2025) — logical reasoning failures
- 2504.09762 — *Stop Anthropomorphizing Intermediate Tokens* (Jun 2026)
- DeepSeek-R1 tech report arXiv 2501.09023

## Risks / kill conditions

- 🔴 **HIGHEST SCOOP RISK** — Multiple AI lab safety teams (Anthropic, OpenAI, Apollo, METR) likely working on this. The 6-9 month window is real. **Move within 6 weeks of start.**
- 🔴 **Contamination risk** — o1/R1 may have seen M-ARC, CUAD, ClaimBuster in training. FSAR-Argue and EDGAR-Q are our defenses (curated post-training cutoff).
- 🟡 **Annotation reliability** — 2-annotator κ ≥ 0.7 is non-negotiable; budget 1 extra week if first round κ < 0.7
- 🟡 **Rapid capability change** — Models improve quickly; paper must hit arXiv within 6 weeks of evaluation completion

## Ethics

- All five domains are public-data benchmarks. No human subjects.
- For medical domain: do not publish specific failed clinical scenarios as if they were validated case studies; always include "evaluation context only, not clinical guidance" disclaimer.
- For nuclear domain: stay strictly on public-domain NRC documents; do not approach safeguards-restricted material.
- Submit responsible-disclosure summary to AI labs before public release.

## Headline result we will know after experiments

A 5 × 5 heatmap showing which failure mode dominates in which domain for each model, plus a clear calibration story. If H1-H3 hold, this becomes the canonical "where reasoning models fail in professional contexts" reference — cited by every clinical AI deployment guideline, every legal-tech vendor risk assessment, every nuclear-engineering AI policy document for the next 2-3 years.
