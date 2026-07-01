# Data license and redistribution audit

This repository is designed as a public-safe reproducibility package. Raw third-party datasets are not bundled. Row-level third-party-derived SMILES/Tg records are not redistributed in CSV form unless permission is explicit.

## Source-family handling

| Source family | Role in manuscript | Bundled raw rows? | Bundled row-level SMILES/Tg? | Public release handling |
|---|---|---:|---:|---|
| tsaicying polymer Tg repository | Broad leak-excluded Tg source | No | No | Cite source and provide acquisition instructions; aggregate validation summaries only. |
| NeurIPS/Open Polymer Prediction released Tg-known subset | Benchmark-style directional check | No | No | Cite source and provide acquisition instructions; aggregate validation summaries only. |
| Leeds PAEK / University of Leeds Research Data | Family-narrow PAEK stress test | No | No | Cite publication and data archive; aggregate validation summaries only. |
| Screening-only sources | Overlap/source-screening context | No | No | Not counted as independent validation unless documented; no raw redistribution. |

## Figure policy

Figure 4 uses synthetic illustrative motifs drawn with RDKit. These motifs are schematic chemical examples of mobility-suppression mechanisms and are not redistributed row-level records from third-party datasets.

## Reviewer reproduction note

Full reruns require the user to obtain each external dataset independently and place it under the paths described in `data/README_data_public_safe.md` and `docs/REPRODUCIBILITY.md` or the future supplementary methods. Scripts intentionally avoid overwriting locked aggregate summaries when external data are absent.

## Public-safe checks

The release checker scans for cache files, private paths, bundled raw-data folders, and CSV headers that combine structural identifiers such as SMILES with Tg-like target fields. Such files are blocked from public release unless a future explicit license audit permits redistribution.
