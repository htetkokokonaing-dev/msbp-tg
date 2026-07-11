# Figure and Table Alignment Map - MSBP-Tg Journal Submission

Status: STEP 8 alignment map

## Figure files

- Figure 1: `figures/figure1_theory_schematic.png` - PASS
- Figure 2: `figures/figure2_three_source_residual_scatter.png` - PASS
- Figure 3: `figures/figure3_shuffle_control_entropy.png` - PASS
- Figure 4: `figures/figure4_representative_repeat_unit_structures.png` - PASS

## Public-safe table files

- main_result_summary: `results/three_source_recomputed_summary.csv` - PASS. Main source-level residual association summary.
- S1: `tables/residual_centering_sensitivity.csv` - PASS. Mean-vs-median residual-centering sensitivity.
- S2: `tables/bootstrap_ci_spearman.csv` - PASS. Spearman bootstrap intervals by source.
- S3: `tables/entropy_shuffle_empirical_p.csv` - PASS. Shuffle-control entropy-gain empirical p-values.
- S4: `tables/known_descriptor_comparison_compact.csv` - PASS. Compact known-descriptor comparison.
- S5: `tables/paired_descriptor_bootstrap_ring_summary.csv` - PASS. Paired bootstrap summary for ring alternatives.
- S6: `tables/effect_size_slope_compact.csv` - PASS. Compact effect-size slope table.
- S7: `tables/contradiction_taxonomy_source_summary.csv` - PASS. Contradiction taxonomy by source.
- S8: `tables/source_role_notes.csv` - PASS. Source-role interpretation notes.

## Manuscript image-link audit

- `../figures/figure1_theory_schematic.png` -> PASS (243536 bytes)
- `../figures/figure2_three_source_residual_scatter.png` -> PASS (385791 bytes)
- `../figures/figure3_shuffle_control_entropy.png` -> PASS (145773 bytes)
- `../figures/figure4_representative_repeat_unit_structures.png` -> PASS (179151 bytes)

## Manuscript table-reference audit

- `residual_centering_sensitivity.csv` referenced in manuscript: PASS
- `bootstrap_ci_spearman.csv` referenced in manuscript: PASS
- `entropy_shuffle_empirical_p.csv` referenced in manuscript: PASS
- `known_descriptor_comparison_compact.csv` referenced in manuscript: PASS
- `paired_descriptor_bootstrap_ring_summary.csv` referenced in manuscript: PASS
- `effect_size_slope_compact.csv` referenced in manuscript: PASS
- `contradiction_taxonomy_source_summary.csv` referenced in manuscript: PASS
- `source_role_notes.csv` referenced in manuscript: PASS
- `three_source_recomputed_summary.csv` referenced in manuscript: PASS

## Submission note

The manuscript now identifies the public-safe CSV files that support figure and table statements. The release keeps row-level third-party records out of the public repository and uses source documentation plus aggregate validation tables for journal-safe reproducibility.

## Guard test

`tests/test_figure_table_alignment.py` checks manuscript image links and required public-safe table references.
