# GitHub and Zenodo deployment guide

This guide prepares the MSBP-Tg public-safe preprint package for a citable software DOI.

## 1. Final local checks

Run from the repository root:

```bash
python -m pip install -e .
python -m pytest -q
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
```

Confirm that no raw third-party datasets or row-level third-party-derived SMILES/Tg tables are included.

## 2. Create the GitHub repository

Recommended repository name:

```text
MSBP-Tg
```

Suggested description:

```text
Public-safe reproducibility package for the Mobility Suppression Boundary Principle of polymer Tg.
```

Push the repository using `docs/github_upload_commands.md`.

## 3. Create a preprint-candidate release

Suggested tag:

```text
preprint-candidate
```

Suggested release title:

```text
MSBP-Tg preprint candidate
```

Use `RELEASE_NOTES.md` as the release body.

## 4. Zenodo DOI workflow

After the GitHub repository is public and the release is created, connect the repository to Zenodo and archive the release. This repository uses `.zenodo.json` for Zenodo metadata and `CITATION.cff` for GitHub citation metadata.

## 5. DOI insertion pass

After Zenodo assigns a DOI, update:

- `README.md`
- `CITATION.cff`
- `.zenodo.json`
- manuscript Data and Code Availability statement
- release notes and deployment docs if needed

Then re-render the manuscript PDF.

## 6. Final DOI release

After DOI insertion, create the final release:

```text
final DOI-bearing release
```

Use the DOI-updated PDF for ChemRxiv or journal submission.
