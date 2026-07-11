from pathlib import Path
import csv

from msbp_tg.pmsbp_reanalysis import discover_candidate_tables, write_step15_outputs


def test_step15_audit_no_row_level_table(tmp_path: Path):
    (tmp_path / "tables").mkdir()
    with (tmp_path / "tables" / "aggregate.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source", "rho", "n"])
        w.writeheader()
        w.writerow({"source": "demo", "rho": "0.5", "n": "10"})

    verdict = write_step15_outputs(tmp_path, tmp_path / "results")
    assert verdict == "PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS"
    assert (tmp_path / "results" / "pmsbp_candidate_table_audit.csv").exists()


def test_step15_audit_with_row_level_table(tmp_path: Path):
    (tmp_path / "data").mkdir()
    with (tmp_path / "data" / "row_level.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["smiles", "Tg", "visible_fiber"])
        w.writeheader()
        w.writerow({"smiles": "*CC*", "Tg": "100", "visible_fiber": "A"})
        w.writerow({"smiles": "*CCCC*", "Tg": "110", "visible_fiber": "A"})
        w.writerow({"smiles": "*CO*", "Tg": "120", "visible_fiber": "B"})
        w.writerow({"smiles": "*COCO*", "Tg": "125", "visible_fiber": "B"})

    candidates = discover_candidate_tables(tmp_path)
    assert any(c.is_row_level_candidate for c in candidates)

    verdict = write_step15_outputs(tmp_path, tmp_path / "results")
    assert verdict == "PASS_WITH_ROW_LEVEL_REANALYSIS"
    assert (tmp_path / "results" / "pmsbp_refeature_rows_public_safe.csv").exists()
