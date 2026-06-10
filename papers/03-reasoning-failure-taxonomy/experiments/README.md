# Paper 03 — Experiments README

## What's here

```
experiments/
├── configs/
│   ├── models.json              ← 10 GHC CLI models (8 active + 2 optional)
│   └── prompts_sample.jsonl     ← 10 starter prompts (2 per domain x 5 domains)
├── scripts/
│   └── eval_runner.ps1          ← deterministic, idempotent, resumable runner
├── src/
│   └── aggregate_results.py     ← runs → CSVs (responses, by-model, stability)
└── tests/                       ← (CPU-only smoke tests, future)
```

## TL;DR — smoke test in 60 seconds

```powershell
# 1. From a regular pwsh terminal (not inside a Copilot session)
cd C:\path\to\saif-research-lab\papers\03-reasoning-failure-taxonomy\experiments\scripts

# 2. Dry run — print the work plan, do nothing
.\eval_runner.ps1 -DryRun

# 3. Single model, single prompt, 1 seed — sanity check
.\eval_runner.ps1 `
    -Models "claude-opus-4.7-high" `
    -Prompts "med-001" `
    -NumSeeds 1

# 4. Aggregate the (single) result
python ..\src\aggregate_results.py `
    --runs-dir ..\..\results\runs `
    --out-dir ..\..\results\tables `
    --prompts ..\configs\prompts_sample.jsonl
```

## Full evaluation matrix

```powershell
# All 10 sample prompts × 8 models × 3 seeds = 240 runs
.\eval_runner.ps1 -Resume

# Resume after Ctrl-C / power outage / any failure
.\eval_runner.ps1 -Resume

# Aggregate
python ..\src\aggregate_results.py `
    --runs-dir ..\..\results\runs `
    --out-dir ..\..\results\tables `
    --prompts ..\configs\prompts_sample.jsonl
```

## Determinism contract

| Invariant | How enforced |
|-----------|--------------|
| Same prompts.jsonl + models.json + seed set → same set of work_ids | `work_id = first16hex(SHA256(prompt_id + \0 + cli_id + \0 + seed))` |
| Idempotent: re-running produces no new files | `-Resume` skips any `<work_id>.json` that already exists |
| LLM sampling is NOT deterministic | We capture `NumSeeds=3` runs per (prompt, model) and measure pairwise Jaccard agreement |
| Aggregation is reproducible | `aggregate_results.py` reads files in sorted order; output is a pure function of input dir |
| Provenance | Every output JSON records: timestamps, machine, user, PS version, CLI invocation string, script version |

## CLI assumptions

The script assumes `copilot -p "<prompt>" --model <cli_id> --no-color` works in your PATH. Override if needed:

```powershell
.\eval_runner.ps1 -CliCommand "C:\Tools\copilot.exe" -PromptArg "--prompt" -ModelArg "-m"
```

If the GHC CLI does NOT accept `--model` as a flag (e.g., requires `/model` slash command in an interactive session), wrap each model invocation in a small wrapper:

```powershell
# wrapper-copilot.ps1
param([string]$p, [string]$model)
$env:COPILOT_MODEL = $model
copilot -p $p --no-color
```

Then run:
```powershell
.\eval_runner.ps1 -CliCommand ".\wrapper-copilot.ps1"
```

## Scaling up beyond the sample

The sample (10 prompts × 8 models × 3 seeds = 240 runs) is for smoke testing. The full paper needs:
- 5 domains × 200 prompts each = 1,000 prompts
- 8 models × 1,000 prompts × 3 seeds = **24,000 runs**

Estimated wall time at ~30 sec/run: ~200 hours. Plan for ~10-14 days of overnight runs, or run on a workstation with the script in the background.

## Outputs

After running + aggregating you get:

```
results/
├── runs/
│   ├── _progress.tsv          ← timeline log
│   ├── <work_id>.json         ← one per (prompt, model, seed)
│   └── ...
└── tables/
    ├── responses.csv          ← one row per run, extracted_answer column ready for analysis
    ├── by_model.csv           ← per (model, domain): n, ok, fail, avg_duration, avg_keyword_hit
    └── response_stability.csv ← per (prompt, model): pairwise Jaccard of seeds
```

`responses.csv` is the canonical artifact for paper figures, hand-annotation, and downstream analysis.

## Hand annotation (next phase, weeks 3–4 in plan.md)

After `responses.csv` exists, 2 human annotators code each failed response into 1+ F-codes (F1 hallucination, F2 pattern rigidity, F3 context compression, F4 confidence miscalibration). See `../../plan.md` Phase 3.

## Cost note

Running against GHC CLI is effectively **$0** for the user (subsumed by GHC seat license). If you ever swap to direct API access, estimated cost for full matrix = ~$1,500-2,000 at 2026 token prices.
