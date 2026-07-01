# Reproducibility protocol

1. Acquire raw data from documented public sources.
2. Preserve original files and hashes.
3. Clean and canonicalize polymer SMILES/repeat-unit SMILES; record RDKit version (`rdkit.__version__`) and descriptor script commit/version.
4. Remove exact canonical overlaps with pre-lock source sets.
5. Define comparable fibers using chemistry/family label plus size bin.
6. Compute RDKit-derived descriptors and mobility axes:
   - rotatable-bond suppression count: `-rotatable_bonds`,
   - normalized rotatable suppression density: `-rotatable_bonds / heavy_atoms`.
7. Residualize Tg and mobility axis within each visible fiber by subtracting the within-fiber mean. Median-centering is a sensitivity check, not the main public-code protocol.
8. Evaluate:
   - Spearman correlation between mobility residual and Tg residual,
   - top/bottom quartile sign accuracy,
   - entropy reduction versus shuffled controls,
   - baseline model R2 deltas.
9. Export contradiction cases and source scorecards.
10. Do not add new formula terms after the frozen protocol unless a new version is declared.
