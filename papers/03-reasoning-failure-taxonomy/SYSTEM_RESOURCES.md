# Paper 03 — System Resources & API Contract

> Quick reference card for the paper agent on what tools / APIs / data sources to use, and how to use them.

## Compute resources

| Resource | Access | Cost | Use for |
|---|---|---|---|
| GitHub Copilot CLI | `copilot -p "<prompt>" --model <id> --no-color` | $0 (seat-included) | All 8 model evaluations |
| Local RTX 4070 (12 GB) | `pwsh` + `python` + `torch` | $0 | Optional: DeepSeek-R1-Distill-Qwen-7B local baseline at 4-bit |
| GitHub Actions | `.github/workflows/` | Free tier | CI status validation, brief linting, nightly arxiv-scout |
| Kaggle Notebooks | Web upload | 30hr T4/wk free | Optional fallback if local GPU unavailable |

**Default for this paper**: GHC CLI only. No GPU needed.

## Data sources

### Existing benchmarks
| Source | URL | License | Status |
|---|---|---|---|
| M-ARC (medical) | request from Kim et al. arXiv:2502.03411 | open via authors | TODO email request |
| CUAD (legal) | https://www.atticusprojectai.org/cuad | CC BY 4.0 | Direct download |
| ClaimBuster (journalism) | https://idir.uta.edu/claimbuster | CC BY-NC 4.0 | Direct download |

### Curated by us
| Name | Source | Method | Target size |
|---|---|---|---|
| **FSAR-Argue** (nuclear) | NRC ADAMS | Argument-completeness Qs from public FSARs | 200 items |
| **EDGAR-Q** (finance) | SEC EDGAR | Regulatory reasoning Qs from 10-K/10-Q risk sections | 200 items |

### Cross-reference
- arXiv API for scoop-watch
- Semantic Scholar (free tier 100 req/5min)
- OpenReview for venue calibration

## Model invocation contract

```powershell
copilot -p "<full prompt text>" --model <cli_id> --no-color
```

### Active models (cli_id)
1. `claude-opus-4.8` (thinking)
2. `claude-opus-4.7-xhigh` (thinking, extra-high reasoning)
3. `claude-opus-4.7-high` (thinking, high reasoning)
4. `claude-opus-4.7` (non-thinking baseline)
5. `claude-sonnet-4.6` (non-thinking mid-tier)
6. `gpt-5.5` (thinking, GPT flagship)
7. `gpt-5.4` (non-thinking GPT baseline)
8. `gemini-3.1-pro-preview` (thinking, Google)

Don't call the CLI directly. Always go through `experiments/scripts/eval_runner.ps1` which provides determinism, idempotency, job-based timeout, and full provenance capture.

## Agent contracts (in `.agents/`)

| File | Use when |
|---|---|
| `orchestrator.md` | Top of every turn |
| `researcher.md` | Literature review, gap analysis, scoop check |
| `critic.md` | Hostile review of any artifact |
| `senior-reviewer.md` | Checkpoint A (pre-experiment) + B (pre-submission) |
| `experiment-runner.md` | Anything touching GHC CLI evaluation |
| `paper-writer.md` | LaTeX manuscript production |
| `peer-reviewer.md` | Mock 3-reviewer panel + AC |
| `rebuttal-author.md` | Author response to mock reviews |
| `arxiv-scout.md` | Weekly scoop-watch (also nightly via Action) |

## Output canonical paths

All relative to `papers/03-reasoning-failure-taxonomy/`:

```
experiments/scripts/eval_runner.ps1 -> results/runs/<work_id>.json
results/runs/*.json -> aggregate_results.py -> results/tables/*.csv
literature/ -> annotated-bibliography.md, sources.bib, scoop alerts, gap analysis
manuscript/ -> main.tex, sections/, abstract.tex, build/main.pdf, REVISIONS.md
reviews/ -> critic-*.md, senior-*.md, peer-*.md
rebuttal/ -> response-*.md, revision-plan.md
status.json -> updated after every phase
orchestrator.log -> one-line per decision
```

## Rate limits and ethics

- **GHC CLI**: ~150 req/min. Back off 30s on errors. Always check exit_code; don't silently skip non-zero
- **Semantic Scholar**: register for API key for 100 req/sec (free)
- **arXiv API**: max 1 req/3s (use `arxiv` Python package — handles this)
- **Ethics**: medical results need disclaimer; nuclear stays on PUBLIC NRC docs only; consider responsible disclosure to AI labs 24-48h before arXiv release

## Time + cost summary

| Phase | Wall-time | Cost |
|---|---|---|
| Literature review | 5-7 days | $0 |
| Benchmark curation | 4-5 days | $0 |
| Eval runs (24,000 calls) | 7-10 days | $0 (GHC) |
| Annotation (2 × 1000 responses) | 10-14 days | $0 if collaborator / $500 Prolific |
| Analysis + figures | 3-5 days | $0 |
| Manuscript draft | 7-10 days | $0 |
| Mock review + rebuttal | 5-7 days | $0 |
| arXiv submission | 1 day | $0 |
| **Total** | **6 weeks** | **$0 (best case) / $500 (Prolific)** |
