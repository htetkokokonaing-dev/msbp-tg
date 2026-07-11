# Step 16 — Open Row-Level Dataset Strategy Gate

Final verdict: `STEP16_OPEN_ROW_LEVEL_DATA_FOUND_PMSBP_PARSER_MUST_BE_EXTENDED`

## PolyMetriX audit

- File exists: True
- Rows: 7367
- Has PSMILES column: True
- Has experimental Tg column: True
- Nonempty PSMILES rows: 7367
- Numeric Tg rows: 7367
- Source count: 6
- Polymer class count: 22
- Rows supported by current Step-14 pMSBP parser: 161
- Rows unsupported by current Step-14 pMSBP parser: 7206
- Support fraction: 0.021854
- PolyMetriX verdict: `OPEN_DATASET_FOUND_PMSBP_PROTOTYPE_COVERAGE_LOW`

## Interpretation

A real open row-level Tg dataset is present. This resolves the dataset-strategy direction.

However, the current pMSBP parser is still a prototype. It was designed for simple two-terminal gate strings, not complex PSMILES/BigSMILES. The next step is therefore not journal writing; it is parser extension and feature extraction.

## Next required step

Step 17 should implement a PSMILES-aware pMSBP parser or a conservative conversion layer for the PolyMetriX PSMILES column. Only after row coverage is high enough should source-level statistics be recomputed.
