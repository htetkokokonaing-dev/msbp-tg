# Public-safe data policy

This repository is a public-safe journal-submission and reproducibility package. It does not redistribute raw third-party datasets or row-level third-party-derived structural/property tables.

The public release includes:

- source provenance documentation;
- license and redistribution notes;
- aggregate validation summaries;
- source-role notes;
- figures;
- tests;
- reproducibility scripts;
- manuscript and supplementary files.

The public release intentionally excludes:

- raw third-party source tables;
- locally prepared feature tables generated from third-party sources;
- row-level structural/property records;
- private intermediate files and development paths.

## Source register

Use `data/external_sources.csv` as the machine-readable source register and `data/external_sources.md` as the human-readable source register.

## Local reproduction

To reproduce the source-family validation, users must obtain external datasets directly from the original providers and follow the license or access terms of those providers. Locally prepared feature tables should be placed under `data/processed/` with the names listed in `data/processed/README.md`.

## Manifest note

`data/manifest.csv` records public repository contents at package-build time. It is a release-integrity aid, not a raw-data inventory. It may intentionally exclude itself or use a post-generation audit note because hashing a manifest that includes its own final hash is self-referential.
