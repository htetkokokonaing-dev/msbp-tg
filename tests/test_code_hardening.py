from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def load_script(name: str):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def test_release_zip_excludes_cache_and_bytecode_paths():
    module = load_script("make_release_zip.py")
    assert not module.should_include(ROOT / ".pytest_cache" / "README.md", root=ROOT)
    assert not module.should_include(ROOT / "src" / "msbp_tg" / "__pycache__" / "features.cpython-311.pyc", root=ROOT)
    assert not module.should_include(ROOT / "src" / "msbp_tg.egg-info" / "PKG-INFO", root=ROOT)
    assert not module.should_include(ROOT / "src" / "msbp_tg" / "features.pyc", root=ROOT)
    assert module.should_include(ROOT / "README.md", root=ROOT)

def test_summary_no_data_does_not_overwrite_existing_summary(tmp_path, monkeypatch, capsys):
    module = load_script("run_stage10_11_13_summary.py")
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    summary = results_dir / "three_source_recomputed_summary.csv"
    original = "source,spearman_rho\nexisting,0.5\n"
    summary.write_text(original)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "SOURCES", [
        {
            "name": "missing_source",
            "path": "data/processed/missing.csv",
            "axis": "mobility_suppression_density",
            "target": "Tg",
            "fiber": "fiber",
        }
    ])
    module.main()
    captured = capsys.readouterr()
    assert "not overwritten" in captured.out
    assert summary.read_text() == original

def test_validate_feature_table_emits_small_fiber_warning(capsys):
    module = load_script("validate_feature_table.py")
    from msbp_tg.validation import validate_axis

    df = pd.DataFrame({
        "mobility_suppression_density": [-0.1, -0.2, -0.3],
        "Tg": [100, 120, 140],
        "fiber": ["a", "b", "c"],
    })
    result, work = validate_axis(df, axis_col="mobility_suppression_density", target_col="Tg", fiber_col="fiber")
    warnings = module.emit_validation_warnings(result, work)
    captured = capsys.readouterr()
    assert any("fewer than" in w for w in warnings)
    assert "Warning:" in captured.err
