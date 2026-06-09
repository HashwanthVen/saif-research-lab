# Venue Calendar (live)

> Current as of June 9, 2026. The arXiv-scout / human should refresh this monthly.

## Primary target venues for this lab

| Venue | Tier | Accept rate | Next deadline | Page limit | Template | Notes |
|-------|------|-------------|---------------|------------|----------|-------|
| **TMLR** | Journal | ~50–55% | Rolling (pause Dec) | Flexible (8–25 pp) | [TMLR style](https://github.com/JmlrOrg/jmlr-style-file) | Correctness-gated, not novelty. Best for solo / limited-compute work. |
| **ARR → EMNLP 2026 Findings** | Findings | ~35–45% | Aug 2, 2026 (commit) | 8 / 4 pp | [ACL style](https://github.com/acl-org/acl-style-files) | Via ARR May cycle. Low-compute explicitly welcome. |
| **ARR → EACL 2027** | Findings | ~35–45% | Oct 11, 2026 (commit) | 8 / 4 pp | ACL style | Via ARR Aug cycle. European venue, less crowded. |
| **NeurIPS 2026 Workshops** | Workshop | 30–50% | ~Aug 22, 2026 | 4–8 pp | NeurIPS style | UniReps, ATTRIB, ENLSP, Safety, MATH-AI — all friendly to small-GPU work. |
| **ICLR 2027 Main** | Main | ~28–32% | ~Sep 19, 2026 (abstract est.) | 9 pp | ICLR style | Hard but no lab bias. |
| **COLM 2027** | Main | ~28–30% | ~Mar 2027 (est.) | 9 pp | COLM style | Perfect for LM / efficiency / interp work. |
| **WACV 2027** | Main | ~40–45% | Round 1 Jun–Aug 2026 (est.) | 8 pp | CVPR style | Best CV entry point. CORE A. |
| **BMVC 2026** | Main | ~35–40% | Jun–Jul 2026 (est.) | 9 pp | BMVC style | CORE A. No rebuttal in 2025 edition. |
| **AAAI-27 Student Abstract** | Special | ~55–65% | Oct–Nov 2026 (est.) | 2 pp | AAAI style | If you have student status. Quick poster CV line. |
| **ICLR 2027 Blogpost Track** | Special | ~40–50% | Aug–Oct 2026 (est.) | Blog | Markdown | No compute needed. Underrated CV line. |

## Reviewing-form conventions

| Venue | Form |
|-------|------|
| TMLR | Action editor + 3 reviewers; binary `accept/reject` after revision rounds; no scores, just claims |
| ARR / ACL family | Soundness 1–4, Excitement 1–4, Confidence 1–5, Overall accept tier |
| NeurIPS / ICML | Soundness, Presentation, Contribution each 1–4; Overall 1–10; Confidence 1–5 |
| ICLR | Soundness 1–4, Presentation 1–4, Contribution 1–4, Rating 1–10, Confidence 1–5 |
| BMVC | Confidence 1–5, Recommendation Strong Reject → Strong Accept |
| WACV | Similar to CVPR: Overall recommendation, Confidence 1–5 |
| COLM | Overall score 1–10, Confidence 1–5, structured strengths/weaknesses |

## Submission templates

Each paper folder should pull the matching LaTeX template into `manuscript/templates/`. The paper-writer agent looks here first.

## Status flags

- ✅ Open and accepting submissions
- ⏳ Window closed but still actionable via rolling submission / next cycle
- 🔴 Past — for reference only

## Deadlines snapshot (this month)

- **Aug 2, 2026** (8 weeks) — EMNLP 2026 commitment
- **Aug 3, 2026** (8 weeks) — ARR August cycle
- **Aug 22, 2026** (10 weeks) — NeurIPS workshop estimated
- **Sep 19, 2026** (14 weeks) — ICLR 2027 abstract estimated
- **Oct 11–12, 2026** (18 weeks) — EACL 2027 commit / ARR October cycle

## When to pick which venue

```
Is it primarily NLP / LMs?
├─ Yes → ARR → EMNLP Findings (fast) or COLM 2027 (LM-focused) or TMLR (rolling)
└─ No → Is it CV?
        ├─ Yes → WACV 2027 (R1 ~Aug 2026) or BMVC 2026 (~Jul 2026)
        └─ No → TMLR (default) or NeurIPS/ICML workshops (if topic-fit)
```
