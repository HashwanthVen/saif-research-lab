# Annotated bibliography — Paper 03: Cross-domain reasoning-model failure taxonomy

Scope note: network access was limited. I used training-data knowledge through 2025--2026 plus a small live check where available. Entries marked `[UNVERIFIED — researcher to confirm citation key/year]` require metadata confirmation before camera-ready use. I did not find a >60% scoop: the closest works evaluate a single domain, a single failure type, or general safety rather than a cross-domain taxonomy across medicine, law, nuclear review, finance, and journalism.

## A. Reasoning-model evaluation

### `kim2025marc`
**Citation.** Kim et al. (2025). *LLMs vs. Physicians on M-ARC / Medical Abstraction and Reasoning Corpus*. arXiv:2502.03411. [UNVERIFIED — researcher to confirm author list/year]

**Summary.** Introduces or evaluates M-ARC as a medical abstraction/reasoning benchmark and compares LLMs or reasoning models against physician baselines. The paper is central for the medical slice of this project because it motivates that high benchmark accuracy can mask clinically meaningful reasoning errors. It appears domain-specific rather than a cross-domain failure taxonomy.

**Relevance quote.** [paraphrased from abstract] The benchmark evaluates medical abstraction and reasoning rather than simple factual recall.

**relationship:** adjacent

### `heyman2025graphhallucination`
**Citation.** Heyman and Zylberberg (2025). *Reasoning Models Hallucinate Graph Edges*. arXiv ID TBD. [UNVERIFIED — researcher to confirm citation key/year]

**Summary.** Reported in project materials as a 2025 study of graph/logical reasoning failures in reasoning models. Its key relevance is a fine-grained failure phenomenon: models invent graph edges or relational structure not present in the input. That is a close analogue of our F1 feature hallucination code, but outside professional-domain deployment.

**Relevance quote.** [paraphrased from abstract / project handoff] Reasoning models can hallucinate graph edges during structured logical reasoning.

**relationship:** adjacent

### `srivastava2023bigbench`
**Citation.** Srivastava et al. (2023). *Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models*. Transactions on Machine Learning Research.

**Summary.** BIG-bench collects many tasks intended to probe general language-model capabilities, including tasks associated with reasoning and robustness. It gives a precedent for broad evaluation and task aggregation. It does not provide professional-domain failure coding or trace-level failure categories.

**Relevance quote.** [paraphrased from abstract] The benchmark is designed to probe and quantify language-model capabilities across a broad suite of tasks.

**relationship:** foundational

### `hendrycks2021mmlu`
**Citation.** Hendrycks et al. (2021). *Measuring Massive Multitask Language Understanding*. International Conference on Learning Representations.

**Summary.** MMLU is an influential multitask evaluation suite covering many academic and professional subjects. It establishes that broad, domain-mixed benchmarks are valuable for capability estimation. Its multiple-choice accuracy framing does not diagnose why high-stakes reasoning fails.

**Relevance quote.** [paraphrased from abstract] The benchmark measures knowledge acquired during pretraining by evaluating models across many subjects.

**relationship:** foundational

### `cobbe2021gsm8k`
**Citation.** Cobbe et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv:2110.14168.

**Summary.** Introduces GSM8K and verifier-based evaluation for multi-step arithmetic word problems. It is foundational for reasoning evaluation because it helped popularize step-by-step answer verification and chain-of-thought-style scoring. It is not a professional-domain reliability study.

**Relevance quote.** [paraphrased from abstract] The dataset consists of grade-school math word problems requiring multi-step reasoning.

**relationship:** foundational

### `zellers2019hellaswag`
**Citation.** Zellers et al. (2019). *HellaSwag: Can a Machine Really Finish Your Sentence?* ACL.

**Summary.** HellaSwag tests commonsense inference and adversarially filtered endings. Its importance is methodological: models can succeed on superficial patterns yet fail when adversarial filtering changes distributional cues. Pattern-rigidity in our taxonomy has a similar motivation, but in professional tasks.

**Relevance quote.** [paraphrased from abstract] The benchmark is designed to be trivial for humans yet challenging for state-of-the-art models through adversarial filtering.

**relationship:** foundational

## B. Domain-specific failure studies — medical / legal / nuclear / financial / journalism

