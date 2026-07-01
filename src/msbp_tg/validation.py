from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from.metrics import (
    entropy_gain_by_bins,
    quartile_sign_accuracy,
    quantile_bins,
    residualize_by_group,
    spearman_corr,
)

@dataclass
class AxisValidationResult:
    n: int
    n_fibers: int
    axis: str
    target: str
    fiber: str
    spearman_rho: float
    spearman_p: float
    sign_accuracy: float
    entropy_gain_nats: float

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([self.__dict__])

def infer_target_column(df: pd.DataFrame) -> str:
    for col in ["Tg_C", "Tg", "Tg_value_raw", "Tg_K"]:
        if col in df.columns:
            return col
    raise ValueError("Could not infer Tg target column. Pass --t explicitly.")

def infer_fiber_column(df: pd.DataFrame) -> str:
    for col in ["visible_dataset_fiber", "fiber", "visible_class", "raw_family"]:
        if col in df.columns:
            return col
    raise ValueError("Could not infer fiber column. Pass --fiber explicitly.")

def validate_axis(
    df: pd.DataFrame,
    axis_col: str,
    target_col: Optional[str] = None,
    fiber_col: Optional[str] = None,
    high_boundary_col: Optional[str] = None,
) -> tuple[AxisValidationResult, pd.DataFrame]:
    """Validate a mobility-suppression axis within visible fibers.

    The function residualizes target and axis inside the fiber by using
    residualize_by_group(), whose public protocol subtracts the within-fiber
    mean. It then reports Spearman correlation, strong-quartile sign
    accuracy, and entropy gain.
    """
    target_col = target_col or infer_target_column(df)
    fiber_col = fiber_col or infer_fiber_column(df)
    if axis_col not in df.columns:
        raise ValueError(f"Missing axis column: {axis_col}")
    if target_col not in df.columns:
        raise ValueError(f"Missing target column: {target_col}")
    if fiber_col not in df.columns:
        raise ValueError(f"Missing fiber column: {fiber_col}")

    work = df.copy()
    work[target_col] = pd.to_numeric(work[target_col], errors="coerce")
    work[axis_col] = pd.to_numeric(work[axis_col], errors="coerce")
    work = work.dropna(subset=[target_col, axis_col, fiber_col])
    work = work[work[fiber_col].astype(str).str.len() > 0].copy()
    work["Tg_resid_fiber"] = residualize_by_group(work, target_col, fiber_col)
    work["axis_resid_fiber"] = residualize_by_group(work, axis_col, fiber_col)

    rho, p = spearman_corr(work["axis_resid_fiber"], work["Tg_resid_fiber"])
    acc = quartile_sign_accuracy(work["axis_resid_fiber"], work["Tg_resid_fiber"])

    if high_boundary_col and high_boundary_col in work.columns:
        label = high_boundary_col
    elif "target_high_Tg_boundary" in work.columns:
        label = "target_high_Tg_boundary"
    else:
        # Create a within-table high-Tg boundary label using median target.
        label = "target_high_Tg_boundary"
        work[label] = (work[target_col] >= work[target_col].median()).astype(int)

    work["axis_quantile_bin"] = quantile_bins(work[axis_col], q=4)
    entropy_gain = entropy_gain_by_bins(work, label, "axis_quantile_bin")

    result = AxisValidationResult(
        n=int(len(work)),
        n_fibers=int(work[fiber_col].nunique()),
        axis=axis_col,
        target=target_col,
        fiber=fiber_col,
        spearman_rho=rho,
        spearman_p=p,
        sign_accuracy=acc,
        entropy_gain_nats=entropy_gain,
)
    return result, work

def read_feature_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    return pd.read_csv(path)
