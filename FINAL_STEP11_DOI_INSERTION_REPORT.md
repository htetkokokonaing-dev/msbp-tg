# Final Step 11 - DOI insertion and GitHub Actions patch report

## Resolved public identifiers

- GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg
- GitHub release: https://github.com/htetkokokonaing-dev/msbp-tg/releases/tag/v1.0.1-preprint
- Zenodo DOI: https://doi.org/10.5281/zenodo.21100020

## Changes made

- Inserted the resolved GitHub repository URL and Zenodo DOI into README.md.
- Updated CITATION.cff with version `v1.0.1-preprint`, DOI, URL, and repository-code fields.
- Updated `.zenodo.json` notes and related identifiers.
- Replaced the manuscript Code Availability placeholder with resolved GitHub and Zenodo citation details.
- Re-rendered the DOI-bearing manuscript PDF from the updated DOCX.
- Preserved the public-safe data policy: raw third-party datasets and row-level third-party-derived SMILES/Tg records are not redistributed.
- Applied the GitHub Actions patch to `src/msbp_tg/fiber.py` for degenerate size-bin handling.
- Updated metadata tests so post-DOI citation metadata is expected rather than treated as a placeholder.

## Verification results

```text
python -m pip install -e .: PASS
python -m pytest -q -p no:cacheprovider: 39 passed
python scripts/check_public_release_safety.py: PASS
python scripts/check_public_safe_repo.py .: PASS
DOCX render to PDF: PASS
Main manuscript PDF: 9 pages
Blank pages observed in render: 0
PDF text check for GitHub repository and Zenodo DOI: PASS
```

## ChemRxiv use

Use the DOI-bearing PDF at `manuscript/MSBP_Tg_Journal_Manuscript.pdf` for ChemRxiv after final human review.
