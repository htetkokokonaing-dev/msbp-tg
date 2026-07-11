# STEP 5 - Related Work + References Report

**Status:** PASS

## Completed edits

1. Strengthened Section 3, "Relationship to existing work".
2. Reframed the manuscript against four reviewer-relevant literatures:
   - classical Tg and glass-transition theory;
   - polymer-property estimation and polymer informatics;
   - cheminformatics representation and RDKit descriptor extraction;
   - reproducible computational research, bootstrap uncertainty, and FAIR-oriented data stewardship.
3. Clarified how MSBP-Tg differs from global Tg prediction models: it is a within-fiber interpretability and validation study, not a claim of higher global predictive accuracy.
4. Added references supporting polymer informatics, Tg prediction, SMILES/RDKit cheminformatics, bootstrap uncertainty, reproducible research, and FAIR data principles.
5. Created `manuscript/references.bib` for journal submission workflows that request BibTeX.
6. Created `docs/related_work_section.md` as a clean copy-paste section.

## Added references

- Ramprasad and Kim on improving polymer Tg machine-learning prediction.
- Babbar et al. on explainability and transferability of Tg models.
- Efron and Tibshirani on bootstrap uncertainty.
- Peng on reproducible computational research.
- Sandve et al. on reproducible computational research rules.
- Wilkinson et al. on FAIR data principles.
- Pedregosa et al. on scikit-learn.

## Reviewer-facing rationale

The revised related-work section now makes clear that the paper is not competing as a universal Tg model. Instead, it contributes a public-safe cheminformatics validation workflow for a simple interpretable mobility-suppression coordinate.

## Step 5 verdict

PASS. The manuscript now has a stronger literature-positioning layer for Journal of Cheminformatics.
