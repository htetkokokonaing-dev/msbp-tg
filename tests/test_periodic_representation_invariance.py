from msbp_tg.periodic_fiber import (
    naive_msbp_density_from_two_terminal_smiles,
    periodic_msbp,
    periodic_msbp_density,
    periodic_invariance_table,
)


def test_editorial_blocker_naive_density_is_representation_sensitive():
    rows = [naive_msbp_density_from_two_terminal_smiles(s) for s in ["*CC*", "*CCCC*", "*CCCCCC*"]]
    assert rows[0][0] == 2
    assert rows[1][0] == 4
    assert rows[2][0] == 6
    assert rows[0][1] == 1
    assert rows[1][1] == 3
    assert rows[2][1] == 5
    assert len({r[2] for r in rows}) == 3


def test_periodic_msbp_is_invariant_for_linear_carbon_supercells():
    values = [periodic_msbp_density(s) for s in ["*CC*", "*CCCC*", "*CCCCCC*"]]
    assert len(set(values)) == 1
    assert values[0] == -0.5


def test_periodic_representation_class_is_stable_for_linear_carbon_supercells():
    classes = [periodic_msbp(s).representation_class for s in ["*CC*", "*CCCC*", "*CCCCCC*"]]
    assert classes == ["*CC*", "*CC*", "*CC*"]


def test_periodic_invariance_table_schema():
    rows = periodic_invariance_table(["*CC*", "*CCCC*", "*CCCCCC*"])
    assert len(rows) == 3
    required = {
        "smiles",
        "heavy_atoms",
        "naive_rotatable_bonds",
        "naive_msbp_density",
        "primitive_period_heavy_atoms",
        "periodic_rotatable_bonds_per_period",
        "periodic_msbp_density",
        "representation_class",
        "notes",
    }
    assert required.issubset(rows[0].keys())
