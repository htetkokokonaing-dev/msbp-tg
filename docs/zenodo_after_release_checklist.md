# Zenodo After-Release Checklist — MSBP-Tg v1.1.0-journal-submission

## Required checks

- [ ] GitHub release exists: `v1.1.0-journal-submission`.
- [ ] Zenodo GitHub integration remains ON for `htetkokokonaing-dev/msbp-tg`.
- [ ] Zenodo created or updated the software/archive record for the new release.
- [ ] Title matches the journal-submission title.
- [ ] Creator name and ORCID are correct.
- [ ] License is MIT for original code/documentation.
- [ ] ChemRxiv DOI is listed as a related identifier: https://doi.org/10.26434/chemrxiv.15005629/v1
- [ ] GitHub repository is listed as a related identifier: https://github.com/htetkokokonaing-dev/msbp-tg
- [ ] Concept DOI remains recorded: https://doi.org/10.5281/zenodo.21100020
- [ ] New version DOI, if assigned, is copied into the journal submission notes.

## DOI policy for journal submission

Use this DOI in the manuscript Data and Code Availability section unless a journal form specifically asks for an exact release-version DOI:

```text
https://doi.org/10.5281/zenodo.21100020
```

Use the version-specific DOI only after Zenodo creates it for `v1.1.0-journal-submission`.

## Do not do this

- Do not create a duplicate Zenodo record unless the GitHub integration fails and cannot be repaired.
- Do not upload raw third-party datasets.
- Do not replace the ChemRxiv DOI with the Zenodo DOI; they identify different public records.

