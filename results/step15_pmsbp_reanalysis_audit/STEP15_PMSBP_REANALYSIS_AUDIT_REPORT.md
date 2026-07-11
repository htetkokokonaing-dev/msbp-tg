# Step 15 pMSBP Re-feature / Re-analysis Audit

Verdict: `PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS`

CSV tables scanned: 32
Row-level candidate tables found: 0
Re-feature summary tables produced: 0

Interpretation:

The repository does not currently expose a public-safe row-level table containing both SMILES/repeat-unit strings and Tg values. The pMSBP descriptor can be validated on representation gates, but the scientific result cannot yet be regenerated from public row-level evidence.

Journal implication:

Do not claim full Journal of Cheminformatics reproducibility until compatible row-level inputs or a complete open-data reconstruction are available.
