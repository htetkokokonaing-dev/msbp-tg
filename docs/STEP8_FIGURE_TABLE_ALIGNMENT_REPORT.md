# Step 8 - Figure/Table Alignment Report

**Status:** PASS

## Actions completed

1. Audited all manuscript image links and confirmed that Figure 1-Figure 4 files exist in `figures/`.
2. Replaced ambiguous table wording with explicit supplementary table/file references.
3. Added Section 5.6, `Public-safe figure and table alignment`, to the manuscript.
4. Added `docs/figure_table_alignment.md` as a persistent reviewer-facing file map.
5. Added `tests/test_figure_table_alignment.py` to guard against missing figure links and missing public-safe table files.
6. Filled previously under-specified Results subsections with explicit references to Supplementary Tables S5-S7.
7. Rebuilt DOCX/PDF manuscript files and performed render QA.

## Figures checked

- Figure 1: `figures/figure1_theory_schematic.png`
- Figure 2: `figures/figure2_three_source_residual_scatter.png`
- Figure 3: `figures/figure3_shuffle_control_entropy.png`
- Figure 4: `figures/figure4_representative_repeat_unit_structures.png`

## Table files locked for submission

- Main summary: `results/three_source_recomputed_summary.csv`
- Supplementary Table S1: `tables/residual_centering_sensitivity.csv`
- Supplementary Table S2: `tables/bootstrap_ci_spearman.csv`
- Supplementary Table S3: `tables/entropy_shuffle_empirical_p.csv`
- Supplementary Table S4: `tables/known_descriptor_comparison_compact.csv`
- Supplementary Table S5: `tables/paired_descriptor_bootstrap_ring_summary.csv`
- Supplementary Table S6: `tables/effect_size_slope_compact.csv`
- Supplementary Table S7: `tables/contradiction_taxonomy_source_summary.csv`
- Supplementary Table S8: `tables/source_role_notes.csv`

## QA results

- Manuscript figure links: PASS
- Required table files exist: PASS
- Required table files are referenced in the manuscript: PASS
- Empty Results subsection check: PASS
- DOCX render QA: PASS
- PDF render QA: PASS
- `pytest -q`: 44 passed

## Verdict

Step 8 passes. The journal submission package now has explicit figure and table mapping, reducing the risk of upload mismatch, missing supplemental table ambiguity, or reviewer confusion about public-safe CSV support files.
