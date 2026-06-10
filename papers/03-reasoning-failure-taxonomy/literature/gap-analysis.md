# Gap analysis — Paper 03

## Explicit gap statement

Published work has evaluated reasoning-capable LLMs on general reasoning benchmarks, medical QA, legal reasoning, financial QA, fact-checking, and emerging nuclear-energy tasks, but it has not yet provided a unified, empirically coded taxonomy of *how* frontier reasoning models fail across multiple high-stakes professional domains. Existing studies tend to be either domain-specific (e.g., M-ARC, LegalBench, PHANTOM), failure-specific (e.g., hallucination surveys and hallucination benchmarks), or model-card/system-card disclosures (e.g., o1, DeepSeek-R1, Claude Thinking, Gemini Thinking). The missing unit of analysis is the cross-domain distribution of failure modes: whether hallucination, pattern rigidity, context compression, and confidence miscalibration dominate differently in medicine, law, nuclear review, finance, and journalism. Paper 03 fills that gap by holding models and annotation codes fixed while varying professional domain.

## Falsification argument

The strongest way to falsify the gap claim would be to find a 2024--2026 paper that simultaneously: (1) evaluates frontier reasoning models such as o1/o3, DeepSeek-R1, Claude Thinking, or Gemini Thinking; (2) covers at least three of the five proposed professional domains; (3) annotates failed responses using an explicit taxonomy beyond raw accuracy; and (4) reports calibration or confidence failure as a first-class outcome. The closest medical source, `kim2025marc`, appears to evaluate medical abstraction/reasoning only, so it cannot answer whether medical failures differ from legal, nuclear, financial, and journalism failures. The closest legal source, `guha2023legalbench`, is broad within law but benchmark-centric; it does not provide cross-domain failure-mode prevalence. The closest financial sources, `financebench2025risk` and `phantom2025finance`, directly motivate risk-aware hallucination/context evaluation, but they are finance-only and primarily concerned with finance agent risk or hallucination detection. The closest general hallucination sources, `ji2023survey`, `huang2023hallucinationSurvey`, and `halluLens2025`, address one family of failures rather than distinguishing hallucination from rigidity, compression, and calibration across professional domains. General safety benchmarks such as `liu2024safetybench` are broader in safety category, but they are not organized around professional-domain workflow failures and do not appear to test the hypothesis that failure-mode dominance is domain-specific. Model cards and technical reports (`openai2024o1`, `guo2025deepseekr1`, `anthropic2025claude37`, `google2025gemini25`) establish the model class but do not publish independent, cross-domain failure annotations. Therefore the gap survives the current falsification pass, with the caveat that rapidly moving frontier-lab evaluations could still scoop this before submission.

## Counter-arguments addressed

### Challenge 1: "LegalBench / MMLU already covers many domains."

`hendrycks2021mmlu` and `guha2023legalbench` show that broad benchmark coverage and legal-reasoning coverage already exist. But their reported unit is mostly task performance, not coded failure mechanisms. They do not compare medicine, law, nuclear review, finance, and journalism under a shared F1--F4 taxonomy, nor do they test whether a failure mode such as context compression dominates one domain while hallucination dominates another.

### Challenge 2: "Hallucination taxonomies already solve the taxonomy problem."

`ji2023survey`, `maynez2020faithfulness`, `huang2023hallucinationSurvey`, and `halluLens2025` provide strong definitions for hallucination and factual inconsistency. They do not solve the present problem because hallucination is only one proposed failure code. The proposed paper treats hallucination as F1 and explicitly compares it with F2 pattern rigidity, F3 context compression, and F4 confidence miscalibration under the same evaluation protocol.

### Challenge 3: "Finance and nuclear studies already show high-stakes-domain failures."

`financebench2025risk`, `phantom2025finance`, `almeldein2025nuclear`, and `nucbench2026` are important adjacent works because they show that professional deployment risks are domain-specific and serious. They do not provide cross-domain evidence about whether the same model fails differently by domain. Paper 03 is therefore not competing with them as another single-domain benchmark; it uses their motivation to ask a higher-level comparative question.

### Challenge 4: "Reasoning-model system cards already report safety evaluations."

The model cards and technical reports (`openai2024o1`, `guo2025deepseekr1`, `anthropic2025claude37`, `google2025gemini25`) are foundational for model selection, but they are not independent cross-domain professional evaluations. They typically report aggregate safety/capability outcomes and deployment mitigations. They do not publish a five-domain, annotator-coded failure taxonomy with calibration analysis.

## Scoop-risk assessment

No >60% scoop was found in this pass. The highest-risk adjacent works are (1) `kim2025marc` for medical reasoning, (2) `phantom2025finance` / `financebench2025risk` for finance risk and hallucination, (3) `almeldein2025nuclear` / `nucbench2026` for nuclear LLM evaluation, and (4) lab model cards for frontier reasoning systems. The scoop risk remains operationally high because a frontier lab or evaluation organization could combine these pieces quickly, but current located work appears adjacent rather than competing.
