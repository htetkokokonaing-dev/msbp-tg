# Mobility Suppression Boundary Principle for Polymer Glass-Transition Temperature: A Public-Safe Cheminformatics Validation Study

This repository contains the public-safe manuscript, supplementary methods, figures, aggregate tables, tests, and reproducibility scripts for the MSBP-Tg journal-submission package.

## Current public records

- ChemRxiv preprint: https://doi.org/10.26434/chemrxiv.15005629/v1
- Zenodo software/archive DOI: https://doi.org/10.5281/zenodo.21100020
- GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

## Journal-submission framing

MSBP-Tg is positioned as a public-safe cheminformatics validation study of an interpretable mobility-suppression coordinate for polymer glass-transition temperature (Tg). The contribution is not a universal Tg law, not a newly invented molecular descriptor, and not a replacement for experimental Tg measurement. MSBP density is defined transparently as `-NumRotatableBonds/heavy_atoms` and is evaluated as a within-fiber boundary coordinate.

## Key submission files

- `manuscript/MSBP_Tg_Journal_Submission_Manuscript.docx`
- `manuscript/MSBP_Tg_Journal_Submission_Manuscript.pdf`
- `supplementary/Supplementary_Methods.pdf`
- `docs/cover_letter_journal_of_cheminformatics.docx`
- `docs/journal_submission_checklist_after_chemrxiv.md`
- `docs/JOURNAL_REPRODUCIBILITY_AUDIT.md`
- `docs/figure_table_alignment.md`
- `data/external_sources.csv`
- `data/external_sources.md`
- `data/license_audit.md`

## Public-safe data policy

Raw third-party datasets and row-level third-party-derived SMILES/Tg records are not redistributed in this repository. Source links, acquisition notes, license-status notes, and preprocessing documentation are provided in `data/external_sources.csv`, `data/external_sources.md`, `data/README_data_public_safe.md`, `data/raw/README.md`, and `data/processed/README.md`.

The public repository contains aggregate validation summaries, source-role notes, figures, tables, tests, and reproducibility scripts intended for public release.

## Install and run checks

Run from the repository root:

```bash
python -m pip install -e .
python -m pytest -q
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
```

Expected result: the editable package installs, tests pass, and public-safety checks pass.

## One-command public-safe reproducibility audit

Reviewers can run:

```bash
bash reproduce.sh
```

This installs the local package in editable mode, runs the public test suite, runs both public-safety checks, and verifies that the source-family summary script behaves safely when non-redistributable raw/processed third-party feature tables are absent.

Latest public-safe audit result: `44 passed`; public release safety check `PASS`; public-safe repository check `PASS`.

## Figure and table alignment

The journal submission package includes explicit manuscript-to-file mapping for Figures 1-4 and Supplementary Tables S1-S8. See `docs/figure_table_alignment.md`.

## Citation

For the manuscript, cite the ChemRxiv preprint: https://doi.org/10.26434/chemrxiv.15005629/v1

For the code and public-safe reproducibility package, cite the Zenodo archive: https://doi.org/10.5281/zenodo.21100020
