# Paper 02 — Attention Sinks in GQA and Sliding-Window Transformer Architectures

## One-line summary
The original attention-sink phenomenon (Xiao et al. 2023) was documented on full-attention Llama-1 and GPT-2. Modern frontier models use **grouped-query attention** (Llama-3.1, Qwen2.5) and **sliding-window attention** (Mistral-7B). Whether attention sinks persist, move, or disappear in these architectures — and whether sink dynamics predict the "lost-in-the-middle" retrieval failure mode — is currently untested.

## Hypotheses

- **H1** — GQA preserves attention sinks but distributes them across query groups in a predictable per-group pattern.
- **H2** — Sliding-window attention breaks the canonical first-token sink and produces windowed sinks at the start of each window, with non-trivial implications for streaming inference.
- **H3** — Sink magnitude at long context correlates negatively (Pearson ρ < −0.3) with needle-in-a-haystack retrieval accuracy at the corresponding depth.

## Experimental plan

### Models (inference only, 4-bit NF4 / GPTQ)
- **Llama-3.1-8B-Instruct** (GQA, full attention)
- **Mistral-7B-Instruct-v0.3** (SWA, window = 4096)
- **Qwen2.5-7B-Instruct** (GQA, full attention)
- **Llama-3.2-1B-Instruct** (small control)

### Context lengths
512, 2K, 4K, 8K, 16K

### Tasks
- Needle-in-a-haystack (depth grid 0–100 % in 10 % increments)
- LongBench retrieval subtasks (HotpotQA, MultiFieldQA-en, NarrativeQA)

### Measurements
- Per-layer **sink-token attention mass** (top-k attention from each query group to first / sink tokens)
- **Sink-position distribution** (which positions attract disproportionate attention)
- **Per-head-group attention entropy**
- Correlation of sink magnitude with retrieval accuracy at each context-length × depth bucket
- Streaming-inference accuracy under the StreamingLLM "preserve sink + recent" eviction policy, with sink count k ∈ {1, 2, 4, 8}

### Output artifacts
- `results/tables/sink_mass_per_layer.csv`
- `results/tables/sink_position_distribution.csv`
- `results/tables/sink_retrieval_correlation.csv`
- `figures/heatmap_sink_attention.{pdf,png}` (one per model)
- `figures/sink_vs_retrieval_scatter.{pdf,png}`

### Wall-time budget
- Pure inference; ~3–5 days end-to-end on RTX 4070
- VRAM: ~6 GB per model at 4-bit; trivially under envelope

## Target venue

- **Primary**: ARR August 3, 2026 cycle → EMNLP 2026 Findings commit Aug 2 (tight); or ARR October 12, 2026 cycle → EACL 2027.
- **Workshop short-form**: NeurIPS 2026 UniReps / Foundation Model Internals workshop (~Aug 22, 2026).
- **Stretch**: ICLR 2027 main (~Sep 19, 2026 abstract).
- **Safety net**: TMLR rolling.

## Compute envelope

- Single RTX 4070, 12 GB VRAM, 4-bit inference only.
- No training. No fine-tuning. No backward passes.
- Disk: ~30 GB for cached attention weights at 16K context.

## Keywords

attention sinks, grouped-query attention, sliding-window attention, GQA, SWA, Llama-3, Mistral, Qwen2.5, streaming LLM, needle-in-a-haystack, long-context, lost in the middle

## Related arXiv IDs

- 2309.17453 — Xiao et al., *Efficient Streaming Language Models with Attention Sinks* (foundational)
- 2307.03172 — Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*
- 2305.13245 — Ainslie et al., *GQA: Training Generalized Multi-Query Transformer Models*
- 2310.06825 — Mistral 7B paper (SWA)
- Recent 2025/2026 attention-sink and StreamingLLM successor papers

## Risks / kill conditions

- 🟡 An adjacent paper may have measured parts of this; the arXiv scout must verify before week 1 ends.
- 🟡 Effect sizes may be small for GQA-only models (no architectural break); mitigation = include Mistral SWA which is more likely to show qualitatively different sinks.
- 🟢 Even if sinks are unchanged in GQA, that itself is publishable (a clean negative result).

## Ethics

- Pure observational interpretability on open-weight models. No dual-use concerns.

## Headline result we will know after the experiments

A side-by-side characterisation of attention-sink behaviour across full-attention, GQA, and SWA models, with a single scatter plot showing whether sink magnitude predicts long-context retrieval performance. If H3 holds, the streaming-inference community has a new lever; if it fails, the field can stop using sink-preservation heuristics as a universal fix.
