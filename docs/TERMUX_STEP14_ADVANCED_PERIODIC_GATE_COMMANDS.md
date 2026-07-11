# Termux Commands — Apply Step 14 Advanced Periodic Invariance Gate

Run from the repository root:

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

Unzip the Step-14 patch package:

```bash
unzip -o /sdcard/Download/MSBP_Tg_step14_advanced_periodic_invariance_gate_patch.zip -d ~/msbp_step14_tmp
```

Copy files into the repository:

```bash
rsync -av ~/msbp_step14_tmp/MSBP_Tg_step14_advanced_periodic_invariance_gate/ ./
```

Install package without rebuilding pandas dependencies:

```bash
python -m pip install -e . --no-deps
```

Run the Step-14 gate script:

```bash
python scripts/run_periodic_advanced_invariance_gate.py
```

If pytest is available, run only the Step-14 tests:

```bash
python -m pytest -q tests/test_periodic_advanced_invariance.py
```

Commit and push:

```bash
git status --short
git add src/msbp_tg/periodic_fiber.py tests/test_periodic_advanced_invariance.py scripts/run_periodic_advanced_invariance_gate.py docs/STEP14_ADVANCED_PERIODIC_INVARIANCE_GATE_REPORT.md docs/TERMUX_STEP14_ADVANCED_PERIODIC_GATE_COMMANDS.md
git commit -m "Add advanced periodic MSBP invariance gates"
git push origin main
```

Check GitHub Actions:

```bash
gh run list --repo htetkokokonaing-dev/msbp-tg --limit 5
```

If green, create release:

```bash
gh release create v1.3.0-advanced-periodic-gates \
  --repo htetkokokonaing-dev/msbp-tg \
  --target main \
  --title "MSBP-Tg advanced periodic invariance gates v1.3.0" \
  --notes "Adds Step-14 advanced periodic MSBP invariance gates: orientation reversal, cut-point relocation, simple spelling equivalence, non-carbon supercells, and simple copolymer expansion. This is a descriptor-validation gate, not a journal-submission release."
```

Optional: archive generated output CSV after running the gate:

```bash
git add results/periodic_msbp_advanced_invariance_gate.csv
git commit -m "Archive Step 14 advanced periodic gate outputs"
git push origin main
```
