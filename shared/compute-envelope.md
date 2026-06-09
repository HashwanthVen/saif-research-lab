# Compute Envelope — RTX 4070 (12 GB)

> This file is sacred. Every agent must respect it. Violations are caught by the experiment-runner's pre-flight VRAM check.

## Hardware

- **GPU**: NVIDIA GeForce RTX 4070 (Ada Lovelace, AD104)
- **VRAM**: 12 GB GDDR6X
- **Peak FP16 / BF16 (tensor cores)**: ~58 TFLOPS
- **Peak FP32**: ~29 TFLOPS
- **Memory bandwidth**: 504 GB/s
- **TDP**: 200 W
- **CUDA capability**: 8.9

## Practical model-size envelope

| Workload | Fits? | Notes |
|----------|-------|-------|
| 7B model, 4-bit inference (NF4 / GPTQ) | ✅ | ~4.5 GB weights + 2–4 GB KV cache |
| 7B model, QLoRA 4-bit + LoRA adapters (rank 16) | ✅ | ~9–10 GB; batch 1, grad-accum |
| 7B model, FP16 inference | ❌ | ~14 GB, does NOT fit |
| 3B model, FP16 full fine-tune + Adam | ✅ tight | ~9–11 GB; grad checkpointing, batch 1 |
| 1.5B model, BF16 full fine-tune + AdamW 8-bit | ✅ | ~10–11 GB |
| 1B model, FP16 full fine-tune | ✅ | ~6–8 GB |
| 13B model, any precision | ❌ | Out of scope |
| 70B+ inference | ❌ | Out of scope |
| SAE training on cached activations | ✅ | SAE itself <500M; cache to disk |
| NanoTabPFN (< 100M) | ✅ | Trivial |
| Pretraining any useful LLM | ❌ | Multi-GPU only |

## Required techniques (use as needed)

- `bitsandbytes` NF4 quantisation for inference and QLoRA
- `peft` for LoRA / QLoRA adapters
- `accelerate` for gradient checkpointing, mixed precision
- Activations cached to disk for SAE training (do not stream every forward pass)
- `torch.compile` for inference speedup on Ada
- Gradient accumulation over batch 1 if needed

## Forbidden without a written exception

- Multi-GPU code (no `DistributedDataParallel`, no `FSDP`)
- Pretraining from scratch
- Full fine-tuning of any model > 1.5B
- 16-bit inference of any model > 5B
- Anything that needs > 11 GB at peak (leave 1 GB headroom for system)

## Pre-flight checklist (every experiment-runner run)

```python
import torch
free, total = torch.cuda.mem_get_info()
free_gb = free / 1024**3
print(f"Free VRAM: {free_gb:.2f} GB")
# Then dry-forward one batch and report peak allocated
```

If the dry forward exceeds 11 GB allocated, abort the run and surface a `vram_oom_risk` blocker.

## Wall-time budget

- Per experiment: ≤ 24 h
- Per paper: ≤ 168 GPU-hours / week
- If a configuration needs more, the experiment-runner must surface to the orchestrator with a justification before starting.

## Cloud GPU fallback

GitHub Codespaces has **no GPU** (verified June 2026 against your account — only 2/4/8/16/32-core CPU tiers). If the local RTX 4070 is unavailable, see `shared/cloud-gpu.md` for vetted alternatives (Kaggle free tier, Vast.ai 4090 spot, RunPod on-demand, Modal serverless).
