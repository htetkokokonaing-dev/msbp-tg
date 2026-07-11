# Changelog

## v1.1.0-journal-submission

- Locked Journal of Cheminformatics as the primary target journal.
- Revised the title and abstract for public-safe cheminformatics validation framing.
- Added explicit claim-boundary language: not a universal Tg law, not a newly invented molecular descriptor, and not a replacement for experimental Tg measurement.
- Strengthened related work and references for polymer informatics, cheminformatics, Tg prediction, reproducibility, and FAIR-data context.
- Hardened data provenance documentation, including external source register, raw-data exclusion notes, local processed-table paths, and license audit notes.
- Added one-command public-safe audit wrapper: `reproduce.sh`.
- Verified editable install, public tests, public release safety, and public-safe repository checks.
- Added explicit figure/table alignment documentation and tests.
- Updated root GitHub and Zenodo metadata after ChemRxiv posting.

## Public DOI-bearing preprint state

- ChemRxiv preprint: https://doi.org/10.26434/chemrxiv.15005629/v1
- Zenodo software/archive DOI: https://doi.org/10.5281/zenodo.21100020
- GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

## Preprint release package

- Aligned manuscript residualization wording with the public code: main protocol is within-fiber mean-centering.
- Added mean-vs-median residual-centering sensitivity results.
- Removed row-level third-party-derived representative SMILES/Tg CSVs from the public repository.
- Replaced Figure 4 with synthetic illustrative motifs that are not redistributed source rows.
- Added public data-rights notes and `data/license_audit.md`.
- Hardened public-safety checks with CSV header scanning for structural identifiers plus Tg-like target fields.
- Updated `CITATION.cff` as software metadata.
- Preserved public-safe code, aggregate result tables, tests, figures, and manuscript files.
