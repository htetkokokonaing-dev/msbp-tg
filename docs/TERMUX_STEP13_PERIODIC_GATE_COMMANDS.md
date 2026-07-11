# Termux Commands — Apply Step 13 Periodic Descriptor Gate

Run from the repository root:

```bash
cd ~/msbp_upload/MSBP_Tg_final_release_ready
```

Unzip the Step-13 patch package:

```bash
unzip -o /sdcard/Download/MSBP_Tg_step13_periodic_descriptor_gate_patch.zip -d /tmp/msbp_step13
```

Copy files into the repository:

```bash
rsync -av /tmp/msbp_step13/MSBP_Tg_step13_periodic_descriptor_gate/ ./
```

Install package without rebuilding pandas dependencies:

```bash
python -m pip install -e . --no-deps
```

Run only the Step-13 gate script:

```bash
python scripts/run_periodic_invariance_gate.py
```

Run only the Step-13 test file if pytest is available:

```bash
python -m pytest -q tests/test_periodic_representation_invariance.py
```

Commit and push:

```bash
git add src/msbp_tg/periodic_fiber.py tests/test_periodic_representation_invariance.py scripts/run_periodic_invariance_gate.py docs/STEP13_PERIODIC_MSBP_DESCRIPTOR_GATE_REPORT.md
git commit -m "Add periodic MSBP representation-invariance gate"
git push origin main
```

Then check GitHub Actions:

```bash
gh run list --repo htetkokokonaing-dev/msbp-tg --limit 5
```

If green, create a gate release:

```bash
gh release create v1.2.0-periodic-descriptor-gate \
  --repo htetkokokonaing-dev/msbp-tg \
  --target main \
  --title "MSBP-Tg periodic descriptor gate v1.2.0" \
  --notes "Adds a first periodic MSBP representation-invariance gate. This is a descriptor-validation gate, not a journal-submission release."
```
