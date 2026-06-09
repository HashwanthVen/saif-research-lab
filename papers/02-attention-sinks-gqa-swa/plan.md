# Paper 02 — Experimental Plan

## Phase 1: Setup (week 1, days 1–2)

- [ ] Download / quantise to NF4 4-bit: Llama-3.1-8B-Instruct, Mistral-7B-Instruct-v0.3, Qwen2.5-7B-Instruct, Llama-3.2-1B-Instruct
- [ ] Hook every attention layer to capture attention weights without materialising the full N×N matrix at 16K (sparse top-k attention export)
- [ ] Generate NIAH and LongBench fixtures; pre-tokenise at every target length

## Phase 2: Attention measurement (week 1, days 3–5)

- [ ] Run 1A: per-layer attention-mass measurement, all 4 models × 5 context lengths × 100 NIAH samples
- [ ] Save sparse top-32 attention indices per token (disk-bounded; aggregate online to stay within 30 GB)
- [ ] Aggregate to per-layer / per-head-group / per-sink-position tables

## Phase 3: Retrieval correlation (week 2, days 1–3)

- [ ] Run NIAH retrieval at every context length × depth bucket × model
- [ ] Run LongBench retrieval subtasks at every context length × model
- [ ] Correlate (depth-wise) sink magnitude with retrieval success rate
- [ ] Generate scatter plots and Pearson / Spearman tables

## Phase 4: Streaming-inference test (week 2, days 4–5)

- [ ] Implement / port StreamingLLM eviction policy (preserve sink + recent N tokens)
- [ ] Sweep sink count k ∈ {1, 2, 4, 8}, recency window N ∈ {1024, 4096}
- [ ] Measure perplexity and downstream accuracy on PG19 + LongBench

## Phase 5: Analysis & figures (week 3, days 1–2)

- [ ] fig01: attention-mass heatmaps (layer × head-group) for each model
- [ ] fig02: sink-position distribution histograms
- [ ] fig03: sink-magnitude vs NIAH-retrieval-accuracy scatter
- [ ] fig04: StreamingLLM k-sweep perplexity curves
- [ ] Tables: per-layer summary, per-model summary, correlation table

## Phase 6: Critique → draft → submit (week 3 day 3 onward)

- [ ] Critic on results
- [ ] Senior reviewer Checkpoint A
- [ ] Paper-writer drafts manuscript (target: 8 pages, ACL Findings format)
- [ ] Mock peer review
- [ ] Rebuttal pass
- [ ] Senior reviewer Checkpoint B
- [ ] Submit to ARR (next deadline) or NeurIPS workshop

## Compute estimates

| Phase | Wall-time | VRAM |
|-------|-----------|------|
| Setup + quantisation | 2 h | ~6 GB peak |
| Attention measurement (4 models × 5 lengths × 100 samples) | ~30 h | ~7 GB |
| Retrieval correlation | ~20 h | ~7 GB |
| Streaming test | ~12 h | ~7 GB |
| Total | ~70 h (~3 calendar weeks) | within envelope |

## Deliverable

An 8-page paper with a clean architectural characterisation, an open-source attention-export library, and a single decisive scatter plot answering H3.