### `jin2021diseaseqa`
**Citation.** Jin et al. (2021). *Disease Question Answering over Medical Knowledge Graphs / MedQA*. [UNVERIFIED — researcher to confirm exact title and venue]

**Summary.** MedQA-style medical QA benchmarks test medical examination and clinical knowledge reasoning. They are often used to evaluate clinical LLM performance and reveal that medical correctness involves more than factual recall. For our work, they support the need for domain-specific medical error analysis but do not classify cross-domain failure modes.

**Relevance quote.** [paraphrased from abstract] The dataset evaluates medical question answering requiring professional medical knowledge.

**relationship:** adjacent

### `pal2022medmcqa`
**Citation.** Pal, Umapathi, and Sankarasubbu (2022). *MedMCQA: A Large-scale Multi-Subject Multi-Choice Dataset for Medical Domain Question Answering*. Conference on Health, Inference, and Learning / arXiv. [UNVERIFIED — researcher to confirm venue]

**Summary.** MedMCQA provides large-scale multiple-choice medical questions spanning many medical subjects. It is useful as background for medical-domain evaluation and for contrasting accuracy benchmarks with failure-mode annotation. It does not target reasoning-model traces or confidence calibration.

**Relevance quote.** [paraphrased from abstract] MedMCQA is a large-scale multi-subject medical question-answering dataset.

**relationship:** adjacent

### `nori2023gpt4medicine`
**Citation.** Nori et al. (2023). *Capabilities of GPT-4 on Medical Challenge Problems*. arXiv:2303.13375.

**Summary.** Studies GPT-4 performance on medical challenge questions and discusses strengths and limitations of LLMs in clinical-style reasoning. It is directly relevant to the risk of using general LLMs in medicine. The work is not a reasoning-model-specific, five-domain failure taxonomy.

**Relevance quote.** [paraphrased from abstract] GPT-4 attains strong performance on medical challenge problems but evaluation is needed before clinical use.

**relationship:** adjacent

### `hendrycks2021cuad`
**Citation.** Hendrycks, Burns, Chen, and Ball (2021). *CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review*. NeurIPS Datasets and Benchmarks.

**Summary.** CUAD provides expert-annotated legal contract review tasks. It anchors the legal benchmark choice in this project and is valuable for studying legal feature hallucination, because answers must be grounded in contract clauses. CUAD itself is a dataset paper rather than a reasoning-model failure taxonomy.

**Relevance quote.** [paraphrased from abstract] CUAD is an expert-annotated dataset for legal contract review.

**relationship:** foundational

### `guha2023legalbench`
**Citation.** Guha et al. (2023). *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models*. NeurIPS Datasets and Benchmarks. [UNVERIFIED — researcher to confirm final venue metadata]

**Summary.** LegalBench aggregates many legal reasoning tasks and explicitly targets LLM legal reasoning evaluation. It is one of the closest legal-domain precedents and helps justify the legal axis. However, it focuses on benchmark performance rather than cross-domain failure categories or confidence calibration.

**Relevance quote.** [paraphrased from abstract] LegalBench is a benchmark for measuring legal reasoning in large language models.

**relationship:** adjacent

### `chalkidis2022lexglue`
**Citation.** Chalkidis et al. (2022). *LexGLUE: A Benchmark Dataset for Legal Language Understanding in English*. ACL.

**Summary.** LexGLUE is a suite of legal NLP tasks for classification, retrieval, and understanding. It demonstrates the maturity of legal-domain NLP evaluation and the need for domain-specific metrics. It does not study frontier reasoning traces or failure-mode distributions.

**Relevance quote.** [paraphrased from abstract] LexGLUE provides a benchmark for legal language understanding in English.

**relationship:** adjacent

### `almeldein2025nuclear`
**Citation.** Almeldein et al. (2025). *Exploring the Capabilities of the Frontier Large Language Models for Nuclear Energy Research*. arXiv:2506.19863. [UNVERIFIED — researcher to confirm author list/year]

**Summary.** Evaluates frontier LLMs for nuclear-energy research tasks such as literature synthesis, workflow design, and possibly NRC-style review support. It is highly relevant because nuclear safety review is underrepresented in LLM evaluation. It appears to advocate expert validation rather than propose a cross-domain taxonomy.

