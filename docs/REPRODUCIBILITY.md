# Reproducibility Guide - MSBP-Tg 

This repository is a public-safe journal-submission package. It contains code, aggregate validation outputs, manuscript files, figures, and documentation. It does not redistribute raw third-party datasets or row-level third-party-derived SMILES/Tg tables.

## 1. Environment setup

Recommended local setup:

```bash
conda env create -f environment.yml
conda activate msbp-tg
python -m pip install -e .
python -m pytest -q
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
```

Expected checks:

```text
pytest: tests pass
public release safety check: PASS
public-safe repo check: PASS
```



## 1.1 One-command public-safe audit

From the repository root, run:

```bash
bash reproduce.sh
```

The audit performs editable local installation, runs the complete public test suite, runs public-release safety checks, runs the public-safe repository/data-rights check, and executes the three-source summary script in safe public mode.

Expected public-safe audit result:

```text
42 tests passed
PUBLIC RELEASE SAFETY CHECK: PASS
Public-safe check passed.
Source-family summary script: controlled skip when private feature tables are absent; locked aggregate summaries are not overwritten.
```

See `docs/JOURNAL_REPRODUCIBILITY_AUDIT.md` and `docs/STEP7_CODE_REPRODUCIBILITY_AUDIT_REPORT.md` for the recorded Step 7 audit.

## 2. Raw data policy

Raw source datasets are not bundled. To reproduce external-source validation, obtain each source directly from its original provider and follow the provider's license and redistribution terms. Keep raw files outside the public repository unless you have explicit redistribution rights.

The public repository intentionally omits:

- raw third-party source tables;
- row-level SMILES/Tg validation tables;
- representative source-row case tables;
- private development paths and intermediate private packages.

## 3. Source acquisition record

For each source, record at minimum:

```text
source_name:
provider:
access_date:
source_url_or_doi:
local_raw_filename:
license_or_terms_checked:
notes:
```

The release includes `data/external_sources.csv`, `data/external_sources.md`, `data/license_audit.md`, `data/raw/README.md`, and `data/processed/README.md` for source-role, local-reproduction, and redistribution notes.


## 3.1 Expected local feature-table paths

After independent source acquisition and private preprocessing, place local feature tables at these paths if you want to rerun the three-source validation summary:

```text
 data/processed/stage10_tsaicying_leak_excluded_novel_features.csv
 data/processed/stage11_neurips_public_private_tg_known_novel_features.csv
 data/processed/stage13_leeds_paek_novel_features.csv
```

These files are intentionally absent from the public release because they may contain row-level third-party-derived structural/property records. The public release provides aggregate validation outputs instead.

## 4. Feature extraction from user-supplied SMILES

Prepare a CSV with a SMILES column. Then run:

```bash
python scripts/extract_features_from_smiles.py --input input.csv --smiles-col SMILES --out features.csv
```

The output includes RDKit-derived descriptors and the locked MSBP density axis:

```text
mobility_suppression_density = -NumRotatableBonds / heavy_atoms
```

## 5. Visible-fiber construction

When a dataset has a polymer class or family label, use it as the family component. Otherwise, the public feature-derived heuristic assigns a simple family class from silicon, aromatic rings, heteroatoms, or hydrocarbon-like status. The family component is combined with a heavy-atom quantile size bin to form `visible_fiber`.

## 6. Validation from a user-supplied feature table

Given a feature table with a target Tg column, an axis column, and a fiber column:

```bash
python scripts/validate_feature_table.py --input features.csv --axis mobility_suppression_density --t Tg_C --fiber visible_fiber --out validation_summary.csv
```

Small tables can produce undefined residual rank statistics. This is expected when each fiber contains too few rows or when residual vectors are constant.

## 7. Residualization protocol

The main public protocol subtracts the within-fiber mean:

```text
Tg_residual = Tg - mean(Tg within fiber)
axis_residual = axis - mean(axis within fiber)
```

A mean-vs-median sensitivity table is included at:

```text
tables/residual_centering_sensitivity.csv
```

## 8. Locked aggregate summaries

The repository includes aggregate validation summaries for auditability. These summaries are not raw-data substitutes. The script `scripts/run_stage10_11_13_summary.py` will not overwrite locked summaries with empty output when local source files are absent.

## 9. Public-safe release zip

To build a public-safe release zip:

```bash
python scripts/make_release_zip.py --out ../MSBP_Tg_release.zip
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
```

The release zip builder excludes cache directories, bytecode, local render artifacts, and known private-development filenames.

## 10. Known limitations

- Full source reproduction requires external data acquisition.
- Exact overlap screening uses canonical structure keys when parseable; it is not a fuzzy near-duplicate screen.
- Visible fibers are reproducible analysis strata, not a complete polymer taxonomy.
- MSBP density is not a new descriptor; it is the sign-reversed rotatable-bond density used as a boundary-coordinate axis.
