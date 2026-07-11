# STEP 6 - Data provenance hardening report

## Status

PASS - data provenance and raw-data redistribution boundaries were strengthened for Journal of Cheminformatics review.

## Files added or strengthened

- `data/external_sources.csv`
- `data/external_sources.md`
- `data/README_data_public_safe.md`
- `data/license_audit.md`
- `data/raw/README.md`
- `data/processed/README.md`
- `data/external/README.md`
- `docs/data_availability_statement.md`
- `docs/data_provenance_protocol.md`
- `docs/source_acquisition_template.csv`
- `docs/REPRODUCIBILITY.md`
- `README.md`
- manuscript Data Availability and Code Availability sections

## Reviewer-facing improvement

The journal version now makes the public-safe reproducibility boundary explicit. It distinguishes:

1. public aggregate evidence included in the repository;
2. raw third-party datasets that are not redistributed;
3. local feature-table paths needed for full source-family reruns;
4. source license and acquisition notes;
5. the difference between public verification and raw-data mirroring.

## Public-safe claim boundary

The repository remains public-safe. It does not bundle raw third-party datasets or row-level third-party-derived structural/property tables. It provides aggregate validation outputs, source registers, code, tests, figures, and reproduction instructions.

## Next step

Step 7 - Code reproducibility audit.
