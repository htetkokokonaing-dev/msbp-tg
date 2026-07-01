#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from msbp_tg.validation import read_feature_table, validate_axis

SOURCES = [
    {
        "name": "stage10_tsaicying_leak_excluded",
        "path": "data/processed/stage10_tsaicying_leak_excluded_novel_features.csv",
        "axis": "mobility_suppression_density",
        "target": "Tg_C",
        "fiber": "visible_dataset_fiber",
    },
    {
        "name": "stage11_neurips_combined",
        "path": "data/processed/stage11_neurips_public_private_tg_known_novel_features.csv",
        "axis": "mobility_suppression_density",
        "target": "Tg",
        "fiber": "visible_dataset_fiber",
    },
    {
        "name": "stage13_leeds_paek",
        "path": "data/processed/stage13_leeds_paek_novel_features.csv",
        "axis": "mobility_suppression_density",
        "target": "Tg_value_raw",
        "fiber": "fiber",
    },
]

NO_DATA_MESSAGE = (
    "No external validation feature tables were found. Raw/processed third-party datasets "
    "are not bundled in the public-safe repository. Follow data/README_data_public_safe.md "
    "and docs/reproducibility_protocol.md to prepare the feature tables first. Existing "
    "summary results were not overwritten."
)

def main() -> None:
    rows = []
    missing = []
    for src in SOURCES:
        path = ROOT / src["path"]
        if not path.exists():
            missing.append(src["path"])
            continue
        df = read_feature_table(path)
        result, _ = validate_axis(df, axis_col=src["axis"], target_col=src["target"], fiber_col=src["fiber"])
        row = result.__dict__.copy()
        row["source"] = src["name"]
        rows.append(row)

    out = ROOT / "results" / "three_source_recomputed_summary.csv"
    if not rows:
        print(NO_DATA_MESSAGE)
        if missing:
            print("Missing expected feature tables:")
            for item in missing:
                print(f" - {item}")
        return

    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    if missing:
        print("Skipped missing feature tables:")
        for item in missing:
            print(f" - {item}")
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
