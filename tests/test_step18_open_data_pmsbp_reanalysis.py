from pathlib import Path
import csv

from msbp_tg.open_data_reanalysis import (
    spearman,
    write_step18_outputs,
)


def test_spearman_basic_negative():
    assert spearman([1, 2, 3], [3, 2, 1]) == -1.0


def test_step18_synthetic_open_reanalysis(tmp_path: Path):
    data_dir = tmp_path / "data" / "open_row_level"
    data_dir.mkdir(parents=True)
    path = data_dir / "LAMALAB_CURATED_Tg_structured_polymerclass.csv"

    with path.open("w", newline="", encoding="utf-8") as f:
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
        # Two classes with internally negative relation between pMSBP and Tg.
        # pMSBP for CC is -0.5; CCO is -2/3; CCCO is -3/4.
        for cls, offset in [("A", 0), ("B", 100)]:
            w.writerow({"PSMILES": "[*]CC[*]", "labels.Exp_Tg(K)": str(300 + offset), "meta.source": "demo", "meta.polymer_class": cls, "meta.reliability": "black"})
            w.writerow({"PSMILES": "[*]CCO[*]", "labels.Exp_Tg(K)": str(330 + offset), "meta.source": "demo", "meta.polymer_class": cls, "meta.reliability": "black"})
            w.writerow({"PSMILES": "[*]CCCO[*]", "labels.Exp_Tg(K)": str(360 + offset), "meta.source": "demo", "meta.polymer_class": cls, "meta.reliability": "black"})

    verdict = write_step18_outputs(tmp_path, tmp_path / "results", n_bootstrap=20, n_permutation=20, seed=1)
    assert verdict in {
        "STEP18_GO_NEGATIVE_WITHIN_CLASS_SIGNAL_REANALYSIS_SUPPORTED",
        "STEP18_MIXED_RAW_SIGNAL_WITHIN_CLASS_NOT_LOCKED",
        "STEP18_NO_GO_INSUFFICIENT_ANALYSIS_SIGNAL",
    }
    assert (tmp_path / "results" / "overall_pmsbp_association_summary.csv").exists()
    assert (tmp_path / "results" / "polymetrix_open_pmsbp_feature_table.csv").exists()
