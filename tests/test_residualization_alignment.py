import pandas as pd

from msbp_tg.metrics import residualize_by_group

def test_residualize_by_group_subtracts_within_fiber_mean():
    df = pd.DataFrame({
        "fiber": ["A", "A", "B", "B"],
        "value": [1.0, 3.0, 10.0, 14.0],
    })
    resid = residualize_by_group(df, "value", "fiber")
    assert resid.tolist() == [-1.0, 1.0, -2.0, 2.0]

def test_residualization_mean_differs_from_median_when_group_is_skewed():
    df = pd.DataFrame({
        "fiber": ["A", "A", "A"],
        "value": [1.0, 2.0, 100.0],
    })
    resid = residualize_by_group(df, "value", "fiber")
    assert round(resid.iloc[0], 6) == round(1.0 - (103.0 / 3.0), 6)
    assert resid.iloc[0] != -1.0  # median-centered residual would be 1 - 2 = -1
