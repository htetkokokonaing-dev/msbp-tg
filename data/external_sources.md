# External source notes

The public-safe package does not redistribute raw third-party datasets. The validation evidence was built from source families that users must reacquire under the original source terms.

1. `tsaicying/polymer-tg-predictor` GitHub repository: broad public Tg source used to construct the leak-excluded novel subset. This repository is cited in the manuscript as a source repository; derived summary tables are provided, but raw rows are not redistributed here.
2. NeurIPS / Open Polymer Prediction 2025: Kaggle competition source and released Tg-known public/private test data. The post-competition Open Polymer Challenge report is cited alongside the Kaggle data page.
3. Leeds PAEK source family: Brierley-Croft et al. Macromolecules article and the associated University of Leeds Research Data archive, DOI 10.5518/1596. This source is treated as a family-narrow PAEK stress test.

Additional screening sources included PolyMetriX/LAMALAB, Figshare `with_Tg`, ViditAg, and RAK2315 repositories, but not all were counted as independent post-lock source families.

Before any public release or journal submission, re-check each data source license, access date, and citation requirement.

##  data-rights note

This public package does not redistribute raw third-party datasets or row-level third-party-derived SMILES/Tg tables. Validation evidence is provided as aggregate statistics and source-role summaries. Full reproduction requires independently obtaining external datasets under their own licenses and terms. See `data/license_audit.md`.
