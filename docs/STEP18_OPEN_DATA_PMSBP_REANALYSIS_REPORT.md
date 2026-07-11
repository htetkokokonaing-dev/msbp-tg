# Step 18 — Open-data pMSBP Statistical Re-analysis

**Status:** patch prepared  
**Purpose:** compute the first open-row-level pMSBP statistical re-analysis using PolyMetriX.

## What this step produces

```text
polymetrix_open_pmsbp_feature_table.csv
overall_pmsbp_association_summary.csv
polymer_class_stratified_summary.csv
source_stratified_summary.csv
bootstrap_uncertainty_summary.csv
within_class_permutation_summary.csv
leave_one_class_out_sensitivity.csv
step18_reanalysis_verdict.csv
STEP18_OPEN_DATA_PMSBP_REANALYSIS_REPORT.md
```

## Main command

```bash
python scripts/run_open_data_pmsbp_reanalysis.py
```

Faster smoke run:

```bash
python scripts/run_open_data_pmsbp_reanalysis.py --n-bootstrap 50 --n-permutation 50
```

Fuller audit run:

```bash
python scripts/run_open_data_pmsbp_reanalysis.py --n-bootstrap 500 --n-permutation 500
```

## Possible verdicts

```text
STEP18_GO_NEGATIVE_WITHIN_CLASS_SIGNAL_REANALYSIS_SUPPORTED
STEP18_GO_POSITIVE_WITHIN_CLASS_SIGNAL_REANALYSIS_SUPPORTED
STEP18_MIXED_RAW_SIGNAL_WITHIN_CLASS_NOT_LOCKED
STEP18_NO_GO_SIGNAL_NOT_STABLE
STEP18_NO_GO_INSUFFICIENT_ANALYSIS_SIGNAL
```

## Scientific caution

Even a GO verdict is not yet a journal-submission verdict. It means open-data pMSBP re-analysis has a stable statistical signal under this audit. Step 19 must still compare against existing descriptors, refine chemical interpretation, and rewrite the manuscript around open-data results only.
