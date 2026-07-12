# Step 19 - Comparator Descriptor + Journal Evidence Hardening

Status: patch prepared

Purpose: compare pMSBP against available PolyMetriX descriptors and decide whether the future journal manuscript can survive the reviewer objection that pMSBP is merely renamed rotatable-bond density.

Main command:

```bash
python scripts/run_comparator_evidence_hardening.py --n-bootstrap 200
```

Outputs:

```text
descriptor_coverage_summary.csv
descriptor_univariate_association_summary.csv
descriptor_cluster_bootstrap_ci.csv
incremental_residual_linear_model_summary.csv
pmsbp_redundancy_vs_comparators.csv
step19_journal_evidence_hardening_verdict.csv
STEP19_COMPARATOR_DESCRIPTOR_EVIDENCE_HARDENING_REPORT.md
```

Possible verdicts:

```text
STEP19_GO_INCREMENTAL_DESCRIPTOR_EVIDENCE_SUPPORTED
STEP19_REVISE_AS_OPEN_DATA_DESCRIPTOR_OBSERVATION_NOT_INCREMENTAL_LOCKED
STEP19_REPOSITION_AS_ROTATABLE_MOBILITY_DESCRIPTOR_NOT_NEW_PRINCIPLE
STEP19_NO_GO_COMPARATOR_EVIDENCE_WEAK
```
