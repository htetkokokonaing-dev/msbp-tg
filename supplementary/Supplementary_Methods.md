# Supplementary Methods for MSBP-Tg 

**Title:** Mobility Suppression Boundary Principle for Polymer Glass Transition Placement

**Author:** Htet Ko Ko Naing, Independent Researcher, ORCID: 0009-0000-6140-0495

**Purpose.** This supplement expands the reproducibility and methods details for the manuscript. It does not redistribute third-party raw datasets or row-level SMILES/Tg records. Full independent reproduction requires obtaining source datasets from their original providers and following their terms.

## S1. Source acquisition and public-data instructions

Three external-source roles are used in the manuscript: a broad public Tg table, a NeurIPS Open Polymer Prediction Tg subset, and a Leeds PAEK family-narrow stress test. The public repository does not bundle raw third-party datasets. Users must obtain each source from the original provider, record the acquisition date, preserve unmodified source files outside the public repository, and run the feature/validation scripts on locally acquired copies.

For public redistribution, the repository includes aggregate summaries, locked validation tables, code, figures, and public-safe documentation. It intentionally omits raw source rows, row-level polymer SMILES/Tg tables, and third-party-derived representative case tables.

## S2. Leak-exclusion and overlap-key definition

Overlap screening uses canonicalized structure identifiers when raw repeat-unit SMILES can be parsed. The intended overlap key is the RDKit canonical SMILES of the repeat unit after the same preprocessing used for feature extraction. Exact canonical-key matches against pre-lock structures are excluded from post-lock validation subsets. Rows that cannot be parsed by RDKit are excluded from raw-SMILES feature validation rather than assigned an inferred structure.

This is an exact-structure exclusion rule, not a fuzzy chemical-similarity de-duplication rule. It is conservative for direct duplicate leakage, but it does not claim to remove every possible near-duplicate, homologous series relationship, or literature-derived data dependency.

## S3. SMILES canonicalization and dummy atom handling

RDKit is used for parsing, canonicalization, and descriptor extraction. Polymer repeat-unit dummy atoms represented by `*` are retained when RDKit can parse the string. The public implementation treats dummy atoms as atomic number 0. They may appear in the molecular graph used by RDKit, but they are not chemical heavy atoms in the usual carbon/heteroatom sense. Therefore, denominator definitions and public explanations refer to the implementation trace rather than a claim of universal polymer descriptor semantics.

Rows with invalid or unparseable SMILES are marked invalid and are not used in raw-SMILES axis validation. No manual structure correction is performed in the public protocol.

## S4. Feature extraction and MSBP density identity

For a parseable repeat-unit SMILES, the public feature extractor computes heavy atom count, molecular weight, rotatable bonds, total rings, aromatic rings, aliphatic rings, heteroatoms, silicon atoms, and density-normalized descriptor variants.

The locked MSBP density axis is:

`MSBP_density = -NumRotatableBonds / heavy_atoms`

This is the suppression-oriented sign reversal of rotatable-bond density. The paper's contribution is not a new molecule-level descriptor. The contribution is the use of normalized local mobility suppression as a within-fiber Tg boundary coordinate, tested with residualization, shuffle controls, descriptor comparisons, and source-separated validation.

## S5. Fiber construction rules

A visible fiber is a reproducible comparison stratum. When a dataset provides a polymer-family or polymer-class label, that label is used as the family component. When a dataset lacks such a label, a simple feature-derived family heuristic is used:

1. one or more silicon atoms -> `silicon_like`
2. two or more aromatic rings -> `multi_aromatic`
3. one aromatic ring -> `aromatic`
4. one or more heteroatoms -> `hetero_aliphatic`
5. otherwise -> `hydrocarbon_like`

The family component is combined with a quantile size bin based on heavy-atom count. The default size binning uses five quantile bins with duplicate-edge handling. A fiber is therefore a practical analysis stratum, not a complete polymer taxonomy.

## S6. Minimum fiber-size handling

Residualization is defined within visible fibers. Very small fibers can produce unstable or undefined rank associations after residualization. The public validation routines return `NaN` for Spearman correlation when there are fewer than three paired residual values or when either residual vector is constant. User-facing validation scripts warn when fiber counts are too small for stable residual rank association.

