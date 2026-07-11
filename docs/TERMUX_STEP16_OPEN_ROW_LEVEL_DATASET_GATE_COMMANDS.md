# Termux Commands — Apply Step 16 Open Row-Level Dataset Strategy Gate

Run from the repository root:

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

Make sure PolyMetriX is downloaded:

```bash
ls -lh data/open_row_level/LAMALAB_CURATED_Tg_structured_polymerclass.csv
head -n 2 data/open_row_level/LAMALAB_CURATED_Tg_structured_polymerclass.csv
```

Unzip the Step-16 patch:

```bash
unzip -o /sdcard/Download/MSBP_Tg_step16_open_row_level_dataset_gate_patch.zip -d ~/msbp_step16_tmp
```

Copy into repository:

```bash
rsync -av ~/msbp_step16_tmp/MSBP_Tg_step16_open_row_level_dataset_gate/ ./
```

Install package without rebuilding dependencies:

```bash
python -m pip install -e . --no-deps
```

Run Step 16:

```bash
python scripts/run_open_dataset_strategy_gate.py
```

If pytest is available:

```bash
python -m pytest -q tests/test_step16_open_dataset_strategy_gate.py
```

Commit and push:

```bash
git status --short
git add src/msbp_tg/open_dataset_audit.py scripts/run_open_dataset_strategy_gate.py tests/test_step16_open_dataset_strategy_gate.py docs/STEP16_OPEN_ROW_LEVEL_DATASET_GATE_REPORT.md docs/TERMUX_STEP16_OPEN_ROW_LEVEL_DATASET_GATE_COMMANDS.md README_STEP16_OPEN_ROW_LEVEL_DATASET_GATE_PATCH.md SHA256_MANIFEST_STEP16.csv
git add results/step16_open_row_level_dataset_gate || true
git commit -m "Add open row-level dataset strategy gate"
git push origin main
```

Check CI:

```bash
gh run list --repo htetkokokonaing-dev/msbp-tg --limit 5
```

If green, create release:

```bash
gh release create v1.5.0-open-row-level-dataset-gate \
  --repo htetkokokonaing-dev/msbp-tg \
  --target main \
  --title "MSBP-Tg open row-level dataset gate v1.5.0" \
  --notes "Adds Step-16 open row-level dataset strategy gate for Option C. Audits PolyMetriX row-level Tg data and current pMSBP parser coverage. This is a dataset-strategy gate, not a journal-submission release."
```
