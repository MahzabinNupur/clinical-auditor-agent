# Clinical Auditor Agent

## Bridging the Documentation-to-Diagnosis Gap with Ambient AI

Research prototype investigating clinical documentation
preservation and the potential role of automated auditing
in identifying omitted clinical information.

### Repository contents

- `clinical_auditor.py`: rule-driven research prototype
- `notebooks/01_Dataset_Preprocessing.ipynb`:
  dataset preprocessing and splitting
- `notebooks/02_Baseline_Experiment.ipynb`:
  note-generation experiments and provisional evaluation
- `results/`: five-case pilot summaries

### Pilot evaluation

Five selected validation cases were evaluated using
Simple Baseline and Structured Prompt note generation.

A total of 336 fact-note comparisons were assessed:
168 comparisons per method.

| Case-balanced metric | Simple Baseline | Structured Prompt |
|---|---:|---:|
| Complete preservation | 33.88% | 41.44% |
| Omission rate | 42.75% | 38.31% |
| Weighted preservation | 45.56% | 51.56% |

Structured prompting showed a 6.00 percentage-point
improvement in case-balanced weighted preservation.

### Interpretation

All reference-fact preservation assessments are
provisional and have not undergone independent clinical
adjudication. The five-case pilot is exploratory.

The implemented auditor is a rule-driven proof of concept.
The complete proposed architecture, including BiLSTM-CRF
and semantic bipartite matching, has not been implemented
or validated.

The pilot evaluates generated-documentation preservation,
not the diagnostic accuracy or clinical effectiveness of
the Clinical Auditor Agent.

### Reproducibility

The notebooks document the exploratory workflow.
They were developed in Google Colab and may reference
Google Drive paths or files not distributed here.

Users must provide appropriately licensed input data
and configure their own environment and API credentials
where required. No API credentials are included.

The repository is a research artifact, not a
turnkey reproducibility package.

### Clinical safety

For research purposes only. Not validated for clinical
decision-making or patient care.

### Research title

The Clinical Auditor Agent: Bridging the
Documentation-to-Diagnosis Gap with Ambient AI