The manuscript source-level summaries were computed on screened validation subsets large enough to support the reported source-level statistics. Small ad hoc input tables should be interpreted as feature-extraction checks rather than full validation tests.

## S7. Residualization protocol and mean-vs-median sensitivity

The main public protocol residualizes both Tg and descriptor axes by subtracting the within-fiber mean:

`residual = value - mean(value within visible fiber)`

A sensitivity check was added because earlier manuscript wording referred to median centering. The direction of the association is stable under both centering choices in the three locked summaries. The public repository reports the sensitivity table in `tables/residual_centering_sensitivity.csv`.

Summary of the locked sensitivity values:

| Source | Mean-centered rho | Median-centered rho |
|---|---:|---:|
| Stage 10 broad Tg source | 0.745 | 0.744 |
| Stage 11 NeurIPS Tg subset | 0.551 | 0.531 |
| Stage 13 Leeds PAEK stress test | 0.828 | 0.832 |

Mean-centering remains the main reported protocol because it matches the public code path and all locked main tables.

## S8. Entropy label definition and binning

The entropy-control analysis evaluates whether axis bins reduce uncertainty in a high-Tg boundary label. When a source-specific high-boundary label is not supplied, the public validation function constructs a within-table label using the median Tg value. The descriptor axis is binned with quantile bins using duplicate-edge handling. Entropy gain is computed as parent binary entropy minus the weighted average child entropy across axis bins.

This analysis is directional and comparative. It should not be interpreted as a thermodynamic entropy model of the glass transition.

## S9. Shuffle-control protocol and N=1000

Shuffle controls randomly permute the axis-target relationship while preserving the observed marginal distribution. The manuscript uses 1000 shuffles for the locked summary controls. This number gives a practical empirical-null estimate for preprint-level robustness checks while keeping the public pipeline lightweight. Very small empirical excesses, especially in the NeurIPS subset, are treated cautiously in the manuscript discussion.

## S10. Descriptor comparison protocol

Descriptor comparisons evaluate MSBP density against other simple structural descriptors such as ring density, aromatic ring density, heteroatom density, and size proxies. Because MSBP density is exactly the negative of rotatable-bond density, the comparison is not framed as a novelty claim over rotatable-bond density. Instead, comparator tables address whether a broader mobility-suppression framing captures variation beyond ring-only or aromatic-only rigidity proxies.

Paired bootstrap comparisons use the same target residuals and compare absolute Spearman association values across descriptors. When confidence intervals include zero, the manuscript treats the distinction as not statistically stable.

## S11. Contradiction taxonomy definition

The contradiction taxonomy groups cases by mechanistic context, such as aromatic/rigid-backbone enrichment, flexible-chain enrichment, heteroatom/polar context, and related categories. The table is a diagnostic map of where mobility suppression aligns or conflicts with Tg residual direction. It is not a complete chemical mechanism classification and is not used as a hard decision rule.

The Leeds PAEK subset is interpreted as a family-narrow stress test because its screened entries are dominated by aromatic/rigid-backbone chemistry. This strengthens that particular stress-test interpretation but does not replace broad chemical-diversity validation.

## S12. Data-rights and redistribution audit

The public release omits raw third-party datasets and row-level third-party-derived SMILES/Tg tables. Public CSVs are restricted to aggregate summaries, source-screening metadata, validation summaries, and non-row-level analysis outputs. A scanner in `scripts/check_public_safe_repo.py` flags CSV files that combine structural identifier columns with Tg-like columns.

Figure 4 uses synthetic illustrative motifs rather than redistributed source-row examples. These are explanatory structures for mechanism communication, not records copied from validation datasets.

## S13. Reproducibility limitations

Because raw third-party datasets are not redistributed, full end-to-end reproduction requires external source acquisition. The public repository is designed to reproduce feature extraction and validation once a user supplies locally obtained source tables with the expected columns. The locked aggregate summaries included in the repository are provided for auditability, not as a substitute for source-controlled raw data.

## S14. Recommended preprint-release order

The recommended public release order is:

1. finalize the public-safe repository;
2. create the public GitHub repository;
3. create a GitHub release;
4. use Zenodo GitHub integration to archive the release and obtain a DOI;
5. Update README, CITATION.cff, .zenodo.json, and manuscript Code Availability with the GitHub URL and Zenodo DOI;
6. re-render the final PDF;
7. upload the final PDF to ChemRxiv.
