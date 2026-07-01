import pandas as pd

from msbp_tg.features import extract_smiles_features
from msbp_tg.fiber import add_visible_fiber, simple_family_from_features

def test_msbp_density_is_negative_rot_density():
    f = extract_smiles_features('CCOCC')
    assert f.valid_rdkit
    assert f.rot_per_heavy is not None
    assert abs(f.mobility_suppression_density + f.rot_per_heavy) < 1e-12

def test_silicon_atom_count_and_fiber_label():
    f = extract_smiles_features('C[Si](C)(C)O')
    assert f.valid_rdkit
    assert f.silicon_atoms == 1
    df = pd.DataFrame([f.__dict__])
    fam = simple_family_from_features(df).iloc[0]
    assert fam == 'silicon_like'

def test_visible_fiber_from_features_without_class_column():
    rows = [extract_smiles_features('c1ccccc1').__dict__, extract_smiles_features('CCCCCC').__dict__]
    out = add_visible_fiber(pd.DataFrame(rows), family_col=None, size_col='heavy_atoms', q=2)
    assert 'visible_fiber' in out.columns
    assert out['visible_fiber'].str.contains('size_').all()
