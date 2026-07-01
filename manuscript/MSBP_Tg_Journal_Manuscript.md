# Abstract

Polymer glass-transition temperature (Tg) varies widely even among repeat units with similar visible chemistry and size. This manuscript formulates and tests the Mobility Suppression Boundary Principle (MSBP-Tg): within comparable chemistry-size fibers, upward Tg boundary displacement is associated with suppression of normalized local rotatable mobility. The density coordinate used here is exactly the sign reversal of rotatable-bond density, MSBP density = -NumRotatableBonds/heavy_atoms. Thus the contribution is not the invention of a new molecular descriptor. It is the physical and statistical use of normalized mobility suppression as a within-fiber boundary coordinate. Three post-lock source-family checks are consistent with this framing: a broad leak-excluded public Tg subset, a released NeurIPS Tg-known test subset, and a family-narrow Leeds PAEK stress test. Bootstrap confidence intervals, paired descriptor comparisons, shuffle controls, and contradiction taxonomy are reported to separate support from overclaiming.

# 1. Introduction

The glass-transition temperature (Tg) is a central property for polymer design because it marks the temperature range where amorphous segmental mobility becomes dynamically accessible. Classical explanations emphasize molecular weight, free volume, cooperative relaxation, configurational entropy, and empirical structure-property correlations [1-8]. Modern polymer-informatics models can predict Tg using fingerprints, descriptors, and learned representations [9-12], but high predictive accuracy alone does not always isolate a physically interpretable boundary coordinate.

The narrower problem addressed here is within-family Tg displacement: after visible polymer family and approximate repeat-unit size are accounted for, why do some repeat units sit on a higher Tg boundary while others sit lower? MSBP-Tg answers this question with a simple normalized coordinate: local rotatable mobility suppression. The analysis tests whether this coordinate organizes residual Tg displacement inside comparable chemistry-size fibers rather than across all polymers at once.

# 2. Principle, physical mechanism, and contribution

The MSBP statement is: within comparable polymer chemistry-size fibers, reduced normalized rotatable mobility shifts the observed Tg boundary upward, while increased local mobility shifts it downward. A visible fiber is a reproducible grouping by polymer-family or raw chemistry label plus a molecular-size bin.

Tg marks the onset temperature for cooperative segmental chain motion. Repeat units with fewer rotatable bonds per heavy atom have lower local conformational freedom, so local rearrangements require higher thermal energy. The MSBP density coordinate therefore represents normalized resistance to local conformational motion, rather than a new molecular descriptor.

Different polymer families carry systematically different baseline Tg levels due to cohesion, polarity, packing, intermolecular interactions, and backbone chemistry. Testing MSBP within comparable chemistry-size fibers removes these baselines and asks whether normalized local mobility suppression explains the remaining within-family Tg boundary displacement.

Raw rotatable-bond count is size-confounded: larger repeat units tend to contain more rotatable bonds simply because they contain more atoms. Dividing by heavy-atom count normalizes this size effect, so the axis measures local rotational-freedom concentration rather than repeat-unit size.

Transparency correction. MSBP density is exactly the negative of rotatable-bond density: rot_density = NumRotatableBonds/heavy_atoms and MSBP_density = -rot_density. The paper does not claim discovery of a new descriptor. The novelty claim is narrower: a familiar mobility descriptor is reoriented as a suppression coordinate and evaluated through within-fiber residualization, post-lock source-family checks, entropy controls, and contradiction taxonomy.

![Figure 1. Theory schematic. MSBP density is the suppression-oriented form of rotatable-bond density and is interpreted as normalized local mobility suppression.](../figures/figure1_theory_schematic.png)

# 3. Relationship to existing work

MSBP-Tg is complementary to classical Tg theories and empirical property-prediction models. Fox-Flory molecular-weight effects, WLF relaxation behavior, Gibbs-DiMarzio and Adam-Gibbs configurational arguments, Cohen-Turnbull free-volume reasoning, and broader glass-transition discussions address different aspects of glass formation and relaxation [1-8]. Bicerano-style group/property estimation and Van Krevelen-style polymer-property methods provide essential context for structure-property modeling [9,10].

