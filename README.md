# Mobility Suppression Boundary Principle for polymer Tg

Public-safe preprint package for the MSBP-Tg reproducibility workflow.

This repository contains the manuscript, supplementary methods, figures, tests, public-safe summary tables, and reproducibility scripts for the Mobility Suppression Boundary Principle (MSBP) analysis of polymer glass-transition boundary placement.

## Key files

- `manuscript/MSBP_Tg_Journal_Manuscript.docx`
- `manuscript/MSBP_Tg_Journal_Manuscript.pdf`
- `supplementary/Supplementary_Methods.pdf`
- `docs/REPRODUCIBILITY.md`
- `data/license_audit.md`
- `scripts/`
- `src/msbp_tg/`
- `tests/`

## Public-safe data policy

This repository does not redistribute raw third-party datasets or row-level third-party-derived SMILES/Tg tables. It includes public-safe aggregate summaries, source instructions, reproducibility code, and documentation.

## Install and run checks

Run from the repository root:

```bash
python -m pip install -e .
python -m pytest -q
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
```

Expected result: the editable package installs, tests pass, and public-safety checks pass.

## Release order

Create the public GitHub repository, create a preprint-candidate release, archive it with Zenodo, insert the real DOI and repository URL into the manuscript and metadata, re-render the PDF, and only then upload the final PDF to ChemRxiv.
