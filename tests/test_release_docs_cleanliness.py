from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_PATHS = [
    ROOT / 'README.md',
    *sorted((ROOT / 'docs').glob('*.md')),
    *sorted((ROOT / 'supplementary').glob('*.md')),
    *sorted((ROOT / 'manuscript').glob('*.md')),
]
BROKEN_PATTERNS = [
    re.compile(r'_[.]md\b'),
    re.compile(r'_[.]pdf\b'),
    re.compile(r'_[.]docx\b'),
    re.compile(r'_[.]csv\b'),
    re.compile(r'_[.]png\b'),
    re.compile(r'git add[.]\b'),
    re.compile(r'--out\.\./'),
    re.compile(r'\.py[.]\b'),
]


def test_public_docs_have_no_broken_release_label_artifacts():
    offenders: list[str] = []
    for path in SCAN_PATHS:
        text = path.read_text(encoding='utf-8')
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pattern in BROKEN_PATTERNS:
                if pattern.search(line):
                    offenders.append(f'{path.relative_to(ROOT)}:{line_no}: {line}')
    assert offenders == []


def test_documented_release_asset_paths_exist():
    required = [
        ROOT / 'RELEASE_NOTES.md',
        ROOT / 'manuscript' / 'MSBP_Tg_Journal_Manuscript.pdf',
        ROOT / 'manuscript' / 'MSBP_Tg_Journal_Manuscript.docx',
        ROOT / 'tables' / 'residual_centering_sensitivity.csv',
        ROOT / 'supplementary' / 'Supplementary_Methods.pdf',
        ROOT / 'supplementary' / 'Supplementary_Methods.docx',
    ]
    assert [p.relative_to(ROOT).as_posix() for p in required if not p.exists()] == []


def test_markdown_image_links_point_to_existing_files():
    image_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    missing: list[str] = []
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        for match in image_pattern.finditer(text):
            target = match.group(1).split()[0]
            if target.startswith(("http://", "https://")):
                continue
            target_path = (path.parent / target).resolve()
            try:
                target_path.relative_to(ROOT)
            except ValueError:
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
                continue
            if not target_path.exists():
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
    assert missing == []