Polymer Genome and related polymer-informatics studies show that modern descriptors and machine-learning representations can predict polymer properties including Tg [11,12]. The Leeds PAEK work by Brierley-Croft et al. provides a recent example of polymer-informatics Tg modeling for a chemically focused PAEK family and supplies the family-narrow dataset used here as a stress test [13,14]. The NeurIPS/Open Polymer benchmark provides a separate released polymer-property source containing SMILES and Tg values derived from molecular-dynamics-based computational workflows [15,16]. The broad public Tg source used for the leak-excluded subset is cited as a source repository rather than redistributed here [19].

# 4. Data sources and source roles

Three post-lock source-family checks were used. The tsaicying polymer Tg subset is the broadest leak-excluded public Tg source and is used only through derived, non-redistributed validation summaries [19]. The NeurIPS released Tg-known subset provides a benchmark-style check from the Open Polymer Prediction source family; it is directionally supportive but weaker in entropy separation [15,16]. The Leeds PAEK subset comes from the Brierley-Croft et al. Macromolecules work and associated University of Leeds Research Data archive [13,14]. It is an independent family-narrow stress test, not a broad chemical-diversity validation. After screening, the Leeds subset contains only aromatic/rigid-backbone PAEK entries, which is informative but should not be generalized as broad coverage.

# 5. Methods

## 5.1 SMILES and descriptor handling

Repeat-unit SMILES were parsed with RDKit using SMILES string representations [17,18]. Rows that could not be parsed were screened out. Polymer dummy atoms (*) were retained when RDKit parsing allowed the representation and were not treated as chemical heavy atoms for the normalized mobility denominator. Descriptor extraction used RDKit NumRotatableBonds, heavy-atom count, ring count, aromatic-ring count, heteroatom count, and explicit silicon atom count. The silicon atom count was added as a direct atomic-number-14 feature to avoid misassignment of silicon-like fibers. The public environment specifies rdkit>=2023.9.1; the Step 7 QA environment reported RDKit 2025.09.4. Future reruns should record rdkit.__version__ with the generated feature table.

## 5.2 MSBP density definition

The locked density coordinate is MSBP_density = -NumRotatableBonds/heavy_atoms. The count coordinate is MSBP_count = -NumRotatableBonds. The sign convention makes higher values mean greater mobility suppression. Because MSBP density is non-positive for ordinary repeat units, higher suppression corresponds to values closer to zero. Because this coordinate is exactly the sign-reversed rotatable-bond density, MSBP density and rot/heavy have equal absolute rank correlations by definition.

## 5.3 Fiber definition and residualization

A visible fiber combines a raw chemistry/family label with a molecular-size bin. Where a dataset supplied polymer class labels, those labels were used. Otherwise a deterministic heuristic assigned simple chemistry families using silicon atoms, aromatic rings, heteroatom status, and hydrocarbon-like fallback categories. These fibers are analysis strata, not claims of complete polymer taxonomy. The main public-code protocol computes residuals by subtracting the within-fiber mean from Tg and from the mobility-suppression coordinate. The reported rank correlations are Spearman correlations between these mean-centered residualized coordinate values and mean-centered residualized Tg values. Median-centering is retained only as a sensitivity check; it preserves the same positive direction across all three source-family checks (Table S1).

Table S1. Residual-centering sensitivity. Main results use within-fiber mean-centering to match `src/msbp_tg/metrics.py::residualize_by_group`; median-centering is reported only as a robustness check.

