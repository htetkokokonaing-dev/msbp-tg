# MSBP-Tg Step 15 pMSBP Re-feature / Re-analysis Audit Patch

This patch adds the Step-15 audit gate.

It checks whether the current public repository contains row-level, public-safe SMILES/Tg tables that can be re-featured with the Step-14 periodic MSBP coordinate.

Possible outputs:

- `PASS_WITH_ROW_LEVEL_REANALYSIS`
- `PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS`

The second result is not a code failure. It is an important scientific/reproducibility finding.
