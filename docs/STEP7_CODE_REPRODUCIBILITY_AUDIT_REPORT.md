# Step 7 — Code Reproducibility Audit Report

**Project:** MSBP-Tg journal submission package  
**Target journal:** Journal of Cheminformatics  
**Step:** 7 of 12  
**Status:** PASS

---

## 1. Purpose

Step 7 checks whether the public-safe code package is runnable, installable, testable, and aligned with the journal-submission reproducibility claims.

The audit is deliberately limited to public-safe materials. It does not download, bundle, or redistribute raw third-party datasets or row-level third-party-derived SMILES/Tg records.

---

## 2. Commands audited

The following commands were run from the repository root:

```bash
python -m pip install -e . --no-deps
python -m pytest -q -p no:cacheprovider
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
python scripts/run_stage10_11_13_summary.py
python -m compileall -q src scripts
```

A one-command public-safe audit wrapper was also added:

```bash
bash reproduce.sh
```

---

## 3. Results

| Gate | Result |
|---|---:|
| Editable package install | PASS |
| Pytest suite | 42 passed |
| Public release safety check | PASS |
| Public-safe data-rights check | PASS |
| Python compile check for `src/` and `scripts/` | PASS |
| Three-source summary script behavior without private feature tables | Controlled public-safe skip; locked summaries not overwritten |

---

## 4. Public-safe behavior of source-family rerun script

The script `scripts/run_stage10_11_13_summary.py` was executed in the public-safe repository. Because raw/processed third-party feature tables are intentionally not bundled, the script reported missing local feature-table paths and did not overwrite existing locked aggregate summaries.

This is the intended behavior for the public journal package.

Expected local feature-table paths for private/full reruns are documented in:

- `data/processed/README.md`
- `docs/REPRODUCIBILITY.md`
- `docs/reproducibility_protocol.md`
- `docs/data_provenance_protocol.md`

---

## 5. Files added or updated in Step 7

- Added `reproduce.sh`
- Added `docs/JOURNAL_REPRODUCIBILITY_AUDIT.md`
- Added `docs/STEP7_CODE_REPRODUCIBILITY_AUDIT_REPORT.md`
- Updated `README.md`
- Updated `docs/REPRODUCIBILITY.md`
- Updated `docs/journal_submission_checklist_after_chemrxiv.md`
- Updated `data/manifest.csv`

---

## 6. Journal-readiness interpretation

The package now provides a clear public-safe reproducibility story:

1. Reviewers can install the local package.
2. Reviewers can run all public tests.
3. Reviewers can run public-release safety checks.
4. Reviewers can inspect aggregate evidence tables.
5. Reviewers can see why raw third-party records are not redistributed.
6. Reviewers can follow documented source-acquisition paths for full local reruns.

This is sufficient for the public-safe code audit gate. Full raw-data reruns still require independent acquisition of third-party datasets under their original terms.

---

## 7. Step 7 decision

**PASS.**

The public-safe code reproducibility layer is now journal-ready for the next step.

**Next step:** Step 8 — Figures and tables journal-alignment audit.