| Source | Center | n | fibers | rho | sign accuracy | entropy gain |
|---|---:|---:|---:|---:|---:|---:|
| Stage 10 | mean | 739 | 64 | 0.745 | 0.903 | 0.157 |
| Stage 10 | median | 739 | 64 | 0.744 | 0.910 | 0.157 |
| Stage 11 | mean | 261 | 36 | 0.551 | 0.780 | 0.060 |
| Stage 11 | median | 261 | 36 | 0.531 | 0.742 | 0.060 |
| Stage 13 | mean | 78 | 7 | 0.828 | 0.950 | 0.271 |
| Stage 13 | median | 78 | 7 | 0.832 | 0.949 | 0.271 |

## 5.4 Entropy and shuffle controls

Boundary uncertainty was summarized as binary entropy in nats. Axis quantile bins were compared with a high-Tg boundary label. The null control shuffled the axis 1000 times. Empirical p-values were computed as (1 + number of shuffled statistics at least as large as observed) / (1 + number of shuffles).

## 5.5 Descriptor comparison and bootstrap uncertainty

Known descriptor comparisons include rotatable-bond density, ring density, aromatic-ring density, heteroatom density, and heavy-atom count. Since MSBP density is exactly the sign reversal of rot/heavy, equal absolute correlations are expected. For other descriptor comparisons, paired bootstrap confidence intervals estimate the difference in absolute correlation. Spearman confidence intervals were estimated with bootstrap resampling. Effect-size slopes were calculated as source-local OLS slopes of Tg residual on MSBP-density residual. These slopes are magnitude anchors, not universal constants.

# 6. Results

## 6.1 Locked residual association

![Figure 2. Residual scatter plots. Leeds is strong but family-narrow; NeurIPS is positive but weaker.](../figures/figure2_three_source_residual_scatter.png)

## 6.2 Shuffle controls

![Figure 3. Shuffle-control distributions with observed entropy gain and shuffle p95.](../figures/figure3_shuffle_control_entropy.png)

## 6.3 Known descriptor comparison

Table 4 reports comparator descriptors. MSBP density is not listed as an independent comparator because it is exactly -rot/heavy. The rot/heavy row is included to make this identity explicit; the meaningful alternatives are ring density, aromatic-ring density, heteroatom density, and size proxies.

## 6.4 Paired descriptor bootstrap

In the broad tsaicying source and the family-narrow Leeds source, MSBP density is distinguishable from ring-density alternatives by paired bootstrap. In the smaller NeurIPS source, the paired bootstrap intervals include zero for ring-density comparisons; this source therefore supports the mobility direction but not a strong superiority claim over ring density.

## 6.5 Effect-size slopes

## 6.6 Contradiction taxonomy

Contradiction rates differ by source and mechanism family. Polar/heteroatom contexts are heterogeneous, supporting their treatment as modifiers. The Leeds PAEK subset contains only aromatic/rigid-backbone entries after screening; this confirms its family-narrow character rather than broad chemical diversity.

## 6.7 Illustrative mobility motifs

![Figure 4. Synthetic illustrative repeat-unit motifs drawn with RDKit. The motifs show qualitative routes to higher or lower normalized mobility suppression and are not redistributed row-level records from third-party datasets. Because MSBP density is non-positive for ordinary repeat units, higher suppression corresponds to values closer to zero.](../figures/figure4_representative_repeat_unit_structures.png)

# 7. Discussion

The main result is not that rotatable bonds matter; that is chemically unsurprising and consistent with existing polymer-property intuition. The result is that the sign-reversed, normalized rotatable mobility coordinate repeatedly organizes Tg displacement after visible chemistry-size structure is removed. This makes MSBP-Tg a boundary-coordinate framing rather than a descriptor-invention claim.

Ring density is a strong comparator because aromatic rings often suppress local mobility. However, ring density captures only one route to mobility suppression: aromatic or cyclic rigidity. MSBP density also responds to flexible aliphatic or side-chain mobility, where high rotatable density shifts the boundary downward. This explains why MSBP can be statistically distinguishable from ring density in broad sources while being statistically comparable in smaller or ring-biased sources such as the NeurIPS subset.

