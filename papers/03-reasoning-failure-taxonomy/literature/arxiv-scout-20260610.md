# arXiv Scout Report — Paper 03 Reasoning Failure Taxonomy

- **Run timestamp:** 2026-06-10T22:30:00Z
- **Last-run:** none (first run)
- **Paper scanned:** `papers/03-reasoning-failure-taxonomy/`
- **Target contribution checked:** cross-domain taxonomy of reasoning-model failures in professional settings (medicine, law, nuclear safety, financial audit, journalism), with four planned codes: feature hallucination, pattern rigidity, context compression, and confidence miscalibration.

## Candidate papers scanned

### 1. arXiv:2505.12151 — *Reasoning Large Language Model Errors Arise from Hallucinating Critical Problem Features*
- **Authors:** Heyman & Zylberberg
- **Submission date:** 2025-05 (exact day not retrievable from reachable sources)
- **Abstract:** Evaluates contemporary reasoning models including o1/o3-family systems, DeepSeek-R1, Claude thinking-style models, Gemini, and Grok on graph-coloring and related structured reasoning tasks. The central finding is that many errors arise when models invent critical problem features, such as nonexistent graph edges, then reason coherently from those hallucinated premises.
- **Relevance score:** 8/10 — Directly matches paper-03's feature-hallucination failure mode and tests several target reasoning models, but it is limited to synthetic/structured reasoning rather than professional domains.
- **Scoop score:** 35% — Covers one major failure mode and a model set similar to ours, but not a five-domain professional taxonomy, annotation protocol, or calibration heatmap.

### 2. arXiv:2505.23646 — *Are Reasoning Models More Prone to Hallucination?*
- **Authors:** Yao et al.
- **Submission date:** 2025-05-29
- **Abstract:** Studies whether large reasoning models hallucinate more than non-reasoning LLMs and analyzes how post-training choices affect factuality. It reports patterns such as flaw repetition, think-answer mismatch, and uncertainty/factual-accuracy mismatch across reasoning traces.
- **Relevance score:** 6/10 — Important for hallucination and calibration framing, but the paper is about hallucination propensity generally rather than cross-domain professional failure taxonomy.
- **Scoop score:** 30% — Overlaps with hallucination and miscalibration mechanisms, but does not cover paper-03's domain-specific professional comparison.

### 3. arXiv:2504.17550 — *HalluLens: LLM Hallucination Benchmark*
- **Authors:** Yejin Bang, Ziwei Ji, Alan Schelten, Anthony Hartshorn, Tara Fowler, Cheng Zhang, Nicola Cancedda, Pascale Fung
- **Submission date:** 2025-04-24
- **Abstract:** Introduces a hallucination benchmark with a taxonomy distinguishing extrinsic and intrinsic hallucinations, dynamic test generation, and analysis of benchmark saturation. It argues for clearer definitions separating hallucination from general factuality errors.
- **Relevance score:** 6/10 — Strong taxonomy reference for the hallucination axis, but it is not specialized to reasoning models or professional-domain deployment.
- **Scoop score:** 25% — Provides a general hallucination taxonomy, not paper-03's four-mode reasoning-model taxonomy across five high-stakes domains.

### 4. arXiv:2506.02126 — *Knowledge or Reasoning? A Close Look at How LLMs Think Across Domains*
- **Authors:** Juncheng Wu, Sheng Liu, Haoqin Tu, Hang Yu, Xiaoke Huang, James Zou, Cihang Xie, Yuyin Zhou
- **Submission date:** 2025-06 (exact day not retrievable from reachable sources)
- **Abstract:** Examines whether LLM performance across domains reflects true reasoning or primarily domain knowledge. The work contrasts behavior across task families and argues that apparent reasoning gains may not transfer uniformly across domains.
- **Relevance score:** 6/10 — Cross-domain reasoning transfer is relevant, but the focus is knowledge-vs-reasoning decomposition rather than coding failures in professional contexts.
- **Scoop score:** 28% — Touches the cross-domain axis but not the planned failure-mode taxonomy, high-stakes domain set, or confidence-calibration analysis.

