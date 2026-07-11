# Termux Commands — Apply Step 17 PSMILES Parser Extension Gate

Run from the repository root:

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

Confirm PolyMetriX exists:

```bash
ls -lh data/open_row_level/LAMALAB_CURATED_Tg_structured_polymerclass.csv
```

Unzip the Step-17 patch:

```bash
unzip -o /sdcard/Download/MSBP_Tg_step17_psmiles_parser_extension_gate_patch.zip -d ~/msbp_step17_tmp
```

Copy into the repository:

```bash
rsync -av ~/msbp_step17_tmp/MSBP_Tg_step17_psmiles_parser_extension_gate/ ./
```

Install package without rebuilding dependencies:

```bash
python -m pip install -e . --no-deps
```

Run Step 17:

```bash
python scripts/run_psmiles_parser_extension_gate.py
```

If pytest is available:

```bash
python -m pytest -q tests/test_step17_psmiles_parser_extension_gate.py
```

Commit and push:

```bash
git status --short
git add src/msbp_tg/psmiles_parser.py scripts/run_psmiles_parser_extension_gate.py tests/test_step17_psmiles_parser_extension_gate.py docs/STEP17_PSMILES_PARSER_EXTENSION_GATE_REPORT.md docs/TERMUX_STEP17_PSMILES_PARSER_EXTENSION_GATE_COMMANDS.md README_STEP17_PSMILES_PARSER_EXTENSION_GATE_PATCH.md SHA256_MANIFEST_STEP17.csv
git add results/step17_psmiles_parser_extension_gate || true
git commit -m "Add PSMILES parser extension gate"
git push origin main
```

Check CI:

```bash
gh run list --repo htetkokokonaing-dev/msbp-tg --limit 5
```

If green, create release:

```bash
gh release create v1.6.0-psmiles-parser-extension-gate \
  --repo htetkokokonaing-dev/msbp-tg \
  --target main \
  --title "MSBP-Tg PSMILES parser extension gate v1.6.0" \
  --notes "Adds Step-17 PSMILES-aware pMSBP parser extension gate for PolyMetriX open row-level data. This is a parser/coverage gate, not a journal-submission release."
```
