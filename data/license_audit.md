# Data license and redistribution audit

This repository is designed as a public-safe journal-submission package. Raw third-party datasets are not bundled. Row-level third-party-derived structural/property records are not redistributed unless permission is explicit.

## Public handling by source family

| Source family | Role in manuscript | Bundled raw rows? | Bundled row-level structural/property table? | Public release handling |
|---|---|---:|---:|---|
| tsaicying polymer Tg repository | Broad leak-excluded source-family check | No | No | Cite source, document access, provide aggregate validation summaries only. |
| NeurIPS/Open Polymer Prediction released known-label subset | Benchmark-style directional check | No | No | Cite source/data page, document access, provide aggregate validation summaries only. |
| Leeds PAEK / University of Leeds Research Data | Family-narrow PAEK stress test | No | No | Cite publication/data archive, provide aggregate validation summaries only. |
| Screening-only sources | Overlap/source-screening context | No | No | Not counted as independent validation unless documented; no raw redistribution. |

## Source register

The source register is provided in two forms:

- `data/external_sources.csv` for machine-readable source metadata;
- `data/external_sources.md` for human-readable source notes and reproduction boundaries.

## Figure policy

Figure 4 uses synthetic illustrative motifs drawn with RDKit. These motifs are schematic chemical examples of mobility-suppression mechanisms and are not redistributed row-level records from third-party datasets.

## Reviewer reproduction note

Full source reruns require readers to obtain each external dataset independently and prepare local feature tables under `data/processed/` as documented in `data/processed/README.md`. The public scripts intentionally avoid overwriting locked aggregate summaries when external data are absent.

## Public-safe checks

The public-safe checker scans for cache files, private paths, bundled raw-data folders, and CSV headers that combine structural identifiers with Tg-like target fields. Such files are blocked from public release unless a future explicit license audit permits redistribution.