### 5. arXiv:2506.10769 — *Mind the Gap: Benchmarking LLM Uncertainty, Discrimination, and Calibration in Specialty-Aware Clinical QA*
- **Authors:** Alberto Testoni, Iacer Calixto
- **Submission date:** 2025-06 (exact day not retrievable from reachable sources)
- **Abstract:** Benchmarks uncertainty and calibration across clinical specialties and question types, showing that calibration quality varies by specialty and use case. It recommends specialty-aware model selection or ensembles for safer clinical deployment.
- **Relevance score:** 5/10 — Useful for paper-03's medical calibration baseline, but it is medicine-only and not specifically about reasoning-model trace failures.
- **Scoop score:** 18% — Covers a subset of H3 in one domain, not the multi-domain taxonomy.

### 6. arXiv:2505.08775 — *HealthBench: Evaluating Large Language Models Towards Improved Human Health*
- **Authors:** Rahul K. Arora, Jason Wei, Rebecca Soskin Hicks, Preston Bowman, Joaquin Quiñonero-Candela, Foivos Tsimpourlas, Michael Sharman, Meghan Shah, Andrea Vallone, Alex Beutel, Johannes Heidecke, Karan Singhal
- **Submission date:** 2025-05 (exact day not retrievable from reachable sources)
- **Abstract:** Presents a large physician-rubric benchmark for evaluating LLMs in health conversations, including hard cases and consensus-style evaluation. It is mainly a medical safety/effectiveness benchmark rather than a mechanistic failure taxonomy.
- **Relevance score:** 4/10 — Good professional-domain context for medicine, but limited overlap with paper-03's reasoning-trace annotation goals.
- **Scoop score:** 12% — Medical benchmark only; no cross-domain taxonomy.

### 7. arXiv:2505.14107 — *DiagnosisArena: Benchmarking Diagnostic Reasoning for Large Language Models*
- **Authors:** [authors not available from reachable sources]
- **Submission date:** 2025-05 (exact day not retrievable from reachable sources)
- **Abstract:** Builds a diagnostic-reasoning benchmark from clinical cases across many specialties and evaluates LLM diagnostic performance. The emphasis is generalization and clinical diagnostic gaps rather than cross-domain error-code comparison.
- **Relevance score:** 4/10 — Relevant as a medical reasoning benchmark, but it does not address legal, financial, nuclear, or journalism domains.
- **Scoop score:** 10% — Supplies possible medical-domain comparison material, not a scoop.

### 8. arXiv:2501.08156 — *Are DeepSeek R1 And Other Reasoning Models More Faithful?*
- **Authors:** James Chua, Owain Evans
- **Submission date:** 2025-01-14
- **Abstract:** Evaluates whether chains of thought from DeepSeek-R1 and other reasoning models faithfully report the factors influencing their answers. It compares reasoning and non-reasoning models on whether prompt cues are reflected in the stated reasoning.
- **Relevance score:** 5/10 — Useful for interpreting reasoning traces, but it is about faithfulness rather than domain-specific failure-mode distribution.
- **Scoop score:** 15% — Informs trace reliability; does not cover paper-03's contribution.

### 9. arXiv:2504.07128 — *DeepSeek-R1 Thoughtology: Let's think about LLM Reasoning*
- **Authors:** Sara Vera Marjanović, Arkil Patel, Vaibhav Adlakha, Milad Aghajohari, Parishad BehnamGhader, Mehar Bhatia, Aditi Khandelwal, Austin Kraft, Benno Krojer, Xing Han Lù, Nicholas Meade, Dongchan Shin, Amirhossein Kazemnejad, Gaurav Kamath, Marius Mosbach, Karolina Stańczak, Siva Reddy
- **Submission date:** 2025-04 (source-reported date inconsistent; arXiv ID confirms April 2025)
- **Abstract:** Analyzes DeepSeek-R1 reasoning traces using a framework for reasoning blocks, rumination, backtracking, safety concerns, and performance regimes. It characterizes how long reasoning chains behave relative to non-reasoning models.
- **Relevance score:** 5/10 — Valuable for trace-level categories such as rumination, but centered on DeepSeek-R1 rather than cross-model professional deployment.
- **Scoop score:** 20% — Provides reasoning-process taxonomy, not paper-03's professional failure taxonomy.

