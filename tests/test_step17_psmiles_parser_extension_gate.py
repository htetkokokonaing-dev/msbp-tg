from pathlib import Path
import csv

from msbp_tg.psmiles_parser import (
    parse_psmiles_to_pmsbp,
    write_step17_outputs,
)


def test_psmiles_parser_supports_bracketed_outer_dummies():
    r = parse_psmiles_to_pmsbp("[*]CC[*]")
    assert r.status == "supported"
    assert r.representation_class == "*CC*"
    assert r.pmsbp_density == -0.5


def test_psmiles_parser_supports_simple_equivalent_spelling():
    a = parse_psmiles_to_pmsbp("[*]C-C[*]")
    b = parse_psmiles_to_pmsbp("[*][C][C][*]")
    assert a.status == "supported"
    assert b.status == "supported"
    assert a.representation_class == b.representation_class == "*CC*"


def test_psmiles_parser_orientation_reversal():
    a = parse_psmiles_to_pmsbp("[*]CO[*]")
    b = parse_psmiles_to_pmsbp("[*]OC[*]")
    assert a.representation_class == b.representation_class


def test_psmiles_parser_supports_complex_polymetrix_like_string():
    r = parse_psmiles_to_pmsbp("[*]#C[SiH2]C#Cc1cccc(C#[*])c1")
    assert r.status == "supported"
    assert r.representation_class.startswith("*")
    assert r.representation_class.endswith("*")


def test_step17_gate_on_synthetic_polymetrix_file(tmp_path: Path):
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
        w.writerow({"PSMILES": "[*]CC[*]", "labels.Exp_Tg(K)": "300", "meta.source": "demo", "meta.polymer_class": "A", "meta.reliability": "black"})
        w.writerow({"PSMILES": "[*]CCCC[*]", "labels.Exp_Tg(K)": "310", "meta.source": "demo", "meta.polymer_class": "A", "meta.reliability": "black"})
        w.writerow({"PSMILES": "[*]CO[*]", "labels.Exp_Tg(K)": "330", "meta.source": "demo", "meta.polymer_class": "B", "meta.reliability": "black"})
        w.writerow({"PSMILES": "[*]#C[SiH2]C#Cc1cccc(C#[*])c1", "labels.Exp_Tg(K)": "345", "meta.source": "demo", "meta.polymer_class": "C", "meta.reliability": "black"})

    verdict = write_step17_outputs(tmp_path, tmp_path / "results")
    assert verdict == "STEP17_PSMILES_PARSER_EXTENDED_COVERAGE_PASS"
    assert (tmp_path / "results" / "polymetrix_psmiles_parser_coverage_summary.csv").exists()
