# Venue Strategy for Paper 03

## Decision tree

```
Manuscript draft ready
        |
        v
+--------------------+
| Critic pass clean? |
+--------------------+
        |
        v (yes)
+--------------------------+
| Senior reviewer (B): GO  |
+--------------------------+
        |
        v
+--------------------------------+
| arXiv cs.CL + cross cs.AI/LG   |  <- SUBMIT FIRST (scoop priority)
+--------------------------------+
        |
        v
+---------------------+    +---------------------+
| Within 2 weeks:     |    | Within 2 weeks:     |
| - ICLR 2027 abstract|    | - Lancet Digital    |
|   (Sep 19, 2026)    |    |   Health perspective|
+---------------------+    |   companion piece   |
        |                  +---------------------+
        v
+--------------------------+
| ICLR 2027 paper full     |
| (Sep 26, 2026)           |
+--------------------------+
        |
        v
        If accepted -> ICLR 2027 (Apr 2027 conf)
        If rejected -> TMLR (rolling) AND
                       NeurIPS 2027 D&B (May 2027)
```

## Venue scorecard

| Venue | Tier | Fit | Speed to public | Accept rate | Prestige |
|---|---|---|---|---|---|
| **arXiv cs.CL** | Preprint | 10/10 | <1 day | 100% | n/a (priority claim) |
| **ICLR 2027 Evaluation** | Main | 10/10 | ~8 months | ~30% | A* |
| **TMLR** | Journal | 9/10 | ~6 months | ~50% | A (rising) |
| **NeurIPS 2027 D&B** | Main | 9/10 | ~12 months | ~30% | A* |
| **Lancet Digital Health** (medical companion) | Journal | 8/10 (one domain) | ~3 months | ~25% | A (cross-disciplinary) |
| **EMNLP 2026 Findings** (via ARR Oct 12 cycle) | Findings | 7/10 | ~6 months | ~40% | A* (Findings = A) |
| **NeurIPS 2026 UniReps/Safe-GenAI workshop** | Workshop | 7/10 | ~3 months | ~45% | Workshop |

## arXiv submission packaging

### Required files
- `manuscript/build/main.pdf`
- `manuscript/main.tex` + all `.sty`, `.cls`, `.bib` dependencies (arXiv compiles from source)
- `manuscript/figures/*.pdf` (referenced, not embedded)

### arXiv metadata template
```yaml
title: "Cross-Domain Failure Modes of Frontier Reasoning Models in High-Stakes Professional Contexts"
authors:
  - "Hashwanth Sutharapu (independent researcher)"
primary_category: cs.CL
cross_lists: [cs.AI, cs.LG]
abstract: |
  Reasoning models (o1, o3, DeepSeek-R1, Claude 3.7 Sonnet Thinking, Gemini 2.5
  Pro Thinking, GPT-5.5) are being deployed in clinical decision support, legal
  research, nuclear safety review, financial audit, and journalism fact-checking.
  Three independent studies have documented domain-specific failures, but no
  unified cross-domain taxonomy exists. We evaluate 8 frontier reasoning and
  baseline models across 5 high-stakes professional domains with a 4-mode failure
  taxonomy (feature hallucination, pattern rigidity, context compression,
  confidence miscalibration). Across 24,000 graded responses, we find that (1)
  failure mode dominance is domain-specific not model-specific, (2) reasoning
  capability reduces some failure modes while exacerbating others, and (3)
  confidence miscalibration is uniformly high across all domains. We release a
  reusable evaluation harness, two new domain benchmarks (FSAR-Argue, EDGAR-Q),
  and per-domain practitioner deployment guidance.
comments: "16 pages, 5 figures, 4 tables. Code: https://github.com/HashwanthVen/saif-research-lab"
```

### arXiv submission process
1. Create arXiv account if first-time (https://arxiv.org/user/register)
2. First-time authors need endorsement in cs.CL — request from any prior arXiv author you know (mention this paper)
3. Submit at https://arxiv.org/submit
4. Choose "Replace this article" workflow only if updating an existing arXiv ID
5. Goes live within 1 business day after moderation

## ICLR 2027 Evaluation track submission

### Timing
- **Abstract**: ~September 19, 2026 (estimated from ICLR pattern)
- **Paper**: ~September 26, 2026
- **Notification**: ~January 2027
- **Conference**: ~April 2027

### Required
- 9 pages main text + unlimited references
- Use ICLR LaTeX template (https://github.com/ICLR/Master-Template)
- OpenReview account; submission via openreview.net
- Authors: identity revealed at submission (single-blind for 2026+)

### Reviewer profile
- 3 reviewers + AC
- Soundness 1-4, Presentation 1-4, Contribution 1-4, Overall 1-10, Confidence 1-5
- Anchor reviewers care about: (a) novelty of evaluation, (b) rigor of methodology, (c) actionability of findings, (d) reproducibility

## EMNLP 2026 Findings via ARR (parallel path)

- **ARR cycle**: October 12, 2026 (next cycle after our 6-week timeline)
- **EMNLP commit deadline**: depends on ARR review window
- **Best for**: securing a Findings paper as insurance if ICLR doesn't land
- **Page limit**: 8 + 4 (long format)
- Use ACL template

## Lancet Digital Health companion piece

### When
2 weeks after arXiv submission, once medical-domain results are validated.

### Format
- ~3000 word Perspective / Comment
- 30-50 references
- 1-2 figures (subset of paper figures, simplified for clinical audience)
- Co-author opportunity: invite a clinician collaborator for credibility

### Why it matters
- Clinical practitioners read Lancet, not ICLR
- Citations from this venue compound paper visibility 3-5x
- "Cited by NHS deployment guideline" carries policy weight ICLR doesn't

## Fallback ladder if primary venues reject

```
ICLR 2027 reject -> TMLR (start parallel during ICLR review, can co-exist on arXiv)
                  -> NeurIPS 2027 D&B (May 2027 deadline)
                  -> EACL 2027 (Oct 2026 commit)
                  -> ARR Dec 2026 -> ACL 2027
```

## Whatever you do — preserve arXiv priority

arXiv timestamp is what wins the scoop race. Even if no formal venue takes it, the arXiv preprint is the citation-attracting artifact and the proof of first-publication.

## Author affiliation

For arXiv: list as "independent researcher" or include institutional affiliation if applicable. For ICLR/TMLR: same. For Lancet companion: needs a clinician co-author with institutional affiliation (IRB and citation norms).