**Relevance quote.** [paraphrased from abstract] Frontier LLMs show promise for nuclear-energy research workflows but require expert validation.

**relationship:** adjacent

### `nucbench2026`
**Citation.** [UNVERIFIED — researcher to confirm citation key/year] *Establishing Benchmarks for Large Language Models in Nuclear Engineering / NucBench*. Nuclear Engineering and Design or related venue, 2026. [UNVERIFIED — metadata and exact title]

**Summary.** A reported nuclear-engineering benchmark for text and possibly multimodal nuclear tasks. It is directly relevant to the nuclear slice because it suggests a field-specific evaluation ecosystem is emerging. It is not, from available information, a five-domain failure taxonomy.

**Relevance quote.** [paraphrased from abstract] The benchmark evaluates LLM performance in nuclear engineering tasks.

**relationship:** adjacent

### `chen2021finqa`
**Citation.** Chen et al. (2021). *FinQA: A Dataset of Numerical Reasoning over Financial Data*. EMNLP.

**Summary.** FinQA evaluates numerical reasoning over financial reports. It motivates the finance/audit axis and shows that financial reasoning requires grounded arithmetic over tabular/textual disclosures. It does not evaluate reasoning models across domains or label failure modes.

**Relevance quote.** [paraphrased from abstract] FinQA is a dataset for numerical reasoning over financial data.

**relationship:** foundational

### `financebench2025risk`
**Citation.** *Standard Benchmarks Fail — Auditing LLM Agents in Finance Must Prioritize Risk*. arXiv:2502.15865, 2025. [UNVERIFIED — researcher to confirm authors/title]

**Summary.** Argues that ordinary finance LLM benchmarks can miss high-impact risks such as hallucination, stale facts, and adversarial vulnerabilities. This is very close in spirit to our safety motivation for finance. It remains finance-only and appears focused on benchmark/risk design rather than a shared taxonomy across professional domains.

**Relevance quote.** [paraphrased from abstract] Standard financial benchmarks fail to capture deployment-critical risks in LLM agents.

**relationship:** adjacent

### `phantom2025finance`
**Citation.** *PHANTOM: A Benchmark for Hallucination Detection in Financial Long-Context Question Answering*. NeurIPS / OpenReview, 2025. [UNVERIFIED — researcher to confirm authors and venue]

**Summary.** A finance-focused hallucination detection benchmark using long-context financial QA, including SEC-style disclosures. It directly supports our F1/F3 concern: hallucination and context loss interact in long professional documents. It is not cross-domain and does not include law, medicine, nuclear, and journalism.

**Relevance quote.** [paraphrased from abstract] PHANTOM measures hallucination detection in financial long-context question answering.

**relationship:** adjacent

### `hassan2017claimbuster`
**Citation.** Hassan et al. (2017). *ClaimBuster: The First-ever End-to-end Fact-checking System*. PVLDB / VLDB Endowment. [UNVERIFIED — researcher to confirm exact venue]

**Summary.** ClaimBuster provides a system and dataset for identifying check-worthy factual claims. It anchors the journalism/fact-checking domain in this project. It evaluates fact-checking workflows, not reasoning-model failure modes or confidence calibration.

**Relevance quote.** [paraphrased from abstract] ClaimBuster is an end-to-end fact-checking system for identifying check-worthy factual claims.

**relationship:** foundational

### `thorne2018fever`
**Citation.** Thorne et al. (2018). *FEVER: a Large-scale Dataset for Fact Extraction and VERification*. NAACL.

**Summary.** FEVER is a foundational fact verification benchmark requiring evidence retrieval and claim verification. It is relevant to the journalism axis and to feature hallucination, since unsupported claims are central. It does not analyze reasoning-model traces or professional-domain taxonomy.

**Relevance quote.** [paraphrased from abstract] FEVER requires systems to verify claims using evidence from Wikipedia.

**relationship:** foundational

## C. Confidence calibration in LLMs

### `lin2022calibration`
**Citation.** Lin, Hilton, and Evans (2022). *Teaching Models to Express Their Uncertainty in Words*. Transactions on Machine Learning Research.

**Summary.** Studies whether language models can express calibrated uncertainty in natural language. It is foundational for our F4 confidence miscalibration hypothesis because it connects verbal confidence to correctness. It is not domain-specific to high-stakes professional contexts.

