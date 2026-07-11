# Step 17 — PSMILES-aware pMSBP Parser Extension Gate

**Status:** patch prepared  
**Purpose:** extend pMSBP from simple gate strings to PolyMetriX-style PSMILES strings.

## What this step adds

```text
src/msbp_tg/psmiles_parser.py
scripts/run_psmiles_parser_extension_gate.py
tests/test_step17_psmiles_parser_extension_gate.py
```

The parser supports:

```text
[*]CC[*]
[*]C-C[*]
[*][C][C][*]
[*]CO[*] versus [*]OC[*]
[*]#C[SiH2]C#Cc1cccc(C#[*])c1
```

It converts common bracketed PSMILES atoms into a reproducible token sequence and computes a prototype pMSBP token-sequence quotient.

## Main command

```bash
python scripts/run_psmiles_parser_extension_gate.py
```

## Expected output directory

```text
results/step17_psmiles_parser_extension_gate/
```

Expected files:

```text
polymetrix_psmiles_parser_coverage_summary.csv
psmiles_unsupported_reason_taxonomy.csv
polymetrix_pmsbp_supported_sample.csv
polymetrix_class_level_pmsbp_preliminary_summary.csv
STEP17_PSMILES_PARSER_EXTENSION_GATE_REPORT.md
```

## Possible verdicts

```text
STEP17_PSMILES_PARSER_EXTENDED_COVERAGE_PASS
STEP17_PSMILES_PARSER_EXTENDED_BUT_COVERAGE_LIMITED
STEP17_PSMILES_PARSER_LOW_COVERAGE
STEP17_PSMILES_PARSER_NO_COVERAGE
```

## Scientific caution

A coverage PASS does not mean the journal claim is ready. It only means pMSBP can now be computed on enough open row-level PSMILES strings to proceed to Step 18 statistical re-analysis.
