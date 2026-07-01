# Changelog

## Preprint release package

- Aligned manuscript residualization wording with the public code: main protocol is within-fiber mean-centering.
- Added mean-vs-median residual-centering sensitivity results.
- Removed row-level third-party-derived representative SMILES/Tg CSVs from the public repository.
- Replaced Figure 4 with synthetic illustrative motifs that are not redistributed source rows.
- Added public data-rights notes and `data/license_audit.md`.
- Hardened public-safety checks with CSV header scanning for structural identifiers plus Tg-like target fields.
- Renamed Zenodo metadata to `.zenodo.json` and removed the legacy non-dot metadata filename.
- Updated `CITATION.cff` as software metadata.
- Preserved public-safe code, aggregate result tables, tests, figures, and manuscript files.
- Cleaned release/deployment documentation so public-facing instructions use a single version policy.

## Planned DOI-bearing release

After GitHub and Zenodo DOI creation, update persistent identifiers and create final release `final DOI-bearing release`.

## Step 6 PDF compliance polish

- Added page numbers, updated title-page version wording, reflowed table layout, and removed pending DOI/URL language from the manuscript PDF.
- Added conservative practical design-workflow implications to the manuscript without changing code, data, or validation results.
