from __future__ import annotations

import importlib.metadata
from pathlib import Path

import msbp_tg

ROOT = Path(__file__).resolve().parents[1]


def test_package_has_standard_init_file_and_no_legacy_init_name() -> None:
    assert (ROOT / "src" / "msbp_tg" / "__init__.py").exists()
    assert not (ROOT / "src" / "msbp_tg" / "_init.py").exists()
    assert msbp_tg.__version__ == "preprint"


def test_editable_distribution_metadata_is_available_after_install() -> None:
    assert importlib.metadata.version("msbp-tg") == "0.1.0"


def test_readme_documents_pip_editable_workflow() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python -m pip install -e ." in readme
    assert "PYTHONPATH=src" not in readme
