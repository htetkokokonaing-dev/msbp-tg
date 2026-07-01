# Public release checklist

Before GitHub/Zenodo/ChemRxiv posting:

- [ ] Run the test suite.
- [ ] Run `scripts/check_public_release_safety.py`.
- [ ] Run `scripts/check_public_safe_repo.py`.
- [ ] Confirm no raw third-party datasets are included.
- [ ] Confirm no row-level third-party-derived SMILES/Tg CSV tables are included.
- [ ] Confirm `data/license_audit.md` is present.
- [ ] Confirm `.zenodo.json` is present and `zenodo.json` is absent.
- [ ] Confirm `CITATION.cff` has software metadata.
- [ ] Regenerate `data/manifest.csv` after any file changes.
- [ ] Re-render the manuscript after DOI/URL insertion.
- [ ] Create GitHub release tag `preprint-candidate`.
- [ ] Enable Zenodo archival and copy the DOI.
- [ ] Insert GitHub URL and Zenodo DOI into README, citation metadata, and manuscript.
- [ ] Create final DOI-bearing release `final DOI-bearing release`.
- [ ] Use the DOI-updated PDF for ChemRxiv or journal submission.

This public package does not redistribute raw third-party datasets or row-level third-party-derived SMILES/Tg tables. Validation evidence is provided as aggregate statistics and source-role summaries. Full reproduction requires independently obtaining external datasets under their own licenses and terms.
