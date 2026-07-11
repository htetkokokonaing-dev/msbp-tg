from pathlib import Path
import csv

from msbp_tg.open_dataset_audit import write_step16_outputs, audit_polymetrix


def test_step16_detects_polymetrix_required_columns(tmp_path: Path):
    p = tmp_path / "data" / "open_row_level"
    p.mkdir(parents=True)
    with (p / "LAMALAB_CURATED_Tg_structured_polymerclass.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "PSMILES",
                "labels.Exp_Tg(K)",
                "meta.source",
                "meta.polymer_class",
                "meta.reliability",
            ],
        )
        w.writeheader()
        w.writerow({
            "PSMILES": "[*]CC[*]",
            "labels.Exp_Tg(K)": "300.0",
            "meta.source": "demo",
            "meta.polymer_class": "demo_class",
            "meta.reliability": "black",
        })
        w.writerow({
            "PSMILES": "[*]COCO[*]",
            "labels.Exp_Tg(K)": "350.0",
            "meta.source": "demo",
            "meta.polymer_class": "demo_class",
            "meta.reliability": "black",
        })

    audit, sample = audit_polymetrix(tmp_path)
    assert audit.exists
    assert audit.has_psmiles
    assert audit.has_tg
    assert audit.n_rows == 2
    assert audit.n_supported_by_current_pmsbp == 2

    verdict = write_step16_outputs(tmp_path, tmp_path / "results")
    assert verdict == "STEP16_OPEN_DATA_READY_FOR_PMSBP_REANALYSIS"


def test_step16_missing_dataset(tmp_path: Path):
    verdict = write_step16_outputs(tmp_path, tmp_path / "results")
    assert verdict == "STEP16_OPEN_ROW_LEVEL_DATA_NOT_READY"
