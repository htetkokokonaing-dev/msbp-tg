# Final Step 8 - Filename Reference Cleanup and Micro-Polish

## Scope

This was a targeted cleanup pass after the final release audit. It does not recompute scientific results and does not change the public-code protocol, row-level data policy, synthetic Figure 4 treatment, or metadata structure.

## Changes made

### Rendered manuscript and supplement references

Corrected broken filename references in the DOCX sources and re-rendered PDFs:

- `tables/known_descriptor_comparison__clean.csv` -> `tables/known_descriptor_comparison_clean.csv`
- `tables/paired_descriptor_bootstrap_.csv` -> `tables/paired_descriptor_bootstrap.csv`
- `tables/contradiction_taxonomy_by_source_.csv` -> `tables/contradiction_taxonomy_by_source.csv`
- `tables/residual_centering_sensitivity_.csv` -> `tables/residual_centering_sensitivity.csv`

### Public wording polish

- README duplicate wording was simplified to: `Public-safe preprint package for the MSBP-Tg reproducibility workflow.`
- `.zenodo.json` notes now use public-facing metadata language and no longer say `Release-compliance metadata candidate`.
- `data/license_audit.md` title no longer contains empty parentheses.

### Guard added

Added `tests/test_final_filename_reference_cleanup.py` to prevent these broken filename references and public-wording regressions from reappearing in public text and DOCX sources.

## Verification

- Editable install: PASS
- Test suite: 38 passed
- Public release safety check: PASS
- Public-safe repo check: PASS
- Rendered main manuscript PDF: 8 pages
- Rendered supplementary methods PDF: 4 pages
- Blank pages: 0
- Broken filename references in rendered PDF text: PASS / none found
- Row-level SMILES/Tg regression scan: PASS / none found
- Broken command/path regression scan: PASS / none found
- Previous fixes preserved: mean-centered residualization, mean-vs-median sensitivity, public-safe data policy, synthetic Figure 4, `.zenodo.json`, installable package, page numbers, and layout alignment.

## Recommended next step

Use this cleaned package for GitHub repository creation. After the first public GitHub release and Zenodo DOI minting, update README, CITATION.cff, .zenodo.json, and manuscript Code Availability with the real GitHub URL and Zenodo DOI, then re-render the final ChemRxiv PDF.
