#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from msbp_tg.features import add_smiles_features
from msbp_tg.fiber import add_visible_fiber

def main() -> None:
    p = argparse.ArgumentParser(description="Extract frozen MSBP mobility features from raw SMILES.")
    p.add_argument("--input", required=True)
    p.add_argument("--smiles-col", default="SMILES")
    p.add_argument("--family-col", default=None)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    df = pd.read_csv(args.input)
    feat = add_smiles_features(df, smiles_col=args.smiles_col)
    feat = add_visible_fiber(feat, family_col=args.family_col, size_col="heavy_atoms")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    feat.to_csv(out, index=False)
    print(f"wrote {out} rows={len(feat)}")

if __name__ == "__main__":
    main()
