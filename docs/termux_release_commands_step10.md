# Step 10 Termux Commands — GitHub Release + Zenodo Version Update

**Repository:** `https://github.com/htetkokokonaing-dev/msbp-tg`  
**Recommended tag:** `v1.1.0-journal-submission`  
**Release title:** `MSBP-Tg journal-submission-ready release v1.1.0`

This file is for the real Termux/GitHub action. Run these commands only after the Step 10 package has been copied into the local repository and all files are committed.

---

## A. Enter the local repository

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

## B. Check branch and status

```bash
git status
git branch --show-current
```

You should be on `main` or the branch you plan to release from. For journal submission, release from `main` after committing the Step 10 files.

## C. Run final local checks

```bash
python -m pytest -q
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
bash reproduce.sh
```

Expected results:

```text
47 passed
PUBLIC RELEASE SAFETY CHECK: PASS
Public-safe check passed.
reproduce.sh completed without error
```

## D. Commit Step 10 files

```bash
git add .
git commit -m "Prepare journal-submission release workflow"
git push origin main
```

If Git says `nothing to commit`, continue to the tag step.

## E. Create and push the Git tag

```bash
git tag -a v1.1.0-journal-submission -m "MSBP-Tg journal-submission-ready release v1.1.0"
git push origin v1.1.0-journal-submission
```

## F. Create the GitHub release with GitHub CLI

```bash
gh release create v1.1.0-journal-submission   --repo htetkokokonaing-dev/msbp-tg   --target main   --title "MSBP-Tg journal-submission-ready release v1.1.0"   --notes-file docs/release_body_copy_paste.md
```

## G. Verify the GitHub release

```bash
gh release view v1.1.0-journal-submission --repo htetkokokonaing-dev/msbp-tg
```

Also check the browser:

```text
https://github.com/htetkokokonaing-dev/msbp-tg/releases/tag/v1.1.0-journal-submission
```

## H. Zenodo update check

After the GitHub release is published, wait for Zenodo to ingest the release.

Check:

```text
https://zenodo.org/account/settings/github/
```

Then open the `htetkokokonaing-dev/msbp-tg` record in Zenodo uploads and confirm that the new version appears.

## I. If Zenodo creates a new version DOI

Record the new version DOI here:

```text
Zenodo concept DOI: https://doi.org/10.5281/zenodo.21100020
Zenodo version DOI for v1.1.0-journal-submission: [paste here after Zenodo finishes]
```

For the manuscript, the concept DOI is acceptable because it resolves to the version chain. If the journal form asks for the exact archived version, use the new version DOI.

## J. If Zenodo does not update automatically

Do not create duplicate records immediately. First check that the repository switch is ON in Zenodo GitHub settings. If it is ON but no record appears after a reasonable wait, use the existing Zenodo record page to inspect errors or re-sync if the UI provides that option.