### 10. arXiv:2503.09567 — *Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning Large Language Models*
- **Authors:** Qiguang Chen, Libo Qin, Jinhao Liu, Dengyun Peng, Jiannan Guan, Peng Wang, Mengkang Hu, Yuhang Zhou, Te Gao, Wanxiang Che
- **Submission date:** 2025-03-12
- **Abstract:** Surveys long chain-of-thought methods for reasoning LLMs, including emergence, training strategies, overthinking, evaluation, and open challenges. It frames the broader research landscape around long-CoT systems.
- **Relevance score:** 4/10 — Useful background survey; too broad to threaten novelty.
- **Scoop score:** 8% — Survey background only.

### 11. arXiv:2501.12948 — *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*
- **Authors:** DeepSeek-AI; Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al.
- **Submission date:** 2025-01-22
- **Abstract:** Technical report describing the DeepSeek-R1 training recipe and reinforcement-learning approach that elicits strong reasoning behavior. It documents capabilities and reasoning patterns of a model family included in paper-03's target set.
- **Relevance score:** 3/10 — Model background, not a reliability taxonomy.
- **Scoop score:** 5% — Enables a target model but does not overlap with the proposed study design.

### 12. arXiv:2501.05366 — *Search-o1: Agentic Search-Enhanced Large Reasoning Models*
- **Authors:** Li et al.
- **Submission date:** 2025-01 (exact day not retrievable from reachable sources)
- **Abstract:** Proposes search-augmented reasoning in which external retrieval is invoked during uncertain reasoning steps. The work targets reducing hallucination and improving trustworthiness through dynamic knowledge access.
- **Relevance score:** 3/10 — Relevant mitigation idea, but not a failure taxonomy or cross-domain evaluation.
- **Scoop score:** 6% — Mitigation method only.

### 13. arXiv:2502.03411 — *LLMs vs. Physicians on M-ARC*
- **Authors:** Kim et al.
- **Submission date:** 2025-02 (exact day not retrievable from reachable sources)
- **Abstract:** Evaluates LLMs against physicians on the Medical Abstraction and Reasoning Corpus, focusing on medical reasoning failures and comparison to clinician performance. It is one of paper-03's planned medical-domain anchors.
- **Relevance score:** 5/10 — Directly relevant to the medical benchmark choice, but single-domain and not a reasoning-model taxonomy.
- **Scoop score:** 15% — Covers one input benchmark/domain, not the cross-domain contribution.

## Scoop verdict

**NO SCOOP — proceed.**

No candidate exceeds the 60% scoop threshold. The closest paper, arXiv:2505.12151, covers feature hallucination in reasoning models but not paper-03's defining combination of five professional domains, four failure codes, dual annotation, and confidence-calibration analysis.

## Network source notes

- `web_fetch` to `https://export.arxiv.org/api/query?...` was attempted for: `reasoning model failure modes`, `chain-of-thought failure taxonomy`, `LLM cross-domain evaluation medicine legal`, `o1 deepseek-r1 calibration`, and `reasoning model hallucination`; all attempts failed with `TypeError: fetch failed`.
- `web_fetch` to individual `https://arxiv.org/abs/...` pages also failed with `TypeError: fetch failed`.
- `web_search` was reachable and supplied partial metadata for several papers. Where metadata could not be verified through reachable sources, the report says so explicitly rather than fabricating exact dates/authors.
- Fallback knowledge used: model/paper landscape through 2025–2026 plus repository-provided related IDs in `PAPER_BRIEF.md`.
