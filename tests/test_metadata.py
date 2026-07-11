from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHEMRXIV_DOI_URL = "https://doi.org/10.26434/chemrxiv.15005629/v1"
ZENODO_DOI = "10.5281/zenodo.21100020"
ZENODO_DOI_URL = f"https://doi.org/{ZENODO_DOI}"
REPO_URL = "https://github.com/htetkokokonaing-dev/msbp-tg"

def test_zenodo_metadata_filename_and_core_fields() -> None:
    zenodo = ROOT / ".zenodo.json"
    assert zenodo.exists(), ".zenodo.json must be present for Zenodo GitHub integration metadata"
    assert not (ROOT / "zenodo.json").exists(), "legacy zenodo.json filename should be absent"
    data = json.loads(zenodo.read_text())
    assert data["license"] == "mit"
    assert data["language"] == "eng"
    assert data["upload_type"] == "software"
    assert 'version' not in data
    related = data.get("related_identifiers", [])
    identifiers = {item.get("identifier") for item in related}
    assert CHEMRXIV_DOI_URL in identifiers
    assert REPO_URL in identifiers

def test_citation_cff_post_doi_identifiers() -> None:
    cff = (ROOT / "CITATION.cff").read_text()
    assert "type: software" in cff
    assert "REPOSITORY_URL_TO_BE_INSERTED" not in cff
    assert "DOI_TO_BE_INSERTED" not in cff
    assert f'doi: "{ZENODO_DOI}"' in cff
    assert f'url: "{ZENODO_DOI_URL}"' in cff
    assert f'repository-code: "{REPO_URL}"' in cff
    assert "preferred-citation:" in cff
    assert "10.26434/chemrxiv.15005629/v1" in cff

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