Leeds PAEK is strong but family-narrow. Its high correlation should be read as a chemically focused stress test, not as evidence that the same magnitude applies across all polymers. NeurIPS is weaker in entropy separation and should be described as directional support. The broadest support here comes from the leak-excluded public Tg subset. Using the mean-centered main residuals, effect-size slopes provide approximate source-local magnitude grounding: roughly 407-411 C per unit MSBP-density residual in the broad and NeurIPS sources, and a larger PAEK slope in the narrow Leeds family.

## 7.1 Implications for polymer design workflows

In practical polymer design, MSBP-Tg is best viewed as an early-stage screening and interpretation coordinate rather than as a stand-alone Tg predictor or qualification tool. By identifying repeat units whose normalized local mobility is unusually suppressed or unusually flexible within comparable chemistry-size fibers, the method can help prioritize candidates before more expensive molecular simulation, synthesis, or experimental Tg measurement. This is most useful when designers must search across many chemically related repeat units and need an interpretable rule for why some candidates are expected to shift toward a higher or lower Tg boundary.

Potential application areas include high-temperature structural polymers, aerospace-adjacent lightweight components, electronics packaging, and plastic components used around EV battery systems, where Tg is one of several design constraints. In such settings, an interpretable mobility-suppression coordinate could reduce wasted effort by flagging candidates whose local mobility profile is inconsistent with the desired Tg direction. However, MSBP-Tg does not replace full materials qualification. Candidate materials still require validation for mechanical strength, thermal aging, flame behavior, processability, dielectric or chemical compatibility, and application-specific safety requirements. Therefore, the practical value of MSBP-Tg is not a guaranteed cost or time saving, but a more transparent way to narrow and explain the candidate search space before higher-cost validation steps.

# 8. Limitations

The analysis depends on repeat-unit SMILES quality, descriptor parsing, fiber definitions, and public-source coverage. MSBP density is a simple sign-reversed descriptor and cannot represent all polymer physics, including tacticity, molecular-weight distribution, crystallinity, processing history, measurement protocol, chain architecture, or intermolecular cohesive energy. Contradiction cases should be treated as scientifically informative rather than discarded.

# 9. Conclusion

MSBP-Tg identifies a boundary-level regularity: within comparable chemistry-size fibers, normalized suppression of local rotatable mobility is associated with upward Tg boundary displacement. The contribution lies in boundary-coordinate framing, within-fiber residualization, and leak-screened multi-source validation rather than descriptor invention. The principle is most useful as a physically interpretable boundary coordinate for explaining residual Tg displacement inside comparable polymer families. For design workflows, the principle is most appropriately used as an interpretable early-screening coordinate that helps prioritize chemically related candidates for higher-cost simulation, synthesis, or measurement. Its practical role is therefore to narrow and explain the search space, not to replace experimental qualification or full multiproperty polymer-design models.

# Data Availability

Raw third-party datasets are not redistributed in this public-safe package. Row-level third-party-derived SMILES/Tg tables are also excluded from the public repository unless redistribution permission is explicit. Source links, acquisition notes, and license-status notes are provided in data/external_sources.md, data/README_data_public_safe.md, and data/license_audit.md. The repository includes only aggregate validation summaries, source-role notes, figures, and reproducibility scripts intended for public release.

# Code Availability

Analysis code and the public-safe reproducibility package are archived on GitHub and Zenodo.

GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

Zenodo DOI: https://doi.org/10.5281/zenodo.21100020

The repository includes src/msbp_tg, scripts, tests, environment files, metadata files, aggregate validation summaries, figures, and public-safe derived tables. Raw third-party datasets and row-level third-party-derived SMILES/Tg records are not redistributed.

# Funding

The author received no external funding for this work.

# Conflict of Interest

The author declares no competing interests.

# Author Contributions

Htet Ko Ko Naing conceived the principle, curated the analysis workflow, interpreted the results, and prepared the manuscript and repository package with AI-assisted drafting and code-generation support. All scientific claims, analyses, and final manuscript decisions were reviewed and approved by the author.

