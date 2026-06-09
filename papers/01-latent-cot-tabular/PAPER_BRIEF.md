# Paper 01 — Latent Chain-of-Thought in Tabular Foundation Models: A Mechanistic Account

## One-line summary
NanoTabPFN gains from a latent CoT scratchpad — but the mechanism is unknown. We probe and ablate to determine whether the scratchpad encodes interpretable intermediate computations (feature ranking, pairwise comparisons, sort-like operations) beyond raw additional depth.

## Hypotheses

- **H1** — Latent CoT scratchpad tokens linearly encode feature-importance / pairwise-comparison structure recoverable via linear probes (target probe AUROC ≥ 0.70 on synthetic comparison tasks).
- **H2** — A depth-matched non-CoT model and a looped-transformer baseline both underperform CoT by ≥ 2% on heterogeneous OpenML tabular tasks, isolating the contribution of the scratchpad **beyond compute budget**.
- **H3** — The CoT advantage scales with task feature heterogeneity: gains are larger for tables with mixed numerical + categorical features than for purely numerical ones.

## Experimental plan

### Models
- **NanoTabPFN** (< 100 M parameters; HuggingFace open weights)
- Optional secondary: **TabPFN-v2** if compute allows

### Datasets
- **TabArena** (30+ heterogeneous OpenML tasks)
- **Synthetic probes** (custom-generated): `rank-by-column`, `top-k feature`, `pairwise-greater`, `argmax`, `sort-positional`

### Conditions
1. Baseline NanoTabPFN (no CoT)
2. NanoTabPFN + latent CoT (k = {2, 4, 8} scratchpad tokens)
3. Depth-matched non-CoT (extra layers, no scratchpad)
4. Looped-transformer (tied weights, k loops)
5. CoT + token-dropout ablation (random drop of scratchpad tokens at inference)
6. CoT with synthetic-task pretrained scratchpad initialisation (does pre-seeding help?)

### Metrics
- Held-out accuracy / NLL on TabArena
- Linear-probe AUROC on synthetic property recovery for each scratchpad token position
- Ablation deltas (Δacc per ablation)
- Attribution maps from scratchpad tokens to output
- Compute-matched comparison (matched FLOPs, not matched layers)

### Training & wall-time budget
- NanoTabPFN training: ~12–24 h
- Each ablation: ~6 h
- Total: ~5–7 days on RTX 4070

## Target venue

- **Primary**: TMLR (rolling, correctness-gated — perfect fit)
- **Secondary**: ICML 2027 tabular track / main (~Jan 2027 abstract)
- **Workshop fallback**: NeurIPS 2026 UniReps or D&B workshop (~Aug 22, 2026)

## Compute envelope

- Single RTX 4070, 12 GB VRAM. NanoTabPFN trivially fits. Even TabPFN-v2 inference fits at FP16.
- Disk: ≤ 50 GB for cached activations.
- Wall time: 1–2 weeks end-to-end on a single GPU.

## Keywords

tabular foundation models, TabPFN, NanoTabPFN, latent chain-of-thought, mechanistic interpretability, scratchpad tokens, linear probing, OpenML, tabular ML

## Related arXiv IDs

- 2505.XXXX — Dudley & Oymak, *Latent Chain-of-Thought Improves Structured-Data Transformers* (the paper we extend)
- Prior TabPFN line (Hollmann et al. 2023, 2024)
- Looped transformer line (Yang et al. 2024, Du et al. 2025)
- Tabular benchmarking (TabArena 2024+)

## Risks / kill conditions

- 🔴 Dudley & Oymak release a v2 extension that subsumes our mechanism question → halt, surface to human.
- 🟡 NanoTabPFN may be too small for clean probing signal; mitigation = include TabPFN-v2 if compute allows.
- 🟡 Synthetic probe tasks may be too easy / unrelated to real tabular tasks; design probes carefully and validate.

## Ethics

- Pure interpretability research on open models and open datasets. No dual-use concerns.
- Standard reproducibility commitments apply (see `shared/reproducibility-checklist.md`).

## Headline result we will know after the experiments

A 4-cell matrix: {CoT, no-CoT} × {feature-heterogeneous, pure-numerical} accuracy, with confidence intervals, plus a probe-AUROC table per scratchpad position. If the CoT advantage is real *and* localisable to specific scratchpad tokens that encode interpretable structure, the paper writes itself.
