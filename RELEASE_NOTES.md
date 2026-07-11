# Release notes: journal-submission-ready public-safe package

Recommended tag: `v1.1.0-journal-submission`

This release provides the journal-submission-ready public-safe reproducibility package for MSBP-Tg, prepared for submission to **Journal of Cheminformatics** as a Research Article.

## Public identifiers

- ChemRxiv preprint: https://doi.org/10.26434/chemrxiv.15005629/v1
- Zenodo software/archive DOI: https://doi.org/10.5281/zenodo.21100020
- GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

## Scope

MSBP-Tg is presented as a public-safe cheminformatics validation study of a mobility-suppression coordinate for polymer glass-transition temperature. It is not presented as a universal Tg law, a newly invented molecular descriptor, or a replacement for experimental measurement.

## Included

- Journal-submission manuscript DOCX/PDF/Markdown.
- Supplementary Methods DOCX/PDF/Markdown.
- Public-safe figures and aggregate validation tables.
- Source-family and data-provenance documentation.
- Public-safe reproducibility scripts, tests, and `reproduce.sh`.
- Journal of Cheminformatics cover letter and checklist.
- Step 1–10 journal-preparation reports.

## Public-safe data policy

Raw third-party datasets and row-level third-party-derived SMILES/Tg records are not redistributed. Source links, acquisition notes, license-status notes, and preprocessing documentation are provided under `data/` and `docs/`.

## Verification summary

- Public test suite: 47 passed.
- Public release safety check: PASS.
- Public-safe repository check: PASS.
- Figure/table alignment guard: PASS.
- Metadata consistency guard: PASS.

## Journal-preparation status

Steps 1–10 are complete through GitHub/Zenodo release workflow preparation. The actual GitHub release must be created from the public repository using the Termux commands in `docs/termux_release_commands_step10.md`.
