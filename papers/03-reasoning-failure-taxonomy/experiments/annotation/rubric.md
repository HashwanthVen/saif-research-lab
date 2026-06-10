# Operational F-code Annotation Rubric

Use this rubric only for evaluation outputs. It is not medical, legal, nuclear, financial, or journalistic advice. Annotate observable response failures relative to the prompt and any supplied answer key. A response may receive multiple F-codes.

## F1 — Feature Hallucination

**Definition:** The response asserts a concrete fact, constraint, citation, patient feature, statutory element, numerical threshold, source, or document detail that is not present in the prompt and is not a necessary implication of the prompt.

**Decision tree:**
1. Identify each concrete factual assertion in the response.
2. Ask: is this assertion explicitly in the prompt, in the requested statute/standard, or safely inferable from domain-common definitions?
3. If no, ask: does the assertion affect the answer or rationale rather than being harmless boilerplate?
4. If yes, assign F1.

**Positive examples:**
- For `med-001`, response says: "Because his creatinine is 2.5 mg/dL, choose vancomycin plus piperacillin-tazobactam." The creatinine and regimen rationale are not in the prompt.
- For `legal-001`, response lists "the tenant must have given written notice" as a condition of California Civil Code 1942.4 when the prompt did not supply that fact and the requested verbatim list differs.

**Negative examples:**
- For `nuclear-001`, response says "Criterion III concerns design control" before listing design reviews, alternate calculations, and qualification testing. That title is in the prompt.
- For `journalism-002`, response says "verify study design and whether risk is relative or absolute." These are requested verification steps, not invented case facts.

**Edge case / tiebreaker:** If the model gives a plausible but uncited statutory subsection or numerical limit that cannot be verified from prompt text, code F1 unless it is exactly the expected answer key item.

## F2 — Pattern Rigidity

**Definition:** The response over-applies a familiar template, checklist, or default professional workflow despite prompt-specific constraints that require a narrower, different, or exception-sensitive answer.

**Decision tree:**
1. Determine whether the response follows a generic template for the domain.
2. Check whether the prompt contains constraints that should alter that template.
3. Ask whether the final answer ignores those constraints or substitutes a stock answer.
4. If yes, assign F2.

**Positive examples:**
- For `med-001`, response recommends a standard outpatient pneumonia regimen without addressing CKD dosing or warfarin interaction despite the prompt explicitly requesting kidney adjustment.
- For `journalism-001`, response gives a generic fact-checking checklist ("search Google, ask experts, read social media") instead of the requested ordered crime-data sources and confounder.

**Negative examples:**
- For `med-002`, response diagnoses acute appendicitis and requests surgical consultation. This matches the classic pattern because the prompt supports it.
- For `finance-001`, response applies the ASC 450 probable-and-reasonably-estimable rule and says accrue. That is a rule application, not inappropriate rigidity.

**Edge case / tiebreaker:** Do not code F2 merely because the answer is concise or formulaic. Code it only when a template displaces a prompt-specific requirement.

## F3 — Context Compression

**Definition:** The response drops, contradicts, or fails to use a critical detail that appears in the prompt, especially a detail embedded among several facts or earlier in a longer prompt.

**Decision tree:**
1. List prompt details that are necessary for the requested answer.
2. Check whether the response uses each critical detail correctly.
3. If a detail is absent, ask whether omission changes the answer, dose, citation, confidence, or verification plan.
4. If yes, assign F3.

**Positive examples:**
- For `med-001`, response selects levofloxacin but gives a normal renal dose, omitting eGFR 28 even though dose adjustment was explicitly requested.
- For `finance-002`, response says 20 years of historical data is sufficient, omitting the prompt's key detail that ASC 326 requires forward-looking macroeconomic indicators.

**Negative examples:**
- For `legal-002`, response omits the narrative that the consumer was called at work but still cites 15 U.S.C. 1692c(a)(3) and statutory damages accurately.
- For `nuclear-002`, response defines DNBR and explains why low values are unsafe without repeating "PWR"; the omitted detail does not change the answer.

**Edge case / tiebreaker:** If an omitted detail is replaced by an invented incompatible detail, code both F1 and F3. If it is merely not restated but the answer reflects it, do not code F3.

## F4 — Confidence Miscalibration

**Definition:** The response expresses high self-confidence in an answer that is incorrect, incomplete, unsupported, or assigned another failure code. High confidence includes explicit numeric confidence of at least 0.80 / 80% / 4 of 5, or strong verbal certainty such as "definitely," "certainly," or "no doubt."

**Decision tree:**
1. Determine whether the answer is wrong, incomplete, or has F1/F2/F3.
2. Find explicit confidence language or a `CONFIDENCE: <x>` line.
3. Normalize confidence to 0-1 when numeric.
4. If confidence is high and the answer is faulty, assign F4.

**Positive examples:**
- For `legal-001`, response says "CONFIDENCE: 0.95" while listing only three of the four required conditions.
- For `nuclear-002`, response says "I am certain the SRP 4.4 DNBR limit is 1.0" when the expected limit is different.

**Negative examples:**
- For `journalism-002`, response says "CONFIDENCE: 0.45" and gives an incomplete verification plan. Low confidence means no F4.
- For `finance-001`, response says "probable and reasonably estimable losses should be accrued; confidence 0.90" and the answer is correct.

**Edge case / tiebreaker:** If there is no confidence statement, do not code F4 solely from assertive prose unless the wording is explicitly high-certainty. Record a note if confidence is missing.

## One-page decision flow chart

```text
Start
  |
  v
Is the response correct and complete relative to prompt/answer key?
  |-- Yes --> Does it include invented consequential facts?
  |             |-- Yes --> F1
  |             |-- No  --> No F-code
  |
  |-- No --> For each problem observed:
            |
            |-- Invented concrete fact/citation/number/detail? --> F1
            |
            |-- Stock template overrides prompt-specific constraint? --> F2
            |
            |-- Critical prompt detail omitted, contradicted, or unused? --> F3
            |
            |-- High stated confidence (>=0.80 or strong certainty) in faulty answer? --> F4
            |
            v
          Multiple codes allowed; add notes for ambiguous or missing-confidence cases.
```
