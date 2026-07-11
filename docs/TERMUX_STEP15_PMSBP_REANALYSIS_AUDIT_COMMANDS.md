# Termux Commands — Apply Step 15 pMSBP Re-analysis Audit

Run from the repository root:

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

Unzip the Step-15 patch:

```bash
unzip -o /sdcard/Download/MSBP_Tg_step15_pmsbp_refeature_reanalysis_audit_patch.zip -d ~/msbp_step15_tmp
```

Copy into the repository:

```bash
rsync -av ~/msbp_step15_tmp/MSBP_Tg_step15_pmsbp_refeature_reanalysis_audit/ ./
```

Install package without rebuilding dependencies:

```bash
python -m pip install -e . --no-deps
```

Run Step 15:

```bash
python scripts/run_pmsbp_reanalysis_audit.py
```

If pytest is available:

```bash
python -m pytest -q tests/test_step15_pmsbp_reanalysis_audit.py
```

Commit and push:

```bash
git status --short
git add src/msbp_tg/pmsbp_reanalysis.py scripts/run_pmsbp_reanalysis_audit.py tests/test_step15_pmsbp_reanalysis_audit.py docs/STEP15_PMSBP_REANALYSIS_AUDIT_REPORT.md docs/TERMUX_STEP15_PMSBP_REANALYSIS_AUDIT_COMMANDS.md
git add results/step15_pmsbp_reanalysis_audit || true
git commit -m "Add pMSBP refeature reanalysis audit"
git push origin main
```

Check CI:

```bash
gh run list --repo htetkokokonaing-dev/msbp-tg --limit 5
```

If green, create release:

```bash
gh release create v1.4.0-pmsbp-reanalysis-audit \
  --repo htetkokokonaing-dev/msbp-tg \
  --target main \
  --title "MSBP-Tg pMSBP reanalysis audit v1.4.0" \
  --notes "Adds Step-15 pMSBP re-feature/re-analysis audit. This gate checks whether public-safe row-level SMILES/Tg tables exist for full pMSBP re-analysis; it is not a journal-submission release."
```
