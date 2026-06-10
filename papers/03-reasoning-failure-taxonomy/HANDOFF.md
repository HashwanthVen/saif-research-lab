# Paper 03 — Cross-Domain Reasoning Model Failure Taxonomy
# AGENT HANDOFF DOCUMENT

> **TL;DR for the paper agent**: You are the orchestrator for an end-to-end paper production from literature review → arXiv preprint → ICLR 2027 submission. The paper has a 6-9 month scoop window. Move fast.

> **Repo**: https://github.com/HashwanthVen/saif-research-lab
> **Paper folder**: `papers/03-reasoning-failure-taxonomy/`
> **Top-level contract**: see `/AGENTS.md` and `.github/copilot-instructions.md` for routing and role definitions

---

## 1. WHAT THIS PAPER IS

A **cross-domain failure taxonomy** for frontier reasoning models (o1, o3, DeepSeek-R1, Claude 3.7 Sonnet Thinking, Gemini 2.5 Pro Thinking, GPT-5.5) evaluated across **5 high-stakes professional domains**: medicine, law, nuclear engineering, finance, and journalism.

Three independent 2025 studies found reasoning models fail in **distinct, domain-specific ways**. No published work unifies them. We do.

**Hypotheses** (full detail in `PAPER_BRIEF.md`):
- **H1**: 4 distinguishable failure modes span all domains: F1 hallucination, F2 pattern rigidity, F3 context compression, F4 confidence miscalibration
- **H2**: Failure-mode dominance is **domain-specific** (medical = rigidity; legal = hallucination; nuclear = compression)
- **H3**: Confidence miscalibration is uniformly high across all domains (ECE > 0.15)

---

## 2. WHY NOW — THE SCOOP CLOCK

- Kim et al. (Feb 2025, arXiv:2502.03411) — medical only
- Heyman & Zylberberg (May 2025) — logical only
- No cross-domain unification as of June 2026

**Multiple frontier lab safety teams (Anthropic, OpenAI, Apollo, METR, ARC Evals) are working in adjacent space.** Estimated window: **6-9 months** before this exact framing is published by someone else.

**Implication**: arXiv preprint within 6 weeks. ICLR 2027 commit Sep 19, 2026.

---

## 3. COMPUTE / API STRATEGY — GHC CLI = $0

The author has GitHub Copilot CLI access with the following models available:

| CLI ID | Display | Tier | Thinking-capable? |
|---|---|---|---|
| `claude-opus-4.8` | Claude Opus 4.8 | frontier | yes |
| `claude-opus-4.7-xhigh` | Claude Opus 4.7 (xHigh reasoning) | frontier | yes |
| `claude-opus-4.7-high` | Claude Opus 4.7 (High reasoning) | frontier | yes |
| `claude-opus-4.7` | Claude Opus 4.7 | frontier | no |
| `claude-sonnet-4.6` | Claude Sonnet 4.6 | mid | no |
| `gpt-5.5` | GPT-5.5 | frontier | yes |
| `gpt-5.4` | GPT-5.4 | frontier | no |
| `gemini-3.1-pro-preview` | Gemini 3.1 Pro | frontier | yes |
| `gemini-3.5-flash` | Gemini 3.5 Flash | mid | no (optional) |
| `claude-haiku-4.5` | Claude Haiku 4.5 | small | no (optional) |

**8 models active** (4 thinking + 4 non-thinking baselines). The 4-thinking vs 4-non-thinking split is the natural control for "does reasoning capability change the failure mode?" — a strong story.

**Cost**: $0 (covered by GHC seat). Compare to ~$1,500-2,000 if using direct APIs.

### Deterministic eval harness — already built

`papers/03-reasoning-failure-taxonomy/experiments/`:

```
experiments/
├── configs/
│   ├── models.json              # 10 GHC models, 8 active
│   └── prompts_sample.jsonl     # 10 seed prompts (2 × 5 domains) — EXPAND to 200/domain
├── scripts/
│   └── eval_runner.ps1          # ★ CANONICAL — deterministic, idempotent, resumable
├── src/
│   ├── aggregate_results.py     # runs/ → responses.csv + by_model.csv + response_stability.csv
│   └── mock_smoke.py            # SMOKE-ONLY cross-platform mock; never invokes a real CLI
└── README.md                    # smoke-test + scale-up instructions
```

> **Hard constraint (do not relax)**: ALL real model evaluation MUST go through `experiments/scripts/eval_runner.ps1` on the Windows host with the GHC CLI. `experiments/src/mock_smoke.py` exists only for cross-platform CI smoke tests of the work-id / build-plan / resume / record-schema logic — it has no `subprocess` import, writes to `results/smoke_runs/` (not `results/runs/`), and every record it produces is self-tagged with `[MOCK]` and `script_version` starting with `mock_smoke.py`. Any output from `mock_smoke.py` is unfit for the manuscript.

