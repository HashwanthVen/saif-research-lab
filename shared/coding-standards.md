# Coding Standards

## Python

- Python 3.11
- Format with `black` (line length 100)
- Lint with `ruff` (default profile)
- Type-hint everything public-facing
- Imports: stdlib → third-party → local, alphabetised within each group
- Module entry-points wrapped in `if __name__ == "__main__":`

## Project layout per `papers/<id>/experiments/`

```
src/                # importable modules (no side effects at import)
scripts/            # entry-points; each one accepts --config <path> and --seed <int>
configs/            # YAML; one file per run; commit alongside the run's output
tests/              # pytest; runnable in < 60 s without GPU
```

## Config-as-code

- Every run is fully described by a single YAML config.
- Configs are committed to the repo before the run starts.
- The run's output folder name embeds the config hash and git sha for trace-back.

## Determinism

```python
import os, random, numpy as np, torch

def set_seed(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

## Logging

- Structured logs via Python `logging`; JSON formatter for files, human format for console.
- Metrics → `results/runs/<run_id>/metrics.json`.
- W&B optional; if used, set `WANDB_MODE=offline` by default.

## Writing style (for the paper-writer agent)

- **Active voice**: "We train" not "It is trained".
- **One claim per sentence.**
- **No empty intensifiers**: avoid "novel", "comprehensive", "extensive", "groundbreaking" unless quantified.
- **Hedge honestly**: "in this setting" is fine; "we believe" is not.
- **Numbers**: always with units. Always with CI when comparing.
- **Citations**: `\citep{Smith2024}` for parenthetical, `\citet{Smith2024}` for inline.
- **Tables**: caption above, source-of-data note below in small font.
- **Figures**: caption is self-contained.

## Ethics

- For any paper touching jailbreaks, safety evaluations, or dual-use methods:
  - The researcher agent must include an ethics section in `PAPER_BRIEF.md`.
  - The senior-reviewer must explicitly sign off at Checkpoint A.
  - Do NOT publish specific high-success attack templates; report aggregated findings only.
  - Defer to HarmBench-style responsible disclosure norms.

## Git hygiene

- Commit message format:
  ```
  <area>: <one-line summary>

  <optional body>

  Co-authored-by: <agent name> <agent>
  ```
- Areas: `paper-01`, `paper-02`, `shared`, `agents`, `ci`, `docs`.
- Branches per phase if changes are large; PR back to `main` with critic-approved diff summary.

## Secrets

- Never commit API keys.
- Use `.env` files locally (in `.gitignore`).
- GitHub Actions: use repo secrets only.
