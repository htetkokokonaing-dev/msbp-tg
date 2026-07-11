from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCX_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    parts: list[str] = []
    for text_el in root.findall(".//w:t", DOCX_NS):
        parts.append(text_el.text or "")
    return " ".join(parts)


def public_text_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "RELEASE_NOTES.md"]
    files += sorted((ROOT / "docs").glob("*.md"))
    files += sorted((ROOT / "manuscript").glob("*.md"))
    files += sorted((ROOT / "supplementary").glob("*.md"))
    return files


def test_no_internal_release_compliance_candidate_wording_in_public_text() -> None:
    offenders: list[str] = []
    for path in public_text_files():
        text = path.read_text(encoding="utf-8")
        if re.search(r"release-compliance", text, re.IGNORECASE):
            offenders.append(path.relative_to(ROOT).as_posix())
    assert offenders == []


def test_manuscript_uses_conservative_support_wording_and_preprint_title_line() -> None:
    md = (ROOT / "manuscript" / "MSBP_Tg_Journal_Manuscript.md").read_text(encoding="utf-8")
    dx = docx_text(ROOT / "manuscript" / "MSBP_Tg_Journal_Manuscript.docx")
    for text in (md, dx):
        assert "Three post-lock source-family checks are consistent with this framing" in text
        assert "Three post-lock source-family checks support this framing" not in text
        assert "Because MSBP density is non-positive for ordinary repeat units" in text
    assert re.search(r"Journal\s+submission\s+version\s+after\s+ChemRxiv\s+preprint\s+posting", dx)
    assert "Release-compliance candidate manuscript" not in dx


def test_supplement_release_order_is_not_bullet_number_duplicated() -> None:
    md = (ROOT / "supplementary" / "Supplementary_Methods.md").read_text(encoding="utf-8")
    dx = docx_text(ROOT / "supplementary" / "Supplementary_Methods.docx")
    assert "CITATION.cff, .zenodo.json" in md
    assert "CITATION.cff, .zenodo.json" in dx
    assert "CITATION.cff,.zenodo.json" not in md
    assert "CITATION.cff,.zenodo.json" not in dx
    assert "• 1." not in dx
    assert "• 2." not in dx