# AI-assisted workflow disclosure

AI-assisted drafting and code-organization tools were used for language refinement and implementation support. The author retained responsibility for scientific interpretation, validation decisions, and final manuscript content. This statement should be adapted to the selected journal policy before submission.

# References

1. Fox, T. G. and Flory, P. J. (1950). Second-order transition temperatures and related properties of polystyrene. Journal of Applied Physics. DOI: 10.1063/1.1699711.

2. Williams, M. L., Landel, R. F. and Ferry, J. D. (1955). The temperature dependence of relaxation mechanisms in amorphous polymers and other glass-forming liquids. Journal of the American Chemical Society. DOI: 10.1021/ja01619a008.

3. Gibbs, J. H. and DiMarzio, E. A. (1958). Nature of the glass transition and the glassy state. Journal of Chemical Physics. DOI: 10.1063/1.1744141.

4. Cohen, M. H. and Turnbull, D. (1959). Molecular transport in liquids and glasses. Journal of Chemical Physics. DOI: 10.1063/1.1730566.

5. Adam, G. and Gibbs, J. H. (1965). On the temperature dependence of cooperative relaxation properties in glass-forming liquids. Journal of Chemical Physics. DOI: 10.1063/1.1696442.

6. Angell, C. A. (1995). Formation of glasses from liquids and biopolymers. Science. DOI: 10.1126/science.267.5206.1924.

7. Ediger, M. D., Angell, C. A. and Nagel, S. R. (1996). Supercooled liquids and glasses. Journal of Physical Chemistry. DOI: 10.1021/jp953538d.

8. Debenedetti, P. G. and Stillinger, F. H. (2001). Supercooled liquids and the glass transition. Nature. DOI: 10.1038/35065704.

9. Bicerano, J. (2002). Prediction of Polymer Properties, 3rd ed. Marcel Dekker.

10. Van Krevelen, D. W. and Te Nijenhuis, K. (2009). Properties of Polymers, 4th ed. Elsevier.

11. Kim, C. et al. (2018). Polymer Genome: A data-powered polymer informatics platform for property predictions. Journal of Physical Chemistry C. DOI: 10.1021/acs.jpcc.8b02913.

12. Chen, G., Tao, L. and Li, Y. (2021). Predicting polymers' glass transition temperature by a chemical language processing model. Polymers. DOI: 10.3390/polym13111898.

13. Brierley-Croft, S., Olmsted, P. D., Hine, P. J., Mandle, R. J., Chaplin, A., Grasmeder, J. and Mattsson, J. (2025). Polymer informatics method for fast and accurate prediction of the glass transition temperature from chemical structure. Macromolecules. DOI: 10.1021/acs.macromol.5c00178.

14. Brierley-Croft, S., Olmsted, P. D., Hine, P. J., Mandle, R. J., Chaplin, A., Grasmeder, J. and Mattsson, J. (2024). Polymer Informatics Method for Fast and Accurate Prediction of the Glass Transition Temperature from Chemical Structure - dataset. University of Leeds Research Data. DOI: 10.5518/1596.

15. Kaggle (2025). NeurIPS - Open Polymer Prediction 2025: competition data. https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/data. Accessed 2026-06-30.

16. Liu, G. et al. (2025). Open Polymer Challenge: Post-Competition Report. arXiv:2512.08896.

17. Weininger, D. (1988). SMILES, a chemical language and information system. 1. Introduction to methodology and encoding rules. Journal of Chemical Information and Computer Sciences. DOI: 10.1021/ci00057a005.

18. RDKit contributors. RDKit: Open-source cheminformatics software. https://www.rdkit.org/. QA environment version recorded for this package: 2025.09.4.

19. tsaicying (2026). polymer-tg-predictor: glass-transition-temperature dataset and model repository. GitHub repository. Accessed 2026-06-30.
