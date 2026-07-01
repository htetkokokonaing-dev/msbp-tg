# Public-safe data note

This public-safe package does not redistribute raw third-party datasets or processed feature tables derived from them. Use `data/external_sources.md` and the scripts in `scripts/` to re-acquire permitted source files and regenerate validation feature tables locally.

Current source roles are:

- broad leak-excluded Tg source: `tsaicying/polymer-tg-predictor`;
- benchmark-style check: NeurIPS / Open Polymer Prediction 2025 released Tg-known test data;
- family-narrow stress test: Leeds PAEK source family associated with Brierley-Croft et al. and University of Leeds Research Data DOI 10.5518/1596.

Before public release, verify every data source license, access date, and citation requirement.

## Manifest note

`data/manifest.csv` records the public repository contents at package-build time. The manifest may intentionally exclude itself or use a post-generation audit note, because hashing a manifest that includes its own final hash is self-referential.

##  data-rights note

This public package does not redistribute raw third-party datasets or row-level third-party-derived SMILES/Tg tables. Validation evidence is provided as aggregate statistics and source-role summaries. Full reproduction requires independently obtaining external datasets under their own licenses and terms. See `data/license_audit.md`.
