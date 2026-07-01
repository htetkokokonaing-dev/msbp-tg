from __future__ import annotations

import pandas as pd

def size_bin(series: pd.Series, q: int = 5) -> pd.Series:
    """Quantile size bin with duplicate-edge handling.

    If all values are identical, pandas.qcut can return all-NaN bins when
    duplicate quantile edges are dropped. For visible-fiber construction, that
    degenerate but valid case is assigned to size bin 0.
    """
    values = pd.to_numeric(series, errors="coerce")
    try:
        bins = pd.qcut(values, q=q, labels=False, duplicates="drop")
        bins = pd.Series(bins, index=series.index)
    except ValueError:
        bins = pd.Series([0] * len(series), index=series.index)

    if bins.isna().all():
        bins = pd.Series([0] * len(series), index=series.index)
    else:
        bins = bins.fillna(0)

    return bins.astype(int)

def simple_family_from_features(df: pd.DataFrame) -> pd.Series:
    """A simple chemistry-family heuristic for raw SMILES validation.

    This is not a chemically exhaustive classifier. It provides a reproducible
    visible fiber when a dataset lacks polymer-class labels.
    """
    def label(row):
        if row.get("silicon_atoms", 0) and row.get("silicon_atoms", 0) > 0:
            return "silicon_like"
        if row.get("aromatic_rings", 0) and row.get("aromatic_rings", 0) >= 2:
            return "multi_aromatic"
        if row.get("aromatic_rings", 0) and row.get("aromatic_rings", 0) == 1:
            return "aromatic"
        if row.get("hetero_atoms", 0) and row.get("hetero_atoms", 0) > 0:
            return "hetero_aliphatic"
        return "hydrocarbon_like"
    return df.apply(label, axis=1)

def add_visible_fiber(df: pd.DataFrame, family_col: str | None = None, size_col: str = "heavy_atoms", q: int = 5) -> pd.DataFrame:
    out = df.copy()
    if family_col and family_col in out.columns:
        fam = out[family_col].astype(str)
    elif "raw_family" in out.columns:
        fam = out["raw_family"].astype(str)
    elif "Polymer Class" in out.columns:
        fam = out["Polymer Class"].astype(str)
    else:
        fam = simple_family_from_features(out)
    out["size_bin"] = size_bin(out[size_col], q=q).astype("Int64").astype(str)
    out["visible_fiber"] = fam + "|size_" + out["size_bin"]
    return out
