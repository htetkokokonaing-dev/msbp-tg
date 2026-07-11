# Journal submission checklist after ChemRxiv posting

Target journal: Journal of Cheminformatics, or another cheminformatics/polymer-informatics journal.

## Identifiers

- ChemRxiv preprint DOI: https://doi.org/10.26434/chemrxiv.15005629/v1
- Zenodo software/archive DOI: https://doi.org/10.5281/zenodo.21100020
- GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

## Files to upload to a journal system

1. `MSBP_Tg_Journal_Submission_Manuscript.docx`
2. `MSBP_Tg_Journal_Submission_Manuscript.pdf`
3. `cover_letter_journal_of_cheminformatics.docx`
4. `supplementary/Supplementary_Methods.pdf`
5. Optional: figure files from `figures/` if the journal asks for separate figures.

## Final checks before submission

- Title matches ChemRxiv and GitHub/Zenodo records.
- Abstract spacing is clean.
- Code Availability includes GitHub and Zenodo DOI.
- Preprint Availability includes the ChemRxiv DOI.
- Data Availability clearly states that raw third-party datasets and row-level third-party-derived SMILES/Tg records are not redistributed.
- Conflict of interest statement says that the author declares no competing interests.
- Funding statement says that no external funding was received.
- AI-assisted workflow disclosure is adapted to the selected journal policy.
- The claim is framed as interpretable screening evidence, not as a universal Tg law or replacement for experiments.

## Step 4 claim-boundary audit

- Claim-boundary audit completed.
- Added explicit claim-boundary subsection.
- Replaced high-risk phrasing around universal law, proof, deterministic assignment, and design guarantees.
- Confirmed manuscript frames MSBP-Tg as an interpretable cheminformatics validation workflow, not as a universal Tg law, new descriptor, or replacement for experiment.


## Step 5 - Related Work and References Gate

- [x] Relationship-to-existing-work section strengthened for Journal of Cheminformatics scope.
- [x] Polymer informatics and Tg-prediction literature added.
- [x] SMILES/RDKit cheminformatics representation references retained.
- [x] Bootstrap, reproducibility, and FAIR-data references added.
- [x] references.bib created under manuscript/.


## Step 6 data provenance gate

- [x] Machine-readable source register added: `data/external_sources.csv`.
- [x] Human-readable source register strengthened: `data/external_sources.md`.
- [x] Raw-data exclusion documented: `data/raw/README.md`.
- [x] Local feature-table paths documented: `data/processed/README.md`.
- [x] License and redistribution audit strengthened: `data/license_audit.md`.
- [x] Manuscript Data Availability and Code Availability sections updated.
- [x] Public-safe distinction preserved: aggregate evidence is public; raw third-party records are not redistributed.


## Step 7 code reproducibility gate

- [x] Editable package install checked.
- [x] Public test suite passed: 42 tests.
- [x] Public release safety check passed.
- [x] Public-safe repository/data-rights check passed.
- [x] `reproduce.sh` added as a one-command public-safe audit wrapper.
- [x] Three-source summary script verified to perform a controlled public-safe skip when non-redistributable local feature tables are absent.
- [x] `docs/JOURNAL_REPRODUCIBILITY_AUDIT.md` created.
- [x] `docs/STEP7_CODE_REPRODUCIBILITY_AUDIT_REPORT.md` created.


## Step 8 figure/table alignment

- Step 8 figure/table alignment: PASS
- Manuscript image links resolve to public-safe figure files.
- Supplementary table file references are explicit.
- See `docs/figure_table_alignment.md` and `docs/STEP8_FIGURE_TABLE_ALIGNMENT_REPORT.md`.

## Step 9 GitHub metadata update

- [x] README updated with ChemRxiv DOI, Zenodo DOI, GitHub URL, public-safe data policy, and journal-submission framing.
- [x] CITATION.cff updated for software/archive citation with preferred ChemRxiv preprint citation.
- [x] .zenodo.json updated for journal-submission-ready software/archive metadata.
- [x] RELEASE_NOTES.md updated for recommended tag `v1.1.0-journal-submission`.
- [x] CHANGELOG.md updated for journal-submission-ready state.
- [x] GitHub release body copy-paste text updated in `docs/release_body_copy_paste.md`.
- [x] Metadata report created in `docs/STEP9_GITHUB_METADATA_UPDATE_REPORT.md`.

## Step 10 — GitHub release and Zenodo version update preparation

- [x] Recommended tag selected: `v1.1.0-journal-submission`.
- [x] GitHub release body prepared.
- [x] Termux release commands prepared.
- [x] Zenodo after-release checklist prepared.
- [x] Public tests passed before Step 10 packaging.
- [ ] User-created GitHub release confirmed.
- [ ] Zenodo new version confirmed.
- [ ] New Zenodo version DOI copied if assigned.

