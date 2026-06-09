# Paper 01 — Experimental Plan

## Phase 1: Setup (week 1)

- [ ] Clone NanoTabPFN weights (Hugging Face)
- [ ] Acquire TabArena dataset list (30+ OpenML task IDs)
- [ ] Generate synthetic probe datasets (5 task families × 1000 examples each)
- [ ] Implement training loop with config-driven seed / model size
- [ ] Smoke test: train NanoTabPFN baseline 10 epochs on one TabArena dataset; confirm metrics non-degenerate

## Phase 2: Baselines (week 1–2)

- [ ] Run 1A: NanoTabPFN baseline, no CoT, 3 seeds, all 30 TabArena tasks
- [ ] Run 1B: NanoTabPFN + latent CoT (k = 4), 3 seeds, all 30 tasks
- [ ] Run 1C: depth-matched no-CoT (extra layers ≈ FLOPs of 1B), 3 seeds
- [ ] Run 1D: looped-transformer (tied weights, k = 4 loops), 3 seeds
- [ ] Aggregate: results/tables/01_baselines.csv

## Phase 3: Probing (week 2)

- [ ] Cache scratchpad-token activations for run 1B across all 30 TabArena tasks
- [ ] Train linear probes on each scratchpad token position for each synthetic property
- [ ] AUROC table → results/tables/02_probes.csv
- [ ] Sanity baseline: probe random-init NanoTabPFN to confirm signal is learned, not architectural

## Phase 4: Ablations (week 2–3)

- [ ] Scratchpad k-sweep: k ∈ {0, 2, 4, 8, 16}
- [ ] Token-dropout ablation: drop p ∈ {0, 0.25, 0.5} of scratchpad tokens at inference
- [ ] Pre-seeded scratchpad: warm-start scratchpad embeddings with probe targets — does it help?
- [ ] Feature-heterogeneity split: stratify results by (numerical-only) vs (mixed) tasks
- [ ] Aggregate: results/tables/03_ablations.csv

## Phase 5: Analysis & figures (week 3)

- [ ] Generate fig01: CoT vs no-CoT accuracy delta per TabArena task (forest plot)
- [ ] Generate fig02: probe AUROC heatmap (scratchpad position × probe target)
- [ ] Generate fig03: k-sweep accuracy curve with CIs
- [ ] Generate fig04: heterogeneity-stratified bar chart
- [ ] Generate fig05: attribution-map sample for one representative table

## Phase 6: Critique → draft (week 4)

- [ ] Hand artifacts to critic agent
- [ ] Address critic's top-3 weaknesses
- [ ] Senior reviewer Checkpoint A → proceed / abort
- [ ] If proceed: paper-writer drafts manuscript
- [ ] Mock peer review
- [ ] Rebuttal pass
- [ ] Senior reviewer Checkpoint B
- [ ] Submit to TMLR

## Compute estimates

| Phase | Wall-time | VRAM |
|-------|-----------|------|
| Setup smoke | 1 h | < 2 GB |
| Baselines (4 conditions × 3 seeds × 30 tasks) | ~30 h | 4–6 GB |
| Probing | 8 h | < 2 GB |
| Ablations | ~24 h | 4–6 GB |
| Total | ~63 h | well within envelope |

## Deliverable

A TMLR-ready manuscript + open-source code + a pip-installable package `tabcot-probe` that anyone can run on NanoTabPFN / TabPFN-v2 to reproduce the mechanism analysis.