**Relevance quote.** [paraphrased from abstract] Language models should know what they do not know and express uncertainty faithfully.

**relationship:** foundational

### `kadavath2022language`
**Citation.** Kadavath et al. (2022). *Language Models (Mostly) Know What They Know*. arXiv:2207.05221.

**Summary.** Shows that LLMs can often predict whether their own answers are correct under certain elicitation formats. It is central calibration background but also warns that measurement format matters. Our project tests whether such confidence signals remain reliable in professional-domain reasoning models.

**Relevance quote.** [paraphrased from abstract] Language models can be trained or prompted to predict the probability that their answers are correct.

**relationship:** foundational

### `xiong2023calibration`
**Citation.** Xiong et al. (2023). *Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs*. arXiv ID TBD / EMNLP findings? [UNVERIFIED — researcher to confirm metadata]

**Summary.** Evaluates confidence elicitation methods and demonstrates that LLM uncertainty estimates are sensitive to prompting and task design. This supports measuring ECE carefully rather than taking self-reported confidence at face value. It does not cover a professional five-domain taxonomy.

**Relevance quote.** [paraphrased from abstract] LLM confidence estimates depend strongly on elicitation method and can be miscalibrated.

**relationship:** adjacent

## D. Chain-of-thought analysis methods

### `wei2022cot`
**Citation.** Wei et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. NeurIPS.

**Summary.** Shows that prompting models to generate intermediate reasoning steps improves performance on arithmetic, commonsense, and symbolic reasoning tasks. It is foundational because our methodology collects and annotates reasoning traces. It does not establish that traces are faithful explanations.

**Relevance quote.** [paraphrased from abstract] Chain-of-thought prompting enables large language models to solve complex reasoning tasks by generating intermediate reasoning steps.

**relationship:** foundational

### `wang2023selfconsistency`
**Citation.** Wang et al. (2023). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR.

**Summary.** Introduces self-consistency decoding over multiple reasoning paths. The method is relevant because multiple seeds/traces can reveal stability or instability of failure labels. It optimizes answer accuracy rather than providing a failure taxonomy.

**Relevance quote.** [paraphrased from abstract] Sampling diverse reasoning paths and marginalizing over answers improves chain-of-thought reasoning.

**relationship:** foundational

### `turpin2023unfaithful`
**Citation.** Turpin et al. (2023). *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting*. NeurIPS / arXiv. [UNVERIFIED — researcher to confirm venue]

**Summary.** Demonstrates that generated chain-of-thought explanations can be systematically unfaithful to the model's actual decision process. This is a caution for our trace inspection: we should code observable failures without claiming mechanistic access. It supports conservative language in the manuscript.

**Relevance quote.** [paraphrased from abstract] Chain-of-thought explanations can be unfaithful and rationalize answers after the fact.

**relationship:** foundational

### `stopanthro2024`
**Citation.** [UNVERIFIED — researcher to confirm citation key/year] *Stop Anthropomorphizing Intermediate Tokens: Lessons from Scaling Language Models as Reasoners*. arXiv:2402.19468.

**Summary.** Argues against treating intermediate tokens or hidden states as human-like thoughts. This is methodologically important for our CoT analysis: failure annotations should treat traces as model outputs and evidence of behavior, not literal cognition. It is not a domain benchmark.

**Relevance quote.** [paraphrased from abstract] Intermediate tokens should not be anthropomorphized as human-like reasoning steps.

**relationship:** foundational

## E. Hallucination taxonomies

### `ji2023survey`
**Citation.** Ji et al. (2023). *Survey of Hallucination in Natural Language Generation*. ACM Computing Surveys.

**Summary.** Provides a comprehensive survey of hallucination definitions, causes, and evaluation methods in NLG. It is foundational for F1 feature hallucination and helps distinguish intrinsic/extrinsic hallucination. It is broader than reasoning models and not cross-domain professional evaluation.

**Relevance quote.** [paraphrased from abstract] Hallucination refers to generated content that is nonsensical or unfaithful to the provided source.

**relationship:** foundational

### `maynez2020faithfulness`
**Citation.** Maynez et al. (2020). *On Faithfulness and Factuality in Abstractive Summarization*. ACL.

