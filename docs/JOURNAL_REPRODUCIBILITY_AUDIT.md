# Journal Reproducibility Audit — MSBP-Tg

This document summarizes the public-safe reproducibility audit for the MSBP-Tg journal submission package.

## Public reproducibility scope

The public repository supports reproduction of the released code checks, aggregate validation-table consistency, public-safe safety gates, descriptor/fiber utility tests, metadata tests, and manuscript/package consistency checks.

It does **not** redistribute raw third-party datasets or row-level third-party-derived SMILES/Tg records. Those materials must be obtained from their original providers under their original terms.

## One-command audit

From the repository root:

```bash
bash reproduce.sh
```

This command runs:

```bash
python -m pip install -e . --no-deps
python -m pytest -q -p no:cacheprovider
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
python scripts/run_stage10_11_13_summary.py
```

## Verified results

| Check | Verified result |
|---|---:|
| Package editable install | PASS |
| Test suite | 42 passed |
| Public release safety check | PASS |
| Public-safe repository check | PASS |
| Source-family summary rerun without private feature tables | Controlled skip; locked summaries preserved |

## Interpretation for reviewers

The repository is designed so that journal reviewers can evaluate the public analysis layer without receiving non-redistributable raw records. Aggregate validation tables, source-role notes, contradiction taxonomy tables, source manifests, figures, and code are public-safe.

For full local source-family reruns, reviewers should independently acquire the external source datasets, prepare the documented local feature tables, and then rerun the stage summary script.

## Required local feature tables for full rerun

```text
data/processed/stage10_tsaicying_leak_excluded_novel_features.csv
data/processed/stage11_neurips_public_private_tg_known_novel_features.csv
data/processed/stage13_leeds_paek_novel_features.csv
```

These files are intentionally absent from the public repository.

## Safety boundary

The public release safety gate checks for private-path leakage, compiled Python artifacts, known private development filenames, and public-release hazards. The public-safe repository gate checks for row-level third-party SMILES/Tg table risks and forbidden external data placement patterns.

Both gates pass.
