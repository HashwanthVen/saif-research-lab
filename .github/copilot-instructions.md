# GitHub Copilot Coding Agent — Entry Instructions

> Read these instructions before reading any other file. Then read `AGENTS.md` at the repo root.

## What this repo is

A multi-paper research lab. Each `papers/NN-*/` folder is one research paper being driven through its lifecycle by a swarm of specialist agents whose roles are defined in `.agents/`.

## Your job as the coding agent

You are the **runtime** that hosts the specialist agents. For every user request that does not specify otherwise:

1. Read `AGENTS.md` (top-level contract).
2. List all `papers/NN-*/status.json` files and find the paper that needs work next.
3. Read its `PAPER_BRIEF.md` and `status.json`.
4. Dispatch the agent role matching `status.json.phase` (use the prompt in `.agents/<role>.md` verbatim).
5. After the agent finishes, update `status.json` and append a one-line entry to `papers/<id>/orchestrator.log`.
6. Commit changes with a descriptive message; PR if requested.

## Parallel paper execution

Multiple papers are processed by spawning one orchestrator per paper. They share `shared/` and `.agents/` but never touch each other's `papers/<id>/` directory. If both papers want the GPU at the same time, serialise by paper id (lower first).

## Tool preferences (host-specific)

- For file work: built-in editor tools.
- For shell: PowerShell on Windows, bash on Linux. Use the entrypoint `python scripts/run_paper.py <id>` to drive a single paper non-interactively.
- For web research: prefer `web_fetch` / browser tools; fall back to `curl`.
- For arXiv: use the `arxiv` Python package or arXiv API HTTP.
- For LLM API calls (when an agent needs to delegate to a strong model): respect `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` env vars.

## Sub-agent invocation pattern

If your host supports sub-agents (Copilot Coding Agent, Claude Code with `Task`, etc.):

```
Task(
  agent_type: "general-purpose",
  prompt: "<contents of .agents/<role>.md> + concrete inputs for <papers/<id>>",
  mode: "background",
)
```

Otherwise, simulate by adopting the role prompt as a system message in your own context for one turn at a time.

## Status-file invariants

- `phase` is one of: `literature_review | plan_critique | senior_review_plan | experimentation | results_critique | drafting | mock_peer_review | rebuttal_loop | senior_review_final | ready_for_submission | submitted | parked`
- `last_updated` is an ISO-8601 UTC timestamp
- `scoop_alerts` is an array; non-empty → pause and surface to human
- `blockers` is an array of human-readable strings; non-empty → cannot advance
- `scores.weighted_total` < 6.5 → re-evaluate

## Halt conditions — surface to human immediately

- Scoop detected (> 60% overlap with a new arXiv paper)
- Critic verdict `fundamentally flawed` twice in a row
- Peer-reviewer overall score < 4/10
- Compute budget exhausted with no result
- Ethics concern raised

## Do not

- Do not invent experimental results.
- Do not skip the critic.
- Do not exceed the compute envelope.
- Do not commit secrets.
- Do not push directly to main without a critic-approved diff summary in the commit message.

## Default behaviour when the user just hands you the repo link

If the user gives you only the repo link with no further direction, do exactly this:

1. Clone the repo (if not already local).
2. `python scripts/run_paper.py --all --report` → prints a status table for every paper.
3. Pick the paper with the earliest next deadline (`status.json.target_deadline`).
4. Begin its current phase.
5. After one full phase, report back to the user with a summary and ask whether to continue.
