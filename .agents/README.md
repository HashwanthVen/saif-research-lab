# `.agents/` — Agent Registry

This directory holds the role prompts for every specialist agent the orchestrator can dispatch. Each file is a self-contained system prompt + tool contract that any LLM-backed coding agent (Copilot Coding Agent, Claude Code, Cursor, Codex, Devin, AutoGen, CrewAI, LangGraph, etc.) can load.

## Roles

| File | Purpose | Typical input | Typical output |
|------|---------|---------------|----------------|
| `orchestrator.md` | Top-level coordinator | `papers/<id>/status.json` | Updated status, dispatched subagent calls |
| `researcher.md` | Literature review + gap analysis | Paper brief | Annotated bibliography under `literature/` |
| `critic.md` | Hostile internal review | Any artifact | Markdown critique under `reviews/critic-*.md` |
| `senior-reviewer.md` | Domain-expert sanity check before expensive ops | Plan / pre-submission draft | Go / no-go decision with reasoning |
| `experiment-runner.md` | PyTorch / HF code + GPU execution | Experimental spec | Code under `experiments/`, results under `results/` |
| `paper-writer.md` | Manuscript drafting | Results + outline | LaTeX / markdown under `manuscript/` |
| `peer-reviewer.md` | Mock 3-reviewer panel | Final draft | Reviewer 1/2/3 + meta-review under `reviews/` |
| `rebuttal-author.md` | Author response | Reviews | Rebuttal under `rebuttal/` |
| `arxiv-scout.md` | Daily scoop detection | Paper brief | Scoop alerts in `status.json.scoop_alerts` |

## How to invoke an agent (from any coding-agent host)

Each file is a markdown document with these sections:

1. `## Role` — one-paragraph identity
2. `## Inputs` — what files / variables the agent expects
3. `## Outputs` — what it must produce, where it must write
4. `## System Prompt` — the literal prompt to feed the LLM
5. `## Tools` — minimal toolset (read/write/grep/web/python/gpu)
6. `## Stop Conditions` — when the agent must hand control back
7. `## Anti-patterns` — things never to do

Most coding-agent runtimes already understand `AGENTS.md`-style files. For Claude Code: drop these into `.claude/agents/`. For Cursor: load via `.cursor/rules/`. For Copilot Coding Agent: they are auto-discovered when referenced from `.github/copilot-instructions.md`.

## Authoring conventions

- Be specific. Each role gets a single page; no aspirational fluff.
- Always reference shared docs (`shared/rubric.md`, `shared/compute-envelope.md`) instead of duplicating.
- Always require the agent to update `papers/<id>/status.json` at the end of its turn.
