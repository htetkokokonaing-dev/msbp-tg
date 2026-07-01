from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SUMMARY_KEY_BY_STAGE = {
    "10": "stage10_tsaicying_leak_excluded",
    "11": "stage11_neurips_combined",
    "13": "stage13_leeds_paek",
}

ENTROPY_KEY_BY_STAGE = {
    "10": "Stage 10",
    "11": "Stage 11",
    "13": "Stage 13",
}

CV_EXPECTED_BY_STAGE = {
    "10": 0.29748054909702837,
    "11": 0.29610454167706374,
    "13": 0.6449713032785899,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_manuscript_validation_evidence_table_matches_locked_summary_sources() -> None:
    evidence = read_csv(ROOT / "manuscript" / "MSBP_Validation_Evidence_Table.csv")
    summary_rows = read_csv(ROOT / "results" / "three_source_recomputed_summary.csv")
    entropy_rows = read_csv(ROOT / "tables" / "entropy_shuffle_empirical_p.csv")

    summary_by_source = {row["source"]: row for row in summary_rows}
    entropy_by_stage = {}
    for row in entropy_rows:
        for stage, label in ENTROPY_KEY_BY_STAGE.items():
            if label in row["source"]:
                entropy_by_stage[stage] = row

    assert sorted(row["stage"] for row in evidence) == ["10", "11", "13"]
    for row in evidence:
        stage = row["stage"]
        locked = summary_by_source[SUMMARY_KEY_BY_STAGE[stage]]
        entropy = entropy_by_stage[stage]
        assert float(row["spearman_rho"]) == round(float(locked["spearman_rho"]), 4)
        assert float(row["sign_accuracy"]) == round(float(locked["sign_accuracy"]), 4)
        assert float(row["entropy_excess_nats"]) == round(float(entropy["entropy_excess_over_p95"]), 4)
        assert float(row["cv_r2_gain_vs_family_size"]) == round(CV_EXPECTED_BY_STAGE[stage], 4)


def test_manuscript_validation_evidence_table_is_marked_as_msbp_density_axis() -> None:
    evidence = read_csv(ROOT / "manuscript" / "MSBP_Validation_Evidence_Table.csv")
    assert all(row["axis"] == "MSBP density = -rot/heavy" for row in evidence)
