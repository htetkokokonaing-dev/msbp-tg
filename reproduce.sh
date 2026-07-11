#!/usr/bin/env bash
set -euo pipefail

# Public-safe one-command reproducibility audit for the MSBP-Tg repository.
# This checks the local package, test suite, public-release safety, and
# public-safe data-rights boundary. It does not download or redistribute raw
# third-party datasets.

python -m pip install -e . --no-deps
python -m pytest -q -p no:cacheprovider
python scripts/check_public_release_safety.py
python scripts/check_public_safe_repo.py
python scripts/run_stage10_11_13_summary.py
