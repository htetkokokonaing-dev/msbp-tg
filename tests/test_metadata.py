from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_zenodo_metadata_filename_and_core_fields() -> None:
    zenodo = ROOT / ".zenodo.json"
    assert zenodo.exists(), ".zenodo.json must be present for Zenodo GitHub integration metadata"
    assert not (ROOT / "zenodo.json").exists(), "legacy zenodo.json filename should be absent"
    data = json.loads(zenodo.read_text())
    assert data["license"] == "mit"
    assert data["language"] == "eng"
    assert data["upload_type"] == "software"
    assert 'version' not in data
    assert data.get("related_identifiers", []) == []

def test_citation_cff_software_type_and_no_fake_identifier() -> None:
    cff = (ROOT / "CITATION.cff").read_text()
    assert "type: software" in cff
    assert "REPOSITORY_URL_TO_BE_INSERTED" not in cff
    assert "DOI_TO_BE_INSERTED" not in cff
    assert "doi:" not in cff.lower()
    assert "repository-code:" not in cff

def test_metadata_docs_use_dot_zenodo_filename() -> None:
    docs = [
        ROOT / "docs" / "zenodo_metadata_copy_paste.md",
        ROOT / "docs" / "doi_and_release_workflow.md",
        ROOT / "docs" / "github_zenodo_deployment_guide.md",
        ROOT / "docs" / "post_doi_manuscript_update_checklist.md",
    ]
    for path in docs:
        text = path.read_text()
        assert ".zenodo.json" in text
        assert "zenodo.json" not in text.replace(".zenodo.json", "")