**Summary.** Shows that abstractive summarization models can generate fluent but factually inconsistent content. It is an early empirical basis for treating factual unsupportedness as a distinct failure mode. It is not reasoning-model or professional-domain specific.

**Relevance quote.** [paraphrased from abstract] Neural abstractive summarization models can produce summaries that are not faithful to source documents.

**relationship:** foundational

### `huang2023hallucinationSurvey`
**Citation.** Huang et al. (2023). *A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions*. arXiv:2311.05232. [UNVERIFIED — researcher to confirm final venue]

**Summary.** Surveys hallucination in LLMs and organizes causes, detection, and mitigation. It provides vocabulary for our feature hallucination category but does not connect hallucination to domain-specific dominance patterns. Our contribution would operationalize hallucination alongside rigidity, context compression, and calibration.

**Relevance quote.** [paraphrased from abstract] The survey discusses hallucination taxonomy, detection, and mitigation for large language models.

**relationship:** foundational

### `halluLens2025`
**Citation.** *HalluLens: LLM Hallucination Benchmark*. ACL 2025. [UNVERIFIED — researcher to confirm authors and exact citation]

**Summary.** A recent hallucination benchmark/taxonomy paper reported in live search results. It is relevant because it sharpens definitions for hallucination evaluation and may be a close comparator for F1. It appears hallucination-specific, not a cross-domain reasoning failure taxonomy.

**Relevance quote.** [paraphrased from abstract] HalluLens benchmarks hallucination in large language models with explicit hallucination definitions.

**relationship:** adjacent

## F. Foundational reasoning-model papers and model cards

### `openai2024o1`
**Citation.** OpenAI (2024). *OpenAI o1 System Card*. Technical report / system card.

**Summary.** Documents the o1 family and its safety/evaluation properties. It is foundational because o1 introduced widely visible test-time reasoning behavior and chain-of-thought-hidden reasoning products. It is a model card, not an independent failure taxonomy.

**Relevance quote.** [paraphrased from system card] o1 models are trained to spend more time thinking before responding.

**relationship:** foundational

### `guo2025deepseekr1`
**Citation.** Guo et al. / DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948.

**Summary.** Presents DeepSeek-R1 and reasoning-oriented reinforcement learning. It is foundational for the open reasoning-model baseline in our study. It reports capabilities and training approach rather than cross-domain professional reliability failures.

**Relevance quote.** [paraphrased from abstract] DeepSeek-R1 demonstrates reasoning capability incentivized through reinforcement learning.

**relationship:** foundational

### `anthropic2025claude37`
**Citation.** Anthropic (2025). *Claude 3.7 Sonnet System Card*. Technical report / model card. [UNVERIFIED — researcher to confirm exact title/date]

**Summary.** Documents Claude 3.7 Sonnet and its extended-thinking/safety properties. It is foundational for selecting Claude Thinking as a model under evaluation. It does not answer the proposed cross-domain failure question.

**Relevance quote.** [paraphrased from system card] Claude 3.7 Sonnet supports extended thinking for complex tasks.

**relationship:** foundational

### `google2025gemini25`
**Citation.** Google DeepMind (2025). *Gemini 2.5 Pro / Gemini Thinking Technical Report or Model Card*. [UNVERIFIED — researcher to confirm exact title/date]

**Summary.** Describes Gemini's thinking-capable model family and capabilities. It is foundational because Gemini Thinking is one of the planned evaluated systems. The report is a model disclosure artifact, not a professional-domain failure taxonomy.

**Relevance quote.** [paraphrased from model card] Gemini 2.5 Pro includes thinking capabilities for complex reasoning tasks.

**relationship:** foundational

### `liu2024safetybench`
**Citation.** Liu et al. (2024). *SafetyBench: Evaluating the Safety of Large Language Models*. ACL.

**Summary.** SafetyBench is a broad safety-evaluation benchmark with multi-category questions. It is relevant as a general safety benchmark comparator and for discussing why generic safety evaluations are insufficient for professional-domain reasoning failures. It is not tailored to medicine/law/nuclear/finance/journalism failure-mode distributions.

**Relevance quote.** [paraphrased from abstract] SafetyBench evaluates LLM safety across multiple categories and languages.

**relationship:** adjacent
