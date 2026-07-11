# Step 16 — Open Row-Level Dataset Strategy Gate

**Status:** patch prepared  
**Purpose:** begin Option C using open row-level polymer Tg data.

## What this gate checks

1. PolyMetriX curated Tg file exists.
2. Required row-level columns exist:
   - `PSMILES`
   - `labels.Exp_Tg(K)`
3. Metadata columns are counted:
   - `meta.source`
   - `meta.polymer_class`
   - `meta.reliability`
4. Current Step-14 pMSBP parser coverage is measured.
5. Failed / empty secondary downloads are recorded, especially the Figshare zip if it is zero bytes.

## Main command

```bash
python scripts/run_open_dataset_strategy_gate.py
```

## Expected output directory

```text
results/step16_open_row_level_dataset_gate/
```

Expected files:

```text
open_dataset_presence.csv
polymetrix_row_level_audit.csv
polymetrix_current_pmsbp_support_sample.csv
polyverse_tg_like_files.csv
STEP16_OPEN_ROW_LEVEL_DATASET_GATE_REPORT.md
```

## Possible final verdicts

```text
STEP16_OPEN_DATA_READY_FOR_PMSBP_REANALYSIS
```

The open row-level dataset exists and the current pMSBP parser has sufficient coverage.

```text
STEP16_OPEN_ROW_LEVEL_DATA_FOUND_PMSBP_PARSER_MUST_BE_EXTENDED
```

The open row-level dataset exists, but the current parser is too limited for full PolyMetriX PSMILES re-analysis. This is expected if most PSMILES strings are complex.

```text
STEP16_OPEN_ROW_LEVEL_DATA_NOT_READY
```

The dataset is missing or required columns are absent.

## Scientific implication

If the likely verdict is `STEP16_OPEN_ROW_LEVEL_DATA_FOUND_PMSBP_PARSER_MUST_BE_EXTENDED`, then Option C is still the best path, but Step 17 must build a PSMILES-aware parser/conversion layer before any new statistical claims.
