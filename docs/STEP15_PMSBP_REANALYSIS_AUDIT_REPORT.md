# Step 15 — pMSBP Re-feature / Re-analysis Audit

**Status:** patch prepared  
**Purpose:** determine whether the public repository can actually re-feature row-level polymer evidence with the Step-14 pMSBP descriptor.

## Why this step exists

The editorial critique identified a reproducibility blocker:

> the current public package is closer to an audit of aggregate outputs than a complete row-level scientific reproduction package.

Step 15 does not pretend to solve that automatically. It audits the repository for public-safe row-level tables containing both:

```text
SMILES/repeat-unit representation
Tg or glass-transition target
```

If such tables exist, the script applies pMSBP and writes preliminary source summaries.  
If they do not exist, the script returns a controlled audit-only verdict.

## New files

```text
src/msbp_tg/pmsbp_reanalysis.py
scripts/run_pmsbp_reanalysis_audit.py
tests/test_step15_pmsbp_reanalysis_audit.py
docs/STEP15_PMSBP_REANALYSIS_AUDIT_REPORT.md
docs/TERMUX_STEP15_PMSBP_REANALYSIS_AUDIT_COMMANDS.md
```

## Main command

```bash
python scripts/run_pmsbp_reanalysis_audit.py
```

## Possible verdicts

```text
PASS_WITH_ROW_LEVEL_REANALYSIS
```

At least one row-level public-safe table was found and pMSBP re-feature outputs were written.

```text
PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS
```

No public-safe row-level SMILES/Tg table was found. This is a valid audit result, but it means the repository still cannot support a full Journal of Cheminformatics reproducibility claim.

## Expected output directory

```text
results/step15_pmsbp_reanalysis_audit/
```

Expected files:

```text
pmsbp_candidate_table_audit.csv
pmsbp_refeature_summary.csv
STEP15_PMSBP_REANALYSIS_AUDIT_REPORT.md
```

If row-level candidate tables exist, also:

```text
pmsbp_refeature_rows_public_safe.csv
```

## Journal implication

If Step 15 returns `PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS`, the project should not submit to a journal requiring complete row-level third-party reproducibility. The next step must be either:

1. obtain permission / open-compatible row-level source tables; or
2. rebuild the study on fully open row-level datasets; or
3. change the target journal / reposition the work as a limited preprint and archive.
