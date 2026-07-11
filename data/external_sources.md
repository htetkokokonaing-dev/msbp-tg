# External data source register

This file is the public-facing source provenance register for the MSBP-Tg journal-submission package. The repository does **not** redistribute raw third-party datasets or row-level third-party-derived structural/property tables. It documents where external data must be obtained, how each source family is used, and why only public-safe aggregate outputs are included in the release.

A machine-readable register is provided at `data/external_sources.csv`.

## Evidence source families

| Source ID | Source family | Role in manuscript | Public package handling |
|---|---|---|---|
| D1_tsaicying_polymer_tg_repository | Broad public Tg source | Broad leak-excluded validation source | Raw rows omitted; aggregate summaries only. |
| D2_neurips_open_polymer_prediction_2025 | Benchmark-style polymer-property source | Released known-label check | Raw rows omitted; Stage 11 aggregate summaries only. |
| D3_leeds_paek_source_family | Family-narrow PAEK stress test | Independent family-narrow check | Raw rows omitted; Stage 13 aggregate summaries only. |

## Screening-only sources

PolyMetriX/LAMALAB-related sources, Figshare `with_Tg`, ViditAg, and RAK2315 repositories were used only for overlap/source-screening context unless separately documented. They are not counted as independent post-lock validation domains in the main claim.

## Reproduction boundary

Full source reproduction requires the reader to reacquire each source from the original provider and to follow the source-specific license or access terms. Locally prepared feature tables should be placed under `data/processed/` using the file names documented in `data/processed/README.md`. These local feature tables must not be committed to the public repository unless redistribution permission is explicit.

The released manuscript conclusions are supported publicly by aggregate validation summaries, source-role notes, figures, tests, and reproducibility scripts. This is a public-safe reproducibility package, not a redistribution mirror for third-party datasets.
