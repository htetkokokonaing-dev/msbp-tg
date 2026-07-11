# Step 18 — Open-data pMSBP Statistical Re-analysis

Verdict: `STEP18_GO_NEGATIVE_WITHIN_CLASS_SIGNAL_REANALYSIS_SUPPORTED`

## Main results

- Supported open rows: 7367
- Polymer classes: 22
- Sources: 6
- Representation classes: 6176
- Overall Spearman rho: -0.5315390888078491
- Within-class median-residual Spearman rho: -0.269476413921309
- Within-class mean-residual Spearman rho: -0.2649844094957029

## Uncertainty checks

- Row bootstrap: 200
- Class-cluster bootstrap: 200
- Within-class permutation: 200
- Class-cluster bootstrap residual CI: [-0.40481064881677997, -0.12300542891000447]
- Within-class permutation empirical p: 0.004975124378109453

## Interpretation

The open-data pMSBP re-analysis has a stable within-class signal under the current audit tests.

This still does not make the journal manuscript final. The next step is Step 19: inspect whether the token-sequence pMSBP coordinate is chemically defensible, compare against existing descriptors, and write the revised manuscript around the open-data result only.

## Output files

```text
polymetrix_open_pmsbp_feature_table.csv
overall_pmsbp_association_summary.csv
polymer_class_stratified_summary.csv
source_stratified_summary.csv
bootstrap_uncertainty_summary.csv
within_class_permutation_summary.csv
leave_one_class_out_sensitivity.csv
step18_reanalysis_verdict.csv
```
