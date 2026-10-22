# Clinical Auditor Agent
## Five-Case Pilot Experiment: Provisional Results

### Study scope

Five selected validation cases were evaluated using two
clinical-note generation methods: Simple Baseline and
Structured Prompt.

There were 168 reference-fact comparisons per method,
for 336 comparisons overall.

CASE_0014 was used for development and is excluded
from this five-case pilot.

### Pooled results

| Metric | Simple Baseline | Structured Prompt |
|---|---:|---:|
| Complete preservation | 31.55% | 39.88% |
| Omission rate | 45.83% | 40.48% |
| Weighted preservation | 42.86% | 49.70% |

### Case-balanced results

| Metric | Simple Baseline | Structured Prompt |
|---|---:|---:|
| Complete preservation | 33.88% | 41.44% |
| Omission rate | 42.75% | 38.31% |
| Weighted preservation | 45.56% | 51.56% |

### Principal findings

The Structured Prompt achieved a
+7.56
percentage-point difference in case-balanced complete
preservation and a
+6.00
percentage-point difference in case-balanced weighted
preservation relative to the Simple Baseline.

The corresponding case-balanced omission-rate difference
was -4.44
percentage points.

The Structured Prompt had a higher weighted preservation
score in three of the five evaluated cases.

### Evaluation methodology

Clinical reference facts were extracted and refined
through source-evidence inspection and decomposition.

Generated notes were provisionally classified as:
present, partial, missing, or contradicted.

The exploratory weighted preservation metric assigned:
present = 1, partial = 0.5, missing = 0,
and contradicted = 0.

Pooled scores weight each reference fact equally.
Case-balanced scores give each selected case equal weight.

### Limitations

1. All preservation labels are provisional.
   No independent clinical adjudication was performed.

2. The pilot includes only five selected validation cases.
   The sample is too small for broad clinical conclusions.

3. Reference-fact extraction and completeness review
   were not independently validated.

4. Some reference facts may overlap or carry different
   levels of clinical importance.

5. The exploratory partial-credit weighting is not a
   clinically validated scoring system.

6. This experiment measures preservation in generated
   documentation, not the detection accuracy of the
   Clinical Auditor Agent.

7. The implemented prototype is a rule-driven
   proof of concept. The complete proposed architecture,
   including BiLSTM-CRF and semantic bipartite matching,
   has not been implemented or validated.

8. These preliminary findings do not establish
   clinical safety, statistical significance,
   or generalizability.

### Conclusion

In this small exploratory pilot, structured prompting
showed higher average documentation-preservation scores
than simple prompting. The observed differences warrant
evaluation with larger datasets, independently reviewed
reference annotations, and separate validation of
the Clinical Auditor's detection performance.

These results should be described as provisional
proof-of-concept findings.
