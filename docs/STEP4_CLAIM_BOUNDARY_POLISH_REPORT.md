# Step 4 - Claim Boundary Polish Report

**Project:** MSBP-Tg Journal Submission
**Target journal:** Journal of Cheminformatics
**Step:** 4 of 12
**Status:** PASS

## Purpose

This step tightened the manuscript's claim boundary so that the paper reads as a conservative cheminformatics validation study rather than as an overbroad physical-law or universal-prediction claim.

## Edits completed

1. Added a dedicated **Section 2.2 Claim boundary**.
2. Replaced "deterministic heuristic" with "rule-based heuristic" to avoid overprecision.
3. Replaced "The main result" with "The main observation" and "reported evidence".
4. Reframed the MSBP statement as a **working statement tested here** rather than an established law.
5. Expanded the Limitations section to state that the analysis is not proof of a universal Tg law or causal mechanism.
6. Clarified that public reproduction emphasizes public-safe aggregate tables and source documentation when raw third-party records cannot be redistributed.
7. Updated `docs/claim_boundary.md` with allowed and disallowed wording.
8. Updated the journal submission checklist with the Step 4 claim-boundary audit.

## Current required framing

MSBP-Tg should be presented as:

> a public-safe cheminformatics validation study of an interpretable mobility-suppression coordinate for polymer Tg boundary displacement.

It should not be presented as:

- a universal Tg law;
- a causal proof of glass-transition mechanism;
- a replacement for experimental Tg measurement;
- a newly invented molecular descriptor;
- a guaranteed polymer-design engine.

## Flagged-term audit after editing

The remaining occurrences of sensitive terms are acceptable because they appear inside explicit negation or limitation language, or in reference titles.

```text
line 9: Polymer glass-transition temperature (Tg) remains difficult to interpret across structurally related repeat units because visible chemistry and molecular size do not fully determine residual property differences. This study evaluates the Mobility Suppression Boundary Principle (MSBP-Tg) as a public-safe cheminformatics validation study. Within comparable chemistry-size fibers, upward residual Tg displacement is tested for association with suppression of normalized local rotatable mobility. The MSBP density coordinate is exactly the sign reversal of rotatable-bond density, MSBP density = -NumRotatableBonds/heavy_atoms; therefore, the contribution is not the invention of a new molecular descriptor. Instead, the contribution is the use of a familiar mobility descriptor as an interpretable within-fiber suppression coordinate combined with residualization, source-family checks, descriptor comparisons, shuffle controls, bootstrap summaries, and contradiction taxonomy. Three post-lock source-family checks are consistent with this framing: a broad leak-excluded public Tg subset, a released NeurIPS Tg-known test subset, and a family-narrow Leeds PAEK stress test. Across these public-safe aggregate checks, the mobility-suppression coordinate gives directionally consistent support for upward Tg displacement while preserving explicit limitations around source bias, family narrowing, raw-data redistribution, and prospective experimental validation. The study is positioned as an interpretable polymer-informatics screening and validation workflow, not as a universal Tg law, a new descriptor claim, or a replacement for experimental glass-transition measurement.
line 17: This framing makes the present work a cheminformatics validation study rather than a universal theory of glass transition. The coordinate tested here, MSBP density, is the sign-reversed normalized rotatable-bond density. It is not introduced as a new molecular descriptor. Its value is in reorienting a familiar descriptor into a suppression-coordinate interpretation and then testing whether that coordinate remains associated with upward Tg boundary displacement under residualization, source-family checks, comparator descriptors, shuffle controls, and contradiction analysis.
line 31: Descriptor transparency statement. MSBP density is exactly the negative of rotatable-bond density: rot_density = NumRotatableBonds/heavy_atoms and MSBP_density = -rot_density. The paper does not claim discovery of a new descriptor. The manuscript's claim is narrower: a familiar mobility descriptor is reoriented as a suppression coordinate and evaluated through within-fiber residualization, post-lock source-family checks, entropy controls, and contradiction taxonomy.
line 42: The contribution is therefore methodological and interpretive. It does not claim a complete theory of Tg, a universal law of polymer glass transition, a causal proof of glass-transition mechanism, or a replacement for experimental measurement.
line 47: Throughout this manuscript, the term "principle" is used as the name of the tested MSBP-Tg working hypothesis and coordinate framing. It should not be read as a claim that a universal physical law of polymer glass transition has been established. The present evidence supports a narrower statement: within the public-safe source-family checks reported here, sign-reversed normalized rotatable-bond density is directionally associated with upward Tg displacement after chemistry-size residualization. The analysis does not establish causality, does not replace experimental Tg measurement, and does not remove the need for prospective validation on new polymer candidates.
line 83: Known descriptor comparisons include rotatable-bond density, ring density, aromatic-ring density, heteroatom density, and heavy-atom count. Since MSBP density is exactly the sign reversal of rot/heavy, equal absolute correlations are expected. For other descriptor comparisons, paired bootstrap confidence intervals estimate the difference in absolute correlation. Spearman confidence intervals were estimated with bootstrap resampling. Effect-size slopes were calculated as source-local OLS slopes of Tg residual on MSBP-density residual. These slopes are magnitude anchors, not universal constants.
line 125: Potential application areas include high-temperature structural polymers, aerospace-adjacent lightweight components, electronics packaging, and plastic components used around EV battery systems, where Tg is one of several design constraints. In such settings, an interpretable mobility-suppression coordinate could reduce wasted effort by flagging candidates whose local mobility profile is inconsistent with the desired Tg direction. However, MSBP-Tg does not replace full materials qualification. Candidate materials still require validation for mechanical strength, thermal aging, flame behavior, processability, dielectric or chemical compatibility, and application-specific safety requirements. Therefore, the practical value of MSBP-Tg is not a guaranteed cost or time saving, but a more transparent way to narrow and explain the candidate search space before higher-cost validation steps.
line 129: The analysis depends on repeat-unit SMILES quality, descriptor parsing, fiber definitions, and public-source coverage. MSBP density is a simple sign-reversed descriptor and cannot represent all polymer physics, including tacticity, molecular-weight distribution, crystallinity, processing history, measurement protocol, chain architecture, or intermolecular cohesive energy. The reported checks are therefore best interpreted as source-family validation of an interpretable boundary coordinate rather than proof of a universal Tg law or a causal mechanism. Because raw third-party records are not redistributed, public reproduction emphasizes public-safe aggregate tables, source documentation, code checks, and derived figures rather than unrestricted row-level replay of every source. Contradiction cases should be treated as scientifically informative rather than discarded, and prospective experimental validation remains necessary for newly proposed polymer candidates.
```

## Verdict

**Step 4 PASS.** The manuscript now has an explicit reviewer-facing claim boundary and safer wording across the abstract, contribution, methods, discussion, limitations, conclusion, and author contribution statements.

## Next step

Step 5 - Related Work + references strengthening.
