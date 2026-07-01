#!/usr/bin/env python
from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from msbp_tg.validation import read_feature_table, validate_axis

def emit_validation_warnings(result, work, min_rows_per_fiber: int = 3) -> list[str]:
    """Return and print user-facing warnings for degenerate validation cases."""
    warnings: list[str] = []
    fiber_col = result.fiber
    if fiber_col in work.columns:
        group_sizes = work.groupby(fiber_col).size()
        small = int((group_sizes < min_rows_per_fiber).sum())
        if small:
            warnings.append(
                f"Warning: {small}/{len(group_sizes)} fibers have fewer than {min_rows_per_fiber} rows; "
                "within-fiber residual metrics may be unstable or undefined."
)
        if len(group_sizes) == len(work):
            warnings.append(
                "Warning: each retained row is in a separate fiber; residualized Spearman rho and sign accuracy may be undefined."
)
    if math.isnan(result.spearman_rho):
        warnings.append("Warning: Spearman rho is NaN; check sample size, fiber grouping, and nonconstant residuals.")
    if math.isnan(result.sign_accuracy):
        warnings.append("Warning: sign accuracy is NaN; at least eight retained rows and nonzero residual signs are needed.")
    for warning in warnings:
        print(warning, file=sys.stderr)
    return warnings

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a frozen MSBP axis on a feature table.")
    parser.add_argument("--input", required=True, help="CSV/XLSX feature table")
    parser.add_argument("--axis", required=True, help="Axis column, e.g. mobility_suppression_density")
    parser.add_argument("--t", default=None, help="Tg column; inferred if omitted")
    parser.add_argument("--fiber", default=None, help="Fiber column; inferred if omitted")
    parser.add_argument("--out", required=True, help="Output CSV path")
    args = parser.parse_args()

    df = read_feature_table(args.input)
    result, work = validate_axis(df, axis_col=args.axis, target_col=args.t, fiber_col=args.fiber)
    emit_validation_warnings(result, work)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.to_frame().to_csv(out, index=False)
    print(result.to_frame().to_string(index=False))

if __name__ == "__main__":
    main()
