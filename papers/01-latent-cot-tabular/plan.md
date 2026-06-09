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

The total depends almost entirely on whether Dudley & Oymak (2026) have released
their pretrained CoT-variant NanoTabPFN checkpoint. **The researcher agent must
resolve this in week 1** before the experiment-runner commits to a path.

### Best case — pretrained CoT checkpoint available on HF

Pure inference + lightweight probing. NanoTabPFN is in-context, so per-task
prediction is seconds, not minutes.

| Phase | Wall-time | VRAM |
|-------|-----------|------|
| Setup smoke | 1 h | < 2 GB |
| Inference: 30 TabArena tasks × 4 conditions × 3 seeds | 2–6 h | 2–4 GB |
| Cache scratchpad activations | 1–3 h | 2–4 GB |
| Train linear probes (could run on CPU) | < 1 h | < 1 GB |
| k-sweep (k ∈ {0,2,4,8,16}) | 2–4 h | 2–4 GB |
| Token-dropout ablation | 1–2 h | 2–4 GB |
| **Best-case total** | **~8–15 GPU-hrs** | well within envelope |

### Worst case — must retrain base + variants from scratch

| Phase | Wall-time | VRAM |
|-------|-----------|------|
| Setup smoke | 1 h | < 2 GB |
| Pretrain NanoTabPFN base | 8–20 h | 4–6 GB |
| Pretrain 3 architectural variants (CoT-k=4, deep-no-CoT, looped) | 24–60 h | 4–6 GB |
| Inference + probing as above | 8–15 h | 2–4 GB |
| **Worst-case total** | **~40–95 GPU-hrs** | well within envelope |

### Decision gate

If the CoT checkpoint exists → best case applies; full experimental program
finishes in a weekend.

If it does not exist → escalate to the human before committing to the
worst-case 95-hour path. Consider whether the question can be answered with
LoRA fine-tuning of the base NanoTabPFN checkpoint instead of full retraining.

## Deliverable

A TMLR-ready manuscript + open-source code + a pip-installable package `tabcot-probe` that anyone can run on NanoTabPFN / TabPFN-v2 to reproduce the mechanism analysis.
