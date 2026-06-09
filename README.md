# Saif Research Lab — Multi-Agent Paper Production Pipeline

> One repository. Multiple papers. A small swarm of specialised AI agents that take each paper from idea → arXiv → peer review → rebuttal — fully runnable on a single NVIDIA RTX 4070 (12 GB).

## What this is

A plug-and-play scaffold designed for a **coding agent** (GitHub Copilot Coding Agent, Claude Code, Cursor, Codex, or any AGENTS.md-aware tool) to pick up the repository, read the agent registry in `.agents/`, and autonomously drive multiple research papers in parallel.

Inspired by [Sakana AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2) and [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory), but optimised for:
- **Single consumer GPU** (RTX 4070, 12 GB VRAM)
- **Solo independent researcher** workflow
- **Balanced-reputation venues** (TMLR, COLM, ACL Findings, NeurIPS workshops, BMVC, WACV)
- **Multiple papers in parallel** — clean per-paper folders under `papers/`, shared agent contracts under `.agents/`

## Repository layout

```
saif-research-lab/
├── AGENTS.md                          # Top-level agent contract (read first by any coding agent)
├── README.md                          # This file
├── .agents/                           # Subagent role definitions (markdown prompts)
│   ├── orchestrator.md                # Coordinates the others
│   ├── researcher.md                  # Literature review, gap analysis
│   ├── critic.md                      # Hostile internal review
│   ├── senior-reviewer.md             # Domain expert sanity check
│   ├── experiment-runner.md           # Writes & runs PyTorch code on the 4070
│   ├── paper-writer.md                # LaTeX manuscript production
│   ├── peer-reviewer.md               # Mock peer review (3 reviewers)
│   ├── rebuttal-author.md             # Responds to reviewer comments
│   └── arxiv-scout.md                 # Daily arXiv scan for related work
├── .github/
│   ├── copilot-instructions.md        # GitHub Copilot Coding Agent entrypoint
│   └── workflows/
│       ├── paper-pipeline.yml         # CI on each push to papers/*
│       └── arxiv-watch.yml            # Nightly arXiv scout
├── shared/
│   ├── rubric.md                      # Idea / paper scoring rubric
│   ├── venue-calendar.md              # Live deadline tracker
│   ├── compute-envelope.md            # Exact hardware constraints
│   ├── coding-standards.md
│   └── reproducibility-checklist.md
├── papers/
│   ├── 01-latent-cot-tabular/         # Paper #1
│   │   ├── PAPER_BRIEF.md             # Hypothesis, plan, target venue (READ ME FIRST)
│   │   ├── plan.md
│   │   ├── status.json                # Machine-readable state for orchestrator
│   │   ├── literature/                # Annotated bibliography
│   │   ├── experiments/               # Code, configs, runs
│   │   ├── data/                      # Datasets (gitignored except metadata)
│   │   ├── results/                   # Raw + processed outputs
│   │   ├── figures/                   # Generated figures
│   │   ├── manuscript/                # LaTeX + markdown drafts
│   │   ├── reviews/                   # Mock peer reviews
│   │   └── rebuttal/                  # Author responses
│   └── 02-attention-sinks-gqa-swa/    # Paper #2 (same structure)
└── scripts/
    ├── run_paper.py                   # Orchestrator entrypoint: python scripts/run_paper.py 01
    └── setup.ps1                      # Windows env bootstrap
```

## Quickstart — hand this repo to a coding agent

Tell your coding agent:

> *"Read `AGENTS.md` and `.github/copilot-instructions.md`, then drive `papers/01-latent-cot-tabular` and `papers/02-attention-sinks-gqa-swa` in parallel through their full lifecycle. Update `status.json` after every phase. Target venues and deadlines are in `shared/venue-calendar.md`."*

The agent will:
1. Read `papers/<id>/PAPER_BRIEF.md` for hypothesis and scope.
2. Dispatch the **researcher** agent for literature review.
3. Hand findings to the **critic** for hostile review.
4. Loop back to **researcher** until critic is satisfied.
5. Dispatch the **experiment-runner** with a precise experimental plan.
6. The **senior-reviewer** spot-checks experimental design before any GPU time is burned.
7. After results, the **paper-writer** drafts the manuscript.
8. The **peer-reviewer** runs a mock 3-reviewer panel.
9. The **rebuttal-author** addresses each weakness; loop back to paper-writer.
10. When `status.json.ready_for_submission == true`, the orchestrator stops and asks the human for the final go-ahead.

## Running a single paper locally

```powershell
# from repo root
python scripts/run_paper.py 01   # drives paper 01 through the full lifecycle
python scripts/run_paper.py 02   # in another shell, parallel
```

## Adding paper #3, #4, #N

```powershell
cp -r papers/_template papers/03-your-new-idea
# edit papers/03-your-new-idea/PAPER_BRIEF.md
```

The orchestrator picks up any new `papers/NN-*` folder automatically.

## Hardware

- GPU: NVIDIA RTX 4070 (12 GB VRAM, Ada Lovelace)
- See `shared/compute-envelope.md` for the exact model-size / training-mode envelope every agent must respect.

## License

MIT — see `LICENSE`.

## Acknowledgements

- [Sakana AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2) — agentic tree-search ideation
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) — 3-phase research workflow
- [Anthropic Claude Code](https://github.com/anthropics/claude-code), [GitHub Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/about-copilot-coding-agent) — runtime orchestration
