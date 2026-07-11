# MSBP-Tg Step 13 Periodic Descriptor Gate Patch

This patch starts the fundamental revision requested by the editorial critique.

It does **not** submit a new journal-ready version.  
It adds the first hard descriptor-validity gate:

```text
*CC* == *CCCC* == *CCCCCC*
```

under the prototype periodic MSBP coordinate.

## Files added

- `src/msbp_tg/periodic_fiber.py`
- `tests/test_periodic_representation_invariance.py`
- `scripts/run_periodic_invariance_gate.py`
- `docs/STEP13_PERIODIC_MSBP_DESCRIPTOR_GATE_REPORT.md`
- `docs/TERMUX_STEP13_PERIODIC_GATE_COMMANDS.md`

## Expected next scientific step

After this gate is in GitHub and CI green, extend the descriptor to orientation reversal, cut-point relocation, equivalent SMILES, aromatic/copolymer cases, then re-run the three-source analysis.
