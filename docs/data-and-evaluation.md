# Data and evaluation

## Study material

The NB-PET study uses paired whole-body PET/CT and routine reports from two centers. Patient-level scans, text, identifiers, case-level splits, and prediction files are not distributed here. Any later sharing requires the applicable institutional and data-governance approvals. This document does not offer a data-access mechanism.

## Task contracts

| Stage | Required research inputs | Evaluation target |
|---|---|---|
| Report structuring | Text from an eligible examination | Defined clinical labels and coarse region references |
| Recognition | Paired PET and CT | Examination-level report-derived label vector |
| Localization | PET/CT plus current report-derived labels and regions | Spatial agreement with coarse report-derived regions |

The target-center cohort gate must preserve the distinction between 26 site-specific labels and the 25 labels shared across centers. Record the label order and the source of every reference region. No example in this repository constitutes an authorized clinical deployment or a released model input schema.

## What to record with a result

- The cohort, eligible-record count, split version, and unit of aggregation.
- The inference inputs, including whether the current report is present.
- The image grid and reference mask, including any projection or resampling.
- The selection rule, tie handling, and treatment of empty reference regions.
- The interval and comparison procedure, and the model or evaluation release used.

The synthetic example uses a positive-only top-fraction rule. It illustrates the selection logic only; its toy outputs and tie-break policy are not manuscript performance results.
