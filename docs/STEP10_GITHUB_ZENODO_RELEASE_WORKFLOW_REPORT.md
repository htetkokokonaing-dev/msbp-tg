# Step 10 Report — GitHub Release and Zenodo Version Update Preparation

**Project:** MSBP-Tg  
**Target journal:** Journal of Cheminformatics  
**Recommended release tag:** `v1.1.0-journal-submission`  
**Status:** PASS — release workflow prepared, not executed from this environment

---

## 1. What Step 10 completed

Step 10 prepared the GitHub release and Zenodo version-update workflow for the journal-submission-ready package.

Created or updated:

- `docs/termux_release_commands_step10.md`
- `docs/release_body_copy_paste.md`
- `docs/zenodo_after_release_checklist.md`
- `docs/zenodo_metadata_copy_paste.md`
- `docs/journal_submission_checklist_after_chemrxiv.md`
- `RELEASE_NOTES.md`
- `CHANGELOG.md`
- `data/manifest.csv`

---

## 2. Public identifiers retained

- ChemRxiv preprint: https://doi.org/10.26434/chemrxiv.15005629/v1
- Zenodo software/archive DOI: https://doi.org/10.5281/zenodo.21100020
- GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

---

## 3. Recommended GitHub release

```text
Tag: v1.1.0-journal-submission
Title: MSBP-Tg journal-submission-ready release v1.1.0
Release notes file: docs/release_body_copy_paste.md
Target branch: main
```

---

## 4. Termux command file

The exact command sequence for the user's local Termux environment is stored in:

```text
docs/termux_release_commands_step10.md
```

This includes:

1. entering the repository;
2. running tests and public-safe checks;
3. committing Step 10 files;
4. creating the annotated Git tag;
5. creating the GitHub release through `gh release create`;
6. verifying the release;
7. checking Zenodo ingestion.

---

## 5. Verification performed in this preparation environment

```text
pytest: 47 passed
public release safety check: PASS
public-safe repo check: PASS
```

---

## 6. Important limitation

This environment cannot publish to the user's GitHub or Zenodo accounts. Therefore Step 10 prepared the release workflow and files, but the real GitHub release and Zenodo update must be performed by the user in Termux or GitHub web UI.

---

## 7. Next step

After the GitHub release and Zenodo version update are confirmed, proceed to:

```text
Step 11 — Journal files final package
```

