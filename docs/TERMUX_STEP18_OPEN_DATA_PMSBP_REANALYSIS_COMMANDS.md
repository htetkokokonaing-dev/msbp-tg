# Termux Commands — Apply Step 18 Open-data pMSBP Re-analysis

Run from the repository root:

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

Confirm Step 17 passed:

```bash
cat results/step17_psmiles_parser_extension_gate/polymetrix_psmiles_parser_coverage_summary.csv
```

Unzip Step 18 patch:

```bash
unzip -o /sdcard/Download/MSBP_Tg_step18_open_data_pmsbp_statistical_reanalysis_patch.zip -d ~/msbp_step18_tmp
```

Copy into the repository:

```bash
rsync -av ~/msbp_step18_tmp/MSBP_Tg_step18_open_data_pmsbp_statistical_reanalysis/ ./
```

Install without rebuilding dependencies:

```bash
python -m pip install -e . --no-deps
```

Run a fast audit first:

```bash
python scripts/run_open_data_pmsbp_reanalysis.py --n-bootstrap 50 --n-permutation 50
```

If that succeeds, run the standard audit:

```bash
python scripts/run_open_data_pmsbp_reanalysis.py --n-bootstrap 200 --n-permutation 200
```

Inspect key outputs:

```bash
cat results/step18_open_data_pmsbp_reanalysis/overall_pmsbp_association_summary.csv
cat results/step18_open_data_pmsbp_reanalysis/bootstrap_uncertainty_summary.csv
cat results/step18_open_data_pmsbp_reanalysis/within_class_permutation_summary.csv
cat results/step18_open_data_pmsbp_reanalysis/step18_reanalysis_verdict.csv
head -n 20 results/step18_open_data_pmsbp_reanalysis/polymer_class_stratified_summary.csv
```

If pytest is available:

```bash
python -m pytest -q tests/test_step18_open_data_pmsbp_reanalysis.py
```

Commit and push:

```bash
git status --short
git add src/msbp_tg/open_data_reanalysis.py scripts/run_open_data_pmsbp_reanalysis.py tests/test_step18_open_data_pmsbp_reanalysis.py docs/STEP18_OPEN_DATA_PMSBP_REANALYSIS_REPORT.md docs/TERMUX_STEP18_OPEN_DATA_PMSBP_REANALYSIS_COMMANDS.md README_STEP18_OPEN_DATA_PMSBP_REANALYSIS_PATCH.md SHA256_MANIFEST_STEP18.csv
git add results/step18_open_data_pmsbp_reanalysis || true
git commit -m "Add open-data pMSBP statistical reanalysis"
git push origin main
```

Check CI:

```bash
gh run list --repo htetkokokonaing-dev/msbp-tg --limit 5
```

If green, create release:

```bash
gh release create v1.7.0-open-data-pmsbp-reanalysis \
  --repo htetkokokonaing-dev/msbp-tg \
  --target main \
  --title "MSBP-Tg open-data pMSBP statistical reanalysis v1.7.0" \
  --notes "Adds Step-18 open-row-level PolyMetriX pMSBP statistical re-analysis with class stratification, within-class residualization, row bootstrap, class-cluster bootstrap, within-class permutation, and leave-one-class-out sensitivity. This is an analysis audit, not a journal-submission release."
```
