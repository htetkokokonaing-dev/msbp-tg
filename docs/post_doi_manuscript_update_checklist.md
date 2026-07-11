# Post-DOI manuscript update checklist

After Zenodo issues the DOI:

1. Copy the DOI from the Zenodo record.
2. Update `README.md` with the repository URL and DOI.
3. Update `CITATION.cff` with the DOI and repository URL.
4. Update `.zenodo.json` related identifiers if appropriate.
5. Update the manuscript Data and Code Availability section with:
   - GitHub repository URL
   - Zenodo DOI
   - third-party data source statement
6. Re-render manuscript DOCX to PDF.
7. Run the full test suite and public-safety checks.
8. Regenerate `data/manifest.csv`.
9. Create final release tag `final DOI-bearing release`.
10. Use the DOI-updated PDF for ChemRxiv or journal submission.
