from msbp_tg.periodic_fiber import (
    assert_same_periodic_coordinate,
    canonical_period_string,
    naive_msbp_density_from_two_terminal_smiles,
    periodic_invariance_table,
    periodic_msbp,
    periodic_msbp_density,
    representation_class,
)


def test_step13_carbon_supercell_gate_still_passes():
    assert_same_periodic_coordinate(["*CC*", "*CCCC*", "*CCCCCC*"])
    assert [representation_class(s) for s in ["*CC*", "*CCCC*", "*CCCCCC*"]] == ["*CC*", "*CC*", "*CC*"]
    assert periodic_msbp_density("*CC*") == -0.5


def test_naive_coordinate_remains_negative_control_for_carbon_supercells():
    rows = [naive_msbp_density_from_two_terminal_smiles(s) for s in ["*CC*", "*CCCC*", "*CCCCCC*"]]
    assert len({r[2] for r in rows}) == 3


def test_orientation_reversal_invariance():
    assert_same_periodic_coordinate(["*CO*", "*OC*"])
    assert representation_class("*CO*") == representation_class("*OC*")


def test_cut_point_relocation_invariance_for_three_atom_period():
    # Same periodic token sequence C-C-O written from three possible cut points.
    assert_same_periodic_coordinate(["*CCO*", "*COC*", "*OCC*"])
    assert len({canonical_period_string(s) for s in ["*CCO*", "*COC*", "*OCC*"]}) == 1


def test_equivalent_simple_smiles_spelling_invariance():
    assert_same_periodic_coordinate(["*CC*", "*C-C*", "*[C][C]*"])
    assert representation_class("*C-C*") == "*CC*"


def test_noncarbon_supercell_invariance():
    assert_same_periodic_coordinate(["*CO*", "*COCO*", "*COCOCO*"])
    assert representation_class("*COCOCO*") == representation_class("*CO*")


def test_simple_copolymer_expansion_gate():
    assert_same_periodic_coordinate(["*CN*", "*CNCN*", "*CNCNCN*"])
    assert representation_class("*CNCNCN*") == representation_class("*CN*")


def test_advanced_invariance_table_schema_has_canonical_period():
    rows = periodic_invariance_table(["*CCO*", "*COC*", "*OCC*"])
    assert "canonical_period" in rows[0]
    assert len({row["representation_class"] for row in rows}) == 1
