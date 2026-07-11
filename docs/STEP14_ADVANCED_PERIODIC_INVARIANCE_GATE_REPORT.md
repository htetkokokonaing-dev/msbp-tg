# Step 14 — Advanced Periodic MSBP Invariance Gates

**Status:** patch prepared  
**Purpose:** extend the Step-13 descriptor-validity gate before any journal re-submission.

## Gates covered

Step 14 adds tests for:

1. Step-13 carbon supercell invariance:
   - `*CC*`
   - `*CCCC*`
   - `*CCCCCC*`

2. Orientation reversal:
   - `*CO*`
   - `*OC*`

3. Cut-point / cyclic relocation:
   - `*CCO*`
   - `*COC*`
   - `*OCC*`

4. Equivalent simple SMILES spelling:
   - `*CC*`
   - `*C-C*`
   - `*[C][C]*`

5. Non-carbon supercell invariance:
   - `*CO*`
   - `*COCO*`
   - `*COCOCO*`

6. Simple copolymer expansion:
   - `*CN*`
   - `*CNCN*`
   - `*CNCNCN*`

## New / modified files

```text
src/msbp_tg/periodic_fiber.py
tests/test_periodic_advanced_invariance.py
scripts/run_periodic_advanced_invariance_gate.py
docs/STEP14_ADVANCED_PERIODIC_INVARIANCE_GATE_REPORT.md
docs/TERMUX_STEP14_ADVANCED_PERIODIC_GATE_COMMANDS.md
```

## Expected command

```bash
python scripts/run_periodic_advanced_invariance_gate.py
```

Expected final line:

```text
PASS: all Step-14 advanced periodic MSBP invariance gates passed.
```

Expected CSV output:

```text
results/periodic_msbp_advanced_invariance_gate.csv
```

## Scientific caution

This is still a descriptor-validation gate, not a final scientific result. Passing these simple representation tests only permits moving to the next descriptor gate and later re-analysis. It does not by itself validate the polymer Tg claim.

## Next gate after Step 14

Step 15 should connect this pMSBP layer to the three existing data sources and report how many public-safe rows can be re-featured under the stricter periodic descriptor rules.