**Determinism contract**:
- `work_id = SHA256(prompt_id + "\0" + cli_id + "\0" + seed)[:16]`
- Same input set → same set of work_ids → re-run with `-Resume` skips completed
- LLM sampling is NOT deterministic → script captures `NumSeeds=3` per (prompt, model) and aggregator computes pairwise Jaccard agreement

**Smoke test (1 minute)**:
```powershell
cd papers/03-reasoning-failure-taxonomy/experiments/scripts
.\eval_runner.ps1 -DryRun          # confirm 240-run plan (10 prompts × 8 models × 3 seeds)
.\eval_runner.ps1 -Models "claude-opus-4.7-high" -Prompts "med-001" -NumSeeds 1
```

**Known issue** (paper agent should fix on first run): the `Invoke-CliOnce` function was refactored to use `Start-Job` because the GHC `copilot` binary is a `.ps1` not a `.exe`. The job-based path needs a live end-to-end test on the user's machine. If it errors:
- The output is still captured to `results/runs/<work_id>.json` (even on failure — exit_code will be non-zero)
- Re-run with `-Resume` after fixing
- Fallback: replace `Start-Job` block with direct `& $Cli @args | Tee-Object $tmpFile` if jobs don't cooperate

**Full matrix at scale**: 5 domains × 200 prompts × 8 models × 3 seeds = **24,000 runs**. At ~30 sec/run wall time and serial execution = ~200 hours (~10-14 days of overnight runs). Parallelize 4-way and you're at 2-3 days.

---

## 4. THE FULL LIFECYCLE — ORCHESTRATION

The paper agent should follow `papers/03-reasoning-failure-taxonomy/status.json` and dispatch role-agents from `.agents/`:

```
phase: literature_review     → dispatch .agents/researcher.md
phase: plan_critique         → dispatch .agents/critic.md on plan.md
phase: senior_review_plan    → dispatch .agents/senior-reviewer.md (Checkpoint A)
phase: experimentation       → dispatch .agents/experiment-runner.md
                                 → runs eval_runner.ps1
                                 → runs aggregate_results.py
phase: results_critique      → dispatch .agents/critic.md on results CSVs
phase: drafting              → dispatch .agents/paper-writer.md
phase: mock_peer_review      → dispatch .agents/peer-reviewer.md (3 reviewers + AC)
phase: rebuttal_loop         → dispatch .agents/rebuttal-author.md → paper-writer.md
phase: senior_review_final   → dispatch .agents/senior-reviewer.md (Checkpoint B)
phase: ready_for_submission  → halt, ping human
```

After each phase: update `status.json`, append to `orchestrator.log`, commit with descriptive message.

---

## 5. THE 6-WEEK TIMELINE

| Week | Phase | Output |
|---|---|---|
| **1** | Literature review + benchmark curation | annotated bibliography (30+ papers); curated FSAR-Argue (200 NRC items) + EDGAR-Q (200 SEC items); confirmed scoop check |
| **2** | Plan critique + senior review (A) + GHC eval runs | critic report; senior-reviewer go-decision; 24,000 model responses cached to disk |
| **3** | Hand annotation (round 1) + interim analysis | 2 annotators × 1,000 failed responses coded into F1-F4; Cohen's κ ≥ 0.7 check |
| **4** | Final analysis + figures | 5×5 failure-mode heatmap; calibration curves; CoT trace examples; all CSVs frozen |
| **5** | Manuscript draft + critique loop | 8-10 pg ICLR-style draft; critic pass; revisions |
| **6** | Mock peer review + rebuttal + arXiv submit | 3-reviewer mock + AC meta; rebuttal plan; revision; **arXiv preprint posted** |

After week 6: track ICLR 2027 abstract deadline (~Sep 19, 2026) and EMNLP 2026 Findings via ARR commit (Aug 2, 2026 PAST → next cycle Oct 12).

---

## 6. DATA SOURCES — ALL PUBLIC, NO IRB

| Domain | Benchmark | Source | License | Status |
|---|---|---|---|---|
| Medicine | M-ARC | Kim et al. arXiv:2502.03411 | request from authors | TODO researcher to email |
| Legal | CUAD | atticusprojectai.org/cuad | CC BY 4.0 | Download immediately |
| Nuclear | FSAR-Argue (build it) | NRC ADAMS | public domain | TODO researcher curates 200 items |
| Finance | EDGAR-Q (build it) | sec.gov/edgar | public domain | TODO researcher curates 200 items |
| Journalism | ClaimBuster | idir.uta.edu/claimbuster | CC BY-NC 4.0 | Download immediately |

