from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEMRXIV = "https://doi.org/10.26434/chemrxiv.15005629/v1"
ZENODO = "https://doi.org/10.5281/zenodo.21100020"
REPO = "https://github.com/htetkokokonaing-dev/msbp-tg"
TAG = "v1.1.0-journal-submission"


def test_root_metadata_mentions_public_identifiers() -> None:
    for rel in ["README.md", "RELEASE_NOTES.md", "CHANGELOG.md", "docs/release_body_copy_paste.md"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert CHEMRXIV in text
        assert ZENODO in text
        assert REPO in text


def test_citation_and_zenodo_metadata_are_journal_ready() -> None:
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert "10.5281/zenodo.21100020" in cff
    assert "10.26434/chemrxiv.15005629/v1" in cff
    assert "Public-Safe Cheminformatics Validation Study" in cff
    data = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    assert data["upload_type"] == "software"
    assert data["license"] == "mit"
    assert data["language"] == "eng"
    ids = {item["identifier"] for item in data["related_identifiers"]}
    assert CHEMRXIV in ids
    assert ZENODO in ids
    assert REPO in ids


def test_release_tag_recommended_in_release_docs() -> None:
    text = (
        (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
        + "\n"
        + (ROOT / "docs" / "release_body_copy_paste.md").read_text(encoding="utf-8")
    )
    assert TAG in text
