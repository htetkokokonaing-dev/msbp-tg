from msbp_tg.overlap import canonical_overlap

def test_canonical_overlap_detects_shared_smiles():
    candidate = ['CCO', 'CCCC']
    prior = ['OCC', 'c1ccccc1']
    overlap = canonical_overlap(candidate, prior)
    assert overlap == {0}
