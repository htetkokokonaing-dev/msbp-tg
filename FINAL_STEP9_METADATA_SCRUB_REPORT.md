# Final Step 9 - PDF/DOCX Metadata Scrub Report

## Purpose
This pass scrubbed hidden DOCX/PDF metadata only. It did not recompute scientific results, alter public-safe data policy, change Figure 4, or modify the MSBP-Tg analysis code.

## Metadata updates

### Main manuscript
- DOCX/PDF title: `Mobility Suppression Boundary Principle for Polymer Glass-Transition Temperature`
- DOCX/PDF author: `Htet Ko Ko Naing`
- DOCX/PDF subject: `Preprint manuscript with public-safe reproducibility package.`
- Removed hidden internal subject wording: `MSBP-Tg release-compliance candidate`

### Supplementary Methods
- DOCX/PDF title: `Supplementary Methods for MSBP-Tg Reproducibility Package`
- DOCX/PDF author: `Htet Ko Ko Naing`
- DOCX/PDF subject: `Supplementary methods for public-safe reproducibility package.`
- Removed hidden `python-docx` author metadata.

## Verification

```text
python -m pip install -e .: PASS
pytest: 38 passed
PUBLIC RELEASE SAFETY CHECK: PASS
Public-safe repo check: PASS
Main PDF metadata internal-wording scan: PASS
Supplement PDF metadata internal-wording scan: PASS
Main PDF broken filename text scan: PASS
Supplement PDF broken filename text scan: PASS
Main manuscript PDF: 8 pages
Supplementary Methods PDF: 4 pages
Blank pages: 0
```

## Preserved fixes

```text
mean/median residualization alignment: preserved
row-level SMILES/Tg removal: preserved
synthetic Figure 4: preserved
.zenodo.json: preserved
installable package workflow: preserved
page numbers: preserved
layout alignment: preserved
broken filename reference cleanup: preserved
```

## Next public-release step
Upload the cleaned repository to GitHub, create a GitHub release, obtain a Zenodo DOI, then replace the temporary Code Availability wording with resolved GitHub/Zenodo citation details and re-render the final ChemRxiv PDF.
