# Cloud GPU Fallback Options

> The default compute target is the local NVIDIA RTX 4070 (12 GB) on the human's
> machine. This file lists vetted cloud alternatives for the `experiment-runner`
> agent to fall back to when local GPU is unavailable or when a job exceeds the
> local wall-time budget.

> **GitHub Codespaces does NOT offer GPU.** Verified June 2026 via
> `gh api /repos/<owner>/<repo>/codespaces/machines` — only CPU tiers from
> 2-core to 32-core are available. Do not waste time trying to run experiments
> in Codespaces.

## Decision rule

```
If local RTX 4070 is available AND job wall-time forecast < 24 h:
    use local
ElIf job is pure inference AND fits in 16 GB VRAM:
    prefer Kaggle Notebooks (free, T4 ×2)
ElIf job is short (< 8 h) AND budget-conscious:
    prefer Vast.ai spot (RTX 4090)
ElIf job needs reliability AND > 8 h:
    prefer RunPod on-demand or Modal
Else:
    surface to human for venue decision
```

## Vetted providers

### 0. Kaggle Notebooks — FREE first choice for ≤ 12 h jobs
- 2 × Tesla T4 (16 GB each, 32 GB total)
- 30 hours/week per account, free
- Wall-time per session: 12 hours
- Pre-installed: PyTorch, transformers, bitsandbytes
- **Best for**: Paper 02 inference passes (NIAH, LongBench eval). Each model fits in one T4 at 4-bit.
- Limitation: notebook UI only; no SSH; can be pre-empted.

### 1. Google Colab Pro — $10/month
- T4 / L4 / sometimes A100 (allocation is opportunistic)
- 100 compute units/month included
- **Best for**: Paper 01 if NanoTabPFN must retrain (L4 ≈ 4070 perf)
- Limitation: notebook UI; runtime can be reclaimed

### 2. Vast.ai — cheapest spot market
- RTX 4090 (24 GB) spot: ~$0.30–0.50/hr
- RTX 3090 (24 GB) spot: ~$0.20–0.35/hr
- A100 40GB: ~$0.80/hr
- SSH access; full Linux VM
- **Best for**: Paper 02 inference burst (~30 hrs ≈ $10–15 total)
- Limitation: spot instances can be reclaimed; image quality varies by host

### 3. RunPod — reliable on-demand
- RTX 4090 on-demand: ~$0.55/hr
- A40 (48 GB): ~$0.40/hr
- Serverless or container endpoints
- **Best for**: Paper 01 retraining if it requires > 8 h sustained
- Limitation: pricier than Vast spot

### 4. Lambda Labs — flagship NVIDIA tier
- A10 (24 GB): $0.75/hr
- A100 80GB: ~$1.10/hr on-demand
- **Best for**: nothing in scope unless we ever scale beyond 7B inference

### 5. Modal — Python-native serverless GPU
- A10G (24 GB): ~$0.60/hr (billed per second)
- A100 40GB: ~$1.50/hr
- Trivial to integrate: decorate any Python function with `@app.function(gpu="A10G")`
- **Best for**: parallelising small inference jobs across many GPUs concurrently
- Limitation: pricier per-hour, but per-second billing wins for short jobs

## Cost forecast for this repo (realistic best-case)

| Path | Paper 01 | Paper 02 | Total |
|------|----------|----------|-------|
| Local RTX 4070 (default) | 0 | 0 | $0 |
| Kaggle (free tier) | possible | possible | $0 |
| Vast.ai 4090 spot | ~$5 | ~$15 | ~$20 |
| RunPod on-demand 4090 | ~$8 | ~$22 | ~$30 |
| Modal A10G | ~$10 | ~$25 | ~$35 |

## How the experiment-runner picks

The runner reads this file plus the current job spec from `papers/<id>/plan.md`,
then prints its decision to `papers/<id>/results/runs/<id>/compute-target.txt`
with one of:

```
local-rtx4070
kaggle-t4-x2
vast-4090-spot
runpod-4090-ondemand
modal-a10g
```

If anything other than `local-rtx4070` is chosen, the runner must:

1. Surface the cost forecast to the human before launching.
2. Cache the dataset / weights locally so the cloud run is read-only on the
   storage side.
3. Stream results back to `papers/<id>/results/runs/<id>/` so the local repo
   stays canonical.

## Integration sketches

### Modal (Python-native, cleanest for Modal users)
```python
import modal

app = modal.App("saif-paper-02")
image = modal.Image.debian_slim().pip_install(
    "torch", "transformers", "accelerate", "bitsandbytes"
)

@app.function(gpu="A10G", image=image, timeout=3600, memory=32_000)
def run_attention_export(model_id: str, ctx_len: int) -> dict:
    import torch
    # ... attention export logic ...
    return {"model": model_id, "ctx_len": ctx_len, "...": "..."}

if __name__ == "__main__":
    with app.run():
        results = list(run_attention_export.map(
            [("meta-llama/Meta-Llama-3.1-8B-Instruct", L) for L in [512, 2048, 4096, 8192, 16384]]
        ))
```

### Vast.ai (SSH-style)
```bash
# Provision via vastai CLI
vastai create instance <offer_id> --image pytorch/pytorch:latest --disk 50
# rsync repo
rsync -avz . root@<host>:~/saif-research-lab
# Run remotely
ssh root@<host> 'cd ~/saif-research-lab && python papers/02-attention-sinks-gqa-swa/experiments/scripts/run_attention_export.py'
# rsync results back
rsync -avz root@<host>:~/saif-research-lab/papers/02-attention-sinks-gqa-swa/results/ ./papers/02-attention-sinks-gqa-swa/results/
# Destroy instance to stop billing
vastai destroy instance <id>
```

### Kaggle (notebook-style)
Push a one-cell notebook that `git clone`s the repo, runs the experiment, and
saves results to `/kaggle/working/`. Download the artifact and merge into the
local repo on completion.

## Ethics / data caveats

- Never upload private datasets to public-by-default cloud providers.
- For HuggingFace gated models (e.g., Llama-3.1 requires acceptance), the
  cloud instance must have `HF_TOKEN` set as a runtime secret, not committed.
- For dual-use safety experiments (Paper 02 has no safety angle, but future
  papers may), cloud providers may have their own AUP; check before uploading
  jailbreak datasets.
