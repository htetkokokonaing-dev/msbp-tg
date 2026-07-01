import math

from msbp_tg.features import extract_smiles_features, canonicalize_smiles

def test_dummy_atom_repeat_unit_parses_when_rdkit_allows():
    f = extract_smiles_features('*CC*')
    assert f.valid_rdkit
    assert f.heavy_atoms >= 2
    assert f.canonical_smiles is not None

def test_silicon_atom_feature_is_extracted():
    f = extract_smiles_features('C[Si](C)(C)O')
    assert f.valid_rdkit
    assert f.silicon_atoms == 1

def test_msbp_density_is_exact_sign_reversal_of_rot_density():
    f = extract_smiles_features('CCOCC')
    assert f.valid_rdkit
    assert f.rot_per_heavy is not None
    assert math.isclose(f.mobility_suppression_density, -f.rot_per_heavy, rel_tol=0, abs_tol=1e-12)

def test_canonicalize_reorders_equivalent_simple_smiles():
    a = canonicalize_smiles('OCC')
    b = canonicalize_smiles('CCO')
    assert a == b
