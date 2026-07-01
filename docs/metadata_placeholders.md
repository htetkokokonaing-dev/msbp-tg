# Metadata and placeholder policy ()

Persistent identifiers are intentionally controlled and deferred until public infrastructure exists.

Current policy:

- Zenodo metadata file: `.zenodo.json`
- Legacy non-dot metadata filename: intentionally absent
- Citation metadata file: `CITATION.cff`
- `CITATION.cff` type: `software`
- `.zenodo.json` license identifier: `mit`
- `.zenodo.json` language: `eng`
- `related_identifiers`: updated with the GitHub repository and release URL. Zenodo DOI: https://doi.org/10.5281/zenodo.21100020

After the first public release, update the following in one controlled pass:

1. README repository URL and DOI
2. `CITATION.cff` repository-code and DOI
3. `.zenodo.json` related identifiers
4. Manuscript Code Availability statement
5. Release notes and Zenodo deposition metadata
