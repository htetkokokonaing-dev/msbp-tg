# Data provenance protocol for journal review

## Purpose

This document explains how the MSBP-Tg package handles third-party data provenance for journal review while avoiding redistribution of raw third-party datasets or row-level third-party-derived structural/property tables.

## Public files

The public repository provides:

- `data/external_sources.csv`: machine-readable source register;
- `data/external_sources.md`: human-readable source register;
- `data/license_audit.md`: source-family redistribution audit;
- `data/raw/README.md`: raw-data exclusion and local-use note;
- `data/processed/README.md`: expected local feature-table filenames;
- `docs/REPRODUCIBILITY.md`: commands for checks and local reruns;
- `results/three_source_recomputed_summary.csv`: locked aggregate source summary;
- `tables/`: public-safe aggregate tables used by the manuscript.

## Local reproduction sequence

1. Obtain external datasets directly from their original providers.
2. Check and record the current license or access terms for each source.
3. Keep raw and locally processed row-level data outside version control.
4. Prepare local feature tables with the names listed in `data/processed/README.md`.
5. Run `python scripts/run_stage10_11_13_summary.py` to regenerate source-family aggregate summaries.
6. Run `python -m pytest -q` and the public-safe checks before release or journal upload.

## Boundary of public reproducibility

The public package supports verification of manuscript-level aggregate evidence, code behavior, source-role documentation, and public-safe table consistency. It is not a public redistribution mirror for third-party source datasets. This boundary is intentional and is part of the reproducibility claim.
