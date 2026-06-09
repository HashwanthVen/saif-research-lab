# Paper Template — copy this folder to start a new paper

Copy this folder:

```powershell
Copy-Item -Recurse papers\_template papers\03-your-new-idea
```

Then fill in:

1. `PAPER_BRIEF.md` — replace every section with your paper's content. Run `python scripts/lint_briefs.py` to confirm all required sections are present.
2. `plan.md` — phase-by-phase experimental plan with wall-time and VRAM estimates.
3. `status.json` — set `paper_id`, `target_venue`, `target_deadline`, and initial `scores`.

The orchestrator picks up any `papers/NN-*/` folder with a valid `status.json` automatically. Re-run `python scripts/run_paper.py --report` to confirm your new paper shows up.

## Required files

- `PAPER_BRIEF.md` (must contain all sections listed in `scripts/lint_briefs.py`)
- `plan.md`
- `status.json` (must validate against `scripts/validate_status.py`)

## Required directories (pre-created)

- `literature/`
- `experiments/{configs,src,scripts,tests}/`
- `data/samples/`
- `results/{runs,tables}/`
- `figures/`
- `manuscript/{sections,build}/`
- `reviews/`
- `rebuttal/`
