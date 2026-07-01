from __future__ import annotations

import math
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

try:
    from scipy.stats import spearmanr
except Exception:  # pragma: no cover
    spearmanr = None

def residualize_by_group(df: pd.DataFrame, value_col: str, group_col: str) -> pd.Series:
    """Return residuals after subtracting the mean within a visible fiber/group."""
    values = pd.to_numeric(df[value_col], errors="coerce")
    group_means = values.groupby(df[group_col]).transform("mean")
    return values - group_means

def spearman_corr(x: Sequence[float], y: Sequence[float]) -> tuple[float, float]:
    """Spearman correlation with a rank-correlation fallback if scipy is unavailable."""
    xs = pd.Series(x, dtype="float64")
    ys = pd.Series(y, dtype="float64")
    mask = xs.notna() & ys.notna()
    xs = xs[mask]
    ys = ys[mask]
    if len(xs) < 3:
        return float("nan"), float("nan")
    if xs.nunique(dropna=True) < 2 or ys.nunique(dropna=True) < 2:
        return float("nan"), float("nan")
    if spearmanr is not None:
        rho, p = spearmanr(xs, ys)
        return float(rho), float(p)
    return float(xs.rank().corr(ys.rank())), float("nan")

def binary_entropy_rate(labels: Iterable[int]) -> float:
    """Binary entropy in nats for labels that can be converted to 0/1."""
    s = pd.Series(list(labels)).dropna().astype(int)
    if len(s) == 0:
        return float("nan")
    p = s.mean()
    if p <= 0 or p >= 1:
        return 0.0
    return float(-(p * math.log(p) + (1 - p) * math.log(1 - p)))

def entropy_gain_by_bins(df: pd.DataFrame, label_col: str, bin_col: str) -> float:
    """Parent entropy minus weighted child entropy after splitting by an axis bin."""
    work = df[[label_col, bin_col]].dropna().copy()
    if work.empty:
        return float("nan")
    parent = binary_entropy_rate(work[label_col])
    child = 0.0
    n = len(work)
    for _, sub in work.groupby(bin_col):
        child += (len(sub) / n) * binary_entropy_rate(sub[label_col])
    return float(parent - child)

def quartile_sign_accuracy(axis_resid: Sequence[float], target_resid: Sequence[float]) -> float:
    """Sign accuracy on the top and bottom quartiles of the axis residual."""
    df = pd.DataFrame({"axis": axis_resid, "target": target_resid}).dropna()
    if len(df) < 8:
        return float("nan")
    q1 = df["axis"].quantile(0.25)
    q3 = df["axis"].quantile(0.75)
    strong = df[(df["axis"] <= q1) | (df["axis"] >= q3)].copy()
    if strong.empty:
        return float("nan")
    pred = np.sign(strong["axis"].to_numpy())
    actual = np.sign(strong["target"].to_numpy())
    keep = (pred != 0) & (actual != 0)
    if keep.sum() == 0:
        return float("nan")
    return float((pred[keep] == actual[keep]).mean())

def quantile_bins(values: Sequence[float], q: int = 4) -> pd.Series:
    """Quantile bins with duplicate-edge handling."""
    s = pd.Series(values, dtype="float64")
    try:
        return pd.qcut(s, q=q, labels=False, duplicates="drop")
    except ValueError:
        return pd.Series(np.zeros(len(s)), index=s.index)

def bootstrap_spearman_ci(x, y, n_boot: int = 1000, seed: int = 42, alpha: float = 0.05):
    """Percentile bootstrap confidence interval for Spearman rho."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({'x': x, 'y': y}).dropna().reset_index(drop=True)
    if len(df) < 4:
        return float('nan'), float('nan'), float('nan')
    obs, _ = spearman_corr(df['x'], df['y'])
    vals = []
    n = len(df)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        rho, _ = spearman_corr(df.loc[idx, 'x'], df.loc[idx, 'y'])
        if not np.isnan(rho):
            vals.append(rho)
    lo, hi = np.quantile(vals, [alpha / 2, 1 - alpha / 2])
    return float(obs), float(lo), float(hi)

def paired_bootstrap_rho_difference(axis_a, axis_b, target, n_boot: int = 1000, seed: int = 42):
    """Bootstrap CI for difference in absolute Spearman rho against same target."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({'a': axis_a, 'b': axis_b, 'target': target}).dropna().reset_index(drop=True)
    if len(df) < 4:
        return float('nan'), float('nan'), float('nan'), float('nan')
    rho_a, _ = spearman_corr(df['a'], df['target'])
    rho_b, _ = spearman_corr(df['b'], df['target'])
    obs = abs(rho_a) - abs(rho_b)
    vals = []
    n = len(df)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        ra, _ = spearman_corr(df.loc[idx, 'a'], df.loc[idx, 'target'])
        rb, _ = spearman_corr(df.loc[idx, 'b'], df.loc[idx, 'target'])
        if not (np.isnan(ra) or np.isnan(rb)):
            vals.append(abs(ra) - abs(rb))
    lo, hi = np.quantile(vals, [0.025, 0.975])
    p_two = (1 + min(sum(v <= 0 for v in vals), sum(v >= 0 for v in vals)) * 2) / (1 + len(vals))
    return float(obs), float(lo), float(hi), float(min(1.0, p_two))
