from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def broken(*parts: str) -> str:
    return "".join(parts)


FORBIDDEN_PATTERNS = [
    broken("known_descriptor_comparison", "__", "clean.csv"),
    broken("paired_descriptor_bootstrap", "_", ".csv"),
    broken("contradiction_taxonomy_by_source", "_", ".csv"),
    broken("residual_centering_sensitivity", "_", ".csv"),
    broken("Public-safe ", "public-safe", " preprint package"),
    broken("Release-", "compliance", " metadata candidate"),
    broken("Data license and redistribution audit", " ()"),
]

REQUIRED_REFERENCES = [
    "tables/known_descriptor_comparison_clean.csv",
    "tables/paired_descriptor_bootstrap.csv",
    "tables/contradiction_taxonomy_by_source.csv",
    "tables/residual_centering_sensitivity.csv",
]


def read_docx_text(path: Path) -> str:
    with ZipFile(path) as zf:
        parts = []
        for name in zf.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                parts.append(zf.read(name).decode("utf-8", errors="ignore"))
        return "\n".join(parts)


def test_public_text_and_docx_have_no_broken_filename_references():
    text_paths = [
        ROOT / "README.md",
        ROOT / ".zenodo.json",
        ROOT / "data" / "license_audit.md",
        ROOT / "manuscript" / "MSBP_Tg_Journal_Manuscript.md",
        ROOT / "supplementary" / "Supplementary_Methods.md",
    ]
    corpus = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in text_paths if path.exists())
    corpus += read_docx_text(ROOT / "manuscript" / "MSBP_Tg_Journal_Manuscript.docx")
    corpus += read_docx_text(ROOT / "supplementary" / "Supplementary_Methods.docx")
    offenders = [pattern for pattern in FORBIDDEN_PATTERNS if pattern in corpus]
    assert offenders == []


def test_documented_csv_references_exist():
    for ref in REQUIRED_REFERENCES:
        assert (ROOT / ref).exists(), ref
