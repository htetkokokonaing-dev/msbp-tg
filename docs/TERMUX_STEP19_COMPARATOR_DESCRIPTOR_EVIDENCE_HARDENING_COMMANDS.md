# Termux Commands - Step 19 Comparator Descriptor Evidence Hardening

Run from repository root:

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

Confirm Step 18 exists:

```bash
cat results/step18_open_data_pmsbp_reanalysis/step18_reanalysis_verdict.csv
```

Unzip Step 19 patch:

```bash
unzip -o /sdcard/Download/MSBP_Tg_step19_comparator_descriptor_evidence_hardening_patch.zip -d ~/msbp_step19_tmp
```

Copy into repository:

```bash
rsync -av ~/msbp_step19_tmp/MSBP_Tg_step19_comparator_descriptor_evidence_hardening/ ./
```

Install without rebuilding dependencies:

```bash
python -m pip install -e . --no-deps
```

Fast smoke audit:

```bash
python scripts/run_comparator_evidence_hardening.py --n-bootstrap 50
```

Standard audit:

```bash
python scripts/run_comparator_evidence_hardening.py --n-bootstrap 200
```

Inspect key outputs:

```bash
cat results/step19_comparator_descriptor_evidence_hardening/step19_journal_evidence_hardening_verdict.csv
head -n 20 results/step19_comparator_descriptor_evidence_hardening/descriptor_univariate_association_summary.csv
cat results/step19_comparator_descriptor_evidence_hardening/incremental_residual_linear_model_summary.csv
head -n 20 results/step19_comparator_descriptor_evidence_hardening/pmsbp_redundancy_vs_comparators.csv
```

If pytest is available:

```bash
python -m pytest -q tests/test_step19_comparator_evidence_hardening.py
```

Commit and push:

```bash
git status --short
git add src/msbp_tg/comparator_evidence.py scripts/run_comparator_evidence_hardening.py tests/test_step19_comparator_evidence_hardening.py docs/STEP19_COMPARATOR_DESCRIPTOR_EVIDENCE_HARDENING_REPORT.md docs/TERMUX_STEP19_COMPARATOR_DESCRIPTOR_EVIDENCE_HARDENING_COMMANDS.md README_STEP19_COMPARATOR_DESCRIPTOR_EVIDENCE_HARDENING_PATCH.md SHA256_MANIFEST_STEP19.csv
git add results/step19_comparator_descriptor_evidence_hardening || true
git commit -m "Add comparator descriptor evidence hardening"
git push origin main
```

Check CI:

```bash
gh run list --repo htetkokokonaing-dev/msbp-tg --limit 5
```

If green, create release:

```bash
gh release create v1.8.0-comparator-evidence-hardening \
  --repo htetkokokonaing-dev/msbp-tg \
  --target main \
  --title "MSBP-Tg comparator evidence hardening v1.8.0" \
  --notes "Adds Step-19 comparator descriptor and journal-evidence hardening. Compares pMSBP against available PolyMetriX descriptor columns, residual associations, class-cluster bootstrap, redundancy, and incremental residual linear models. This is an evidence-hardening audit, not a journal-submission release."
```
