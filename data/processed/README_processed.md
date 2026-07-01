# Processed validation tables

This public-safe repository does not redistribute row-level processed feature tables derived from third-party Tg datasets.

To reproduce the validation tables locally:

1. Download the external source files listed in `data/external_sources.md`.
2. Place them under `data/external/` using the recommended filenames in `data/external/README.md`.
3. Run the preparation and validation scripts in `scripts/`.

The repository includes summary-level results under `results/`, but not third-party SMILES/Tg row tables unless redistribution permission is confirmed.