Sample prompts already seeded at `experiments/configs/prompts_sample.jsonl` (2 per domain). Researcher agent expands each domain to 200 prompts.

---

## 7. FAILURE TAXONOMY — F-CODES

Each failed response is coded with one or more F-codes by 2 independent annotators (Cohen's κ ≥ 0.7 required).

| Code | Name | Definition | Example |
|---|---|---|---|
| **F1** | Feature Hallucination | Asserts a fact not in the prompt | "The patient's creatinine is 2.5" when prompt didn't mention creatinine |
| **F2** | Pattern Rigidity | Applies stereotyped template inappropriately | Recommends standard appendectomy when prompt has contraindications |
| **F3** | Context Compression | Loses info from earlier in the prompt | Forgets the patient's eGFR mentioned at position 1 of 2000 tokens |
| **F4** | Confidence Miscalibration | High stated confidence on wrong answer | Says "I am 95% certain" on incorrect diagnosis |

A response can have multiple F-codes (e.g., F1 + F4 = hallucinated + overconfident).

---

## 8. TARGET VENUES — IMMEDIATE + FORMAL

### 🚀 Immediate public venue: **arXiv (cs.CL or cs.AI)**

This is the venue that locks in scoop priority. Submit as soon as the manuscript draft is critic-approved (week 6). arXiv submission requirements:

1. PDF compiled from `manuscript/main.tex`
2. `metadata.json` with title, abstract, authors, primary category `cs.CL`, cross-list `cs.AI`, `cs.LG`
3. Submit via https://arxiv.org/submit (requires arXiv account; first-time authors need endorsement — request from any prior arXiv author you know)

**Timeline**: Submission → on arXiv within 1 business day. **This is what wins the scoop race.**

### 📍 Formal venue #1: **ICLR 2027 Evaluation track**

- Abstract deadline: **~September 19, 2026** (est.; ICLR pattern)
- Paper deadline: ~September 26, 2026
- Page limit: 9 pages
- Style: ICLR LaTeX template
- Why: Evaluation methodology is welcomed at ICLR; reasoning-model failure modes are squarely in their wheelhouse
- Backup: ICLR 2027 main track if Evaluation track full

### 📍 Formal venue #2: **NeurIPS 2026 D&B Track**

- Abstract deadline: typically May (PAST for 2026) → target NeurIPS 2027
- Or target an existing NeurIPS 2026 workshop (UniReps, Safe Generative AI, MATH-AI) — deadline ~Aug 22, 2026
- Why: D&B accepts evaluation methodology; the failure taxonomy IS a benchmark contribution

### 📍 Formal venue #3 (parallel for medical extension): **The Lancet Digital Health / Nature Medicine Perspective**

- Op-ed-style companion piece focused on the medical-domain finding
- Different audience (clinical practitioners), much higher impact than ML venues alone
- Rolling submission; ~2-3 month turnaround
- Submit ~2 weeks after arXiv to maximize cross-citation

### 📍 Formal venue #4 (safety angle): **TMLR**

- Rolling submission, correctness-gated (no novelty gate)
- Perfect for the rigorous failure-taxonomy framing
- Best fallback if ICLR rejects
- ~6 month review cycle

### Pre-submission checklist (before arXiv)
- [ ] All 4 F-codes have ≥ 80% inter-annotator agreement (Cohen's κ ≥ 0.7)
- [ ] All 5 domains have ≥ 50 fully-annotated responses
- [ ] 5×5 heatmap figure ready
- [ ] Calibration curves figure ready
- [ ] Critic pass complete
- [ ] Senior reviewer (Checkpoint B) approved
- [ ] Open source code repo public + linked in paper
- [ ] Data + annotation guidelines public

---

## 9. WHAT THE PAPER AGENT NEEDS TO DO FIRST

1. **Clone the repo** and read in order:
   - `/AGENTS.md`
   - `/.github/copilot-instructions.md`
   - `/papers/03-reasoning-failure-taxonomy/PAPER_BRIEF.md`
   - `/papers/03-reasoning-failure-taxonomy/plan.md`
   - `/papers/03-reasoning-failure-taxonomy/status.json`
   - This file (`HANDOFF.md`)

2. **Verify the smoke test works on the host**:
   ```powershell
   cd papers/03-reasoning-failure-taxonomy/experiments/scripts
   .\eval_runner.ps1 -DryRun  # should print "240 runs"
   .\eval_runner.ps1 -Models "claude-opus-4.7-high" -Prompts "med-001" -NumSeeds 1
   ```
   If the `Start-Job` path fails, fix `Invoke-CliOnce` to call `copilot.ps1` directly via `& $Cli @args` and re-test.

3. **Dispatch the researcher agent** for literature review + benchmark curation. Allow 1 week.

4. **Dispatch the critic agent** on `plan.md`. Iterate until verdict is "minor revision" or better.

5. **Dispatch the senior reviewer** (Checkpoint A). Decision: `proceed` / `revise-and-recheck` / `abort`.

6. **Scale the eval matrix** to 200 prompts per domain. Run `eval_runner.ps1 -Resume`. Aggregate with `aggregate_results.py`.

7. **Manual annotation** (Phase 3) is the critical-path bottleneck. Schedule it in parallel with later work.

8. **Draft → mock review → rebuttal → arXiv** in weeks 5-6.

---

## 10. RISKS — KEEP MONITORING

| Risk | Mitigation |
|---|---|
| 🔴 Scoop in next 6 months | arXiv weekly scan via `.agents/arxiv-scout.md`; halt + alert if >60% overlap detected |
| 🔴 Contamination of benchmarks | FSAR-Argue and EDGAR-Q are curated post-training-cutoff specifically to defend |
| 🟡 Annotator agreement < κ=0.7 | Budget 1 extra week for rubric refinement; consider 3rd annotator on disagreements |
| 🟡 GHC CLI flag changes mid-experiment | Pin a CLI version; document in env.txt; re-run any affected work_ids |
| 🟡 Rapid model upgrades | Lock model evaluation to specific dated CLI version |

---

## 11. WHEN IT'S DONE

The paper agent halts and surfaces to human when ANY of:
- `status.json.phase == "ready_for_submission"` — pings human for final go-ahead
- Critic verdict "fundamentally flawed" two passes in a row
- Mock peer-reviewer overall score < 4/10
- Scoop alert detected (>60% overlap)
- Compute budget exhausted with no result

For final submission to arXiv: human pushes the "submit" button. For ICLR: human confirms commitment at ARR cycle.

---

## 12. ARTIFACTS THE AGENT WILL PRODUCE

```
papers/03-reasoning-failure-taxonomy/
├── PAPER_BRIEF.md          ← canonical paper definition (DONE)
├── plan.md                 ← 6-week experimental plan (DONE)
├── status.json             ← machine-readable state (DONE)
├── HANDOFF.md              ← this file (DONE)
├── orchestrator.log        ← (created by orchestrator)
├── literature/
│   ├── annotated-bibliography.md  ← (researcher agent)
│   ├── gap-analysis.md            ← (researcher agent)
│   ├── sources.bib                ← (researcher agent)
│   └── arxiv-scout-*.md           ← (weekly scoop alerts)
├── experiments/             ← (DONE scaffold; agent extends prompts to 200/domain)
├── results/
│   ├── runs/<work_id>.json        ← (eval_runner.ps1)
│   ├── tables/responses.csv       ← (aggregate_results.py)
│   ├── tables/by_model.csv        ← (aggregate_results.py)
│   └── tables/response_stability.csv
├── figures/
│   ├── failure_mode_heatmap.pdf   ← 5×5 model × domain
│   ├── calibration_curves.pdf
│   └── cot_failure_examples.pdf
├── manuscript/
│   ├── main.tex                   ← paper-writer agent
│   ├── sections/                  ← per-section drafts
│   ├── abstract.tex
│   ├── build/main.pdf             ← compiled
│   └── REVISIONS.md
├── reviews/
│   ├── critic-*.md                ← critic agent
│   ├── senior-A-*.md              ← senior reviewer Checkpoint A
│   ├── peer-R1/R2/R3-*.md         ← peer reviewer agent
│   ├── peer-meta-*.md             ← AC voice
│   └── senior-B-*.md              ← Checkpoint B
└── rebuttal/
    ├── response-R1/R2/R3-*.md
    ├── response-meta-*.md
    └── revision-plan.md
```

---

## 13. WHAT MAKES THIS PAPER WORTH SHIPPING

It directly addresses the **2026 deployment crisis**: reasoning models are being put into production in clinical decision support, legal research, nuclear engineering review, financial audit, and journalism fact-checking — five domains where being wrong matters in human lives, money, or institutional trust.

A unified failure taxonomy:
- Becomes the **canonical reference** every clinical AI deployment guideline, every legal-tech vendor risk assessment, every nuclear-engineering AI policy document cites for the next 2-3 years.
- Provides **immediate, actionable knowledge** for practitioners: "in your domain, the failure mode that will burn you is X — here is what to monitor."
- Establishes a methodology that future reasoning models can be evaluated against.
- Companion publications in *Lancet Digital Health* / *Nature Medicine* compound the citations beyond ML.

If it ships within 6 weeks at $0 marginal cost, the cost-adjusted impact is extraordinary. Go.
