# MSBP-Tg Journal Submission Package Report

Status: prepared after ChemRxiv public posting.

## Persistent identifiers

- ChemRxiv preprint DOI: https://doi.org/10.26434/chemrxiv.15005629/v1
- Zenodo software/archive DOI: https://doi.org/10.5281/zenodo.21100020
- GitHub repository: https://github.com/htetkokokonaing-dev/msbp-tg

## Main updates performed

1. Added ChemRxiv preprint availability to the journal manuscript.
2. Replaced the old placeholder code-availability text with resolved GitHub and Zenodo identifiers.
3. Added a conservative final sentence to the abstract to clarify that the analysis is not a universal Tg law or replacement for experimental measurement.
4. Strengthened the limitations section with explicit non-universal and prospective-validation language.
5. Kept the practical polymer-design implications section, framed conservatively as early-stage screening rather than guaranteed cost/time saving.
6. Updated README, CITATION.cff, .zenodo.json, RELEASE_NOTES.md, and metadata tests for the post-ChemRxiv/post-Zenodo state.
7. Created a journal cover letter draft for Journal of Cheminformatics-style submission.
8. Created a journal submission checklist.

## Verification

- `python -m pytest -q`: 39 passed.
- `python scripts/check_public_release_safety.py`: PASS.
- `python scripts/check_public_safe_repo.py`: PASS.
- Manuscript DOCX rendered to PNG and visually checked: 8 pages, no broken wide table, figures readable.
- Cover letter DOCX rendered to PNG and visually checked: 1 page, readable.

## Recommended journal submission files

- `manuscript/MSBP_Tg_Journal_Submission_Manuscript.docx`
- `manuscript/MSBP_Tg_Journal_Submission_Manuscript.pdf`
- `docs/cover_letter_journal_of_cheminformatics.docx`
- `supplementary/Supplementary_Methods.pdf`
- Optional separate figures from `figures/` if requested by the journal system.
