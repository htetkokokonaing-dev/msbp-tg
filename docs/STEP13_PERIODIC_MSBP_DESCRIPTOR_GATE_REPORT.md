# Step 13 — Periodic MSBP Descriptor Gate

**Status:** prototype gate prepared  
**Purpose:** fix the central representation-invariance blocker before any new journal submission.

## Editorial blocker addressed

The old coordinate

```text
MSBP = -NumRotatableBonds / heavy_atoms
```

can change when the same simple polymer backbone is represented using different repeat-unit lengths:

```text
*CC*      heavy atoms 2, rotatable-like count 1
*CCCC*    heavy atoms 4, rotatable-like count 3
*CCCCCC*  heavy atoms 6, rotatable-like count 5
```

This is not acceptable for a polymer descriptor if those strings are treated as primitive-cell versus supercell encodings of the same ideal linear periodic chain.

## New prototype file

```text
src/msbp_tg/periodic_fiber.py
```

It implements a conservative prototype:

```text
periodic_msbp(smiles)
periodic_msbp_density(smiles)
periodic_invariance_table(smiles_list)
```

## New tests

```text
tests/test_periodic_representation_invariance.py
```

The tests enforce:

```text
1. the old naive coordinate is representation-sensitive on the editorial blocker examples;
2. the new periodic prototype maps *CC*, *CCCC*, and *CCCCCC* to the same pMSBP value;
3. the representation class is stable as *CC*;
4. the exported invariance table schema is stable.
```

## New script

```text
scripts/run_periodic_invariance_gate.py
```

Expected output:

```text
PASS: *CC*, *CCCC*, and *CCCCCC* map to the same pMSBP coordinate.
```

Expected CSV output:

```text
results/periodic_msbp_invariance_gate.csv
```

## Scientific caution

This is a first hard gate, not the final polymer graph descriptor. It is currently valid for simple two-terminal repeat-unit invariance testing. Complex copolymers, aromatic systems, branching, stereochemistry, tacticity, and full periodic graph canonicalization remain future work.

## Next required gates

1. orientation reversal invariance;
2. cut-point relocation invariance;
3. equivalent canonical SMILES invariance;
4. primitive cell versus supercell invariance beyond carbon chains;
5. copolymer unit expansion;
6. re-extraction of features for all three sources;
7. cluster-aware re-analysis.
