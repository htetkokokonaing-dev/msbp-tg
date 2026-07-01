# MSBP-Tg Reproducibility Protocol 

## Purpose

This protocol defines the public-safe reproducibility route for the Mobility Suppression Boundary Principle of Polymer Tg. Raw third-party datasets are not redistributed; full reproduction requires independent acquisition under original source terms.

## Inputs

Each input dataset must contain polymer structure strings and Tg values. Preferred structure formats are polymer SMILES, repeat-unit SMILES, BigSMILES, or manually mapped repeat-unit strings.

## Preprocessing

1. Parse structure strings into valid molecular graphs where possible.
2. Canonicalize structures.
3. Convert Tg units to a common scale; Celsius is used for human-readable summaries, Kelvin may be retained internally.
4. Aggregate exact duplicate canonical structures using median Tg.
5. Screen overlap against prior datasets before counting a source as post-lock support.

## Fiber construction

Group structures by comparable chemistry/class and coarse size. The exact grouping can vary by source, but it must be declared before metric reporting.

## Locked MSBP axes

- mobility_suppression_count = - rotatable_bonds
- mobility_suppression_density = - rotatable_bonds / heavy_atoms

The density axis is preferred for cross-size comparison.

## Primary tests

1. Spearman correlation between within-fiber Tg residual and MSBP residual.
2. Strong-quartile sign accuracy.
3. Conditional entropy gain compared with shuffled mobility-axis controls.
4. Cross-validated model delta: family/size-only baseline versus family/size plus MSBP axis.

## Reporting

Report every source, including exclusions and weak-margin results. Report contradiction taxonomy in aggregate/source-level form. Do not redistribute row-level third-party SMILES/Tg case tables unless permissions are explicitly verified.
