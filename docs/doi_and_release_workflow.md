# DOI and release workflow

## Current status

This public-safe preprint package now has resolved release identifiers.

GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

GitHub release: https://github.com/htetkokokonaing-dev/msbp-tg/releases/tag/v1.0.1-preprint

Zenodo DOI: https://doi.org/10.5281/zenodo.21100020

## Recommended release sequence

1. Create a public GitHub repository, recommended name `MSBP-Tg`.
2. Push this repository after local tests and public-safety checks pass.
3. Create a preprint-candidate GitHub release with tag `preprint-candidate`.
4. Enable Zenodo GitHub integration and archive that release.
5. The Zenodo DOI has been copied into:
   - `README.md`
   - `CITATION.cff`
   - `.zenodo.json` related identifiers if appropriate
   - manuscript Data and Code Availability statement
6. Re-render the manuscript PDF after DOI insertion.
7. Create the final DOI-bearing repository release `final DOI-bearing release`.
8. Use the DOI-updated PDF for ChemRxiv or journal submission.

## DOI wording for manuscript

Use this template after DOI assignment:

```text
The code and public-safe reproducibility package are archived at Zenodo: DOI: [insert DOI]. The repository contains original code, manuscript materials, public-source acquisition instructions, aggregate validation outputs, and public-safe summary tables. Raw third-party datasets and row-level third-party-derived SMILES/Tg tables are not redistributed.
```
