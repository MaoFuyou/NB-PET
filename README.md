<div align="center">

# NB-PET

### Multi-label recognition and report-guided 3D localization in pediatric neuroblastoma PET/CT

**Routine report supervision · Image-only recognition · Report-conditioned localization**

[Overview](#overview) · [Method](#method) · [Evaluation](#evaluation) · [Getting started](#getting-started) · [中文](README.zh-CN.md)

</div>

## Overview

NB-PET uses routine Chinese PET/CT reports to derive clinical labels and coarse anatomical references. These structured signals supervise two research tasks in whole-body pediatric neuroblastoma PET/CT: **multi-label recognition from images alone** and **3D localization guided by the current examination's report**. The two tasks have different inference inputs and should be interpreted separately.

<p align="center">
  <img src="assets/figures/framework.svg" alt="NB-PET schematic: routine reports provide structured supervision; image-only recognition and report-guided localization use distinct inference inputs" width="100%" />
</p>

*Figure 1. High-level research workflow. The schematic contains no patient images or records.*

## Method

### 1. Structure routine reports

Extract report-derived clinical labels and associate positive findings with coarse anatomical regions. These regions are weak spatial references, not manually drawn lesion masks.

### 2. Recognize findings from paired PET/CT

Learn PET/CT features for examination-level multi-label recognition. The current report is not an inference input for this task.

### 3. Localize report-specified findings

Condition the localization model on the structured labels and anatomical regions from the current examination. It produces overall and label-specific 3D response maps and ranks candidate regions for review alongside the source images.

| Task | Inference input | Output |
|---|---|---|
| Multi-label recognition | PET and CT volumes | Examination-level clinical label scores |
| Report-guided localization | PET and CT volumes, current report labels, and associated regions | Overall and label-specific 3D heatmaps; ranked candidates |

## Evaluation

### Study cohorts

| Cohort | Cases reported in the manuscript |
|---|---:|
| Beijing Friendship Hospital | 656 |
| Zhejiang University Children's Hospital | 280 |
| **Total** | **936** |

Each center evaluates 26 labels; cross-center recognition restricts evaluation to 25 shared labels. The site-specific pelvic definitions are not interchangeable.

### Evaluation settings

- **Recognition:** within-center validation and bidirectional cross-center evaluation, including zero-shot and few-shot adaptation.
- **Localization:** agreement between model responses and report-derived anatomical references. A reference-region hit is not evidence of overlap with a manually delineated lesion.
- **Comparability:** record the inference inputs, reference mask, grid, and aggregation unit with every result. Results from different protocols are kept separate.

See [data and evaluation](docs/data-and-evaluation.md) for the label, data, and scoring conventions. Manuscript performance tables are not distributed in this draft.

## Case studies

The bundled example is **synthetic**. It shows why a threshold on the kth-largest score can admit zero-response pixels and turn a miss into a hit. It contains no clinical images, reports, identifiers, or learned weights.

<details>
<summary><strong>Open the synthetic example</strong></summary>

The demo compares the old threshold-based selection with a positive-only selection capped at the requested pixel budget. The corrected rule does not pad the selection with zeros. This is a scoring demonstration, not model inference or a reproduction of a clinical result.

</details>

## Getting started

### Run the synthetic evaluation

Use Python 3.10 or newer. The demonstration has no third-party dependencies; from the repository root:

```bash
python3 scripts/run_synthetic_evaluation.py
python3 -m unittest discover -s tests -v
```

The [release status](docs/release-status.md) distinguishes the files in this draft from the full NB-PET training and inference implementation, checkpoints, and data. The full model cannot be run from this draft.

## Data and model workflow

The research pipeline separates report structuring, image-only recognition, report-conditioned localization, and evaluation. For an implementation release, the preprocessing convention, label order, input contract, and evaluation rules must be versioned together. See [data and evaluation](docs/data-and-evaluation.md) for the intended documentation boundary.

## Repository structure

```text
NB-PET/
├── assets/figures/    # Original project schematic
├── configs/           # Synthetic demonstration inputs
├── docs/              # Data, evaluation, and release notes
├── scripts/           # Synthetic evaluation entry point
├── src/               # Data-free demonstration code
├── tests/             # Demonstration tests
└── .github/          # Checks and pull-request guidance
```

## Validation and contributions

The test suite checks selection budgets, empty references, and threshold ties using toy arrays. It does not validate clinical performance. See [contribution guidance](CONTRIBUTING.md) before adding material.

## Citation

The manuscript link, confirmed author list, and citation metadata will be added after release approval. No publication venue, DOI, or pretrained-model release is claimed here.

NB-PET is a research project. This draft is not intended for clinical decision-making.
