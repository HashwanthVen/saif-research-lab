# Reproducibility Checklist

> Before a paper enters `phase: drafting`, every box below must be checked.

## Per-experiment

- [ ] Config YAML committed
- [ ] Git SHA recorded in `results/runs/<id>/commit.txt`
- [ ] Seed recorded in `seed.txt`
- [ ] GPU model + driver recorded in `gpu.txt` (`nvidia-smi --query-gpu=name,driver_version --format=csv`)
- [ ] Library versions recorded in `env.txt` (`pip freeze`)
- [ ] Stdout + stderr logged
- [ ] Metrics JSON committed
- [ ] ≥ 3 seeds for every reported metric
- [ ] 95% CI computed and stored
- [ ] Random-seed sensitivity reported in appendix

## Per-paper

- [ ] All code committed; nothing under `~/scratch/` referenced
- [ ] All datasets either committed (small) or downloadable via a script in `data/fetch.py`
- [ ] `requirements.txt` or `pyproject.toml` pinned to exact versions
- [ ] `scripts/replicate.py` reproduces every table and figure end-to-end
- [ ] README in paper folder describes how to replicate in < 1 page
- [ ] Hardware requirements documented (VRAM, wall time, disk)
- [ ] Any API-based component (e.g., teacher LLM) documented with cost estimate + caching layer

## Pre-submission

- [ ] arXiv submission-ready PDF compiles cleanly
- [ ] Code repo is public (or scheduled to be) at submission time
- [ ] Trained model weights uploaded to Hugging Face (if small enough)
- [ ] Anonymisation pass if venue requires double-blind
