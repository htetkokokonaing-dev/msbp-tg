#!/usr/bin/env python
"""Run Step-18 open-data pMSBP statistical re-analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from msbp_tg.open_data_reanalysis import write_step18_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-bootstrap", type=int, default=200)
    parser.add_argument("--n-permutation", type=int, default=200)
    parser.add_argument("--seed", type=int, default=1729)
    args = parser.parse_args()

    root = Path(".").resolve()
    out = root / "results" / "step18_open_data_pmsbp_reanalysis"
    verdict = write_step18_outputs(
        root,
        out,
        n_bootstrap=args.n_bootstrap,
        n_permutation=args.n_permutation,
        seed=args.seed,
    )

    print("Step-18 open-data pMSBP statistical re-analysis")
    print(f"Output directory: {out}")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    main()
