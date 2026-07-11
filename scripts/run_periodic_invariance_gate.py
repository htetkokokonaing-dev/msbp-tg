#!/usr/bin/env python
"""Run the Step-13 periodic MSBP representation-invariance gate."""

from __future__ import annotations

import csv
from pathlib import Path

from msbp_tg.periodic_fiber import periodic_invariance_table


def main() -> None:
    smiles = ["*CC*", "*CCCC*", "*CCCCCC*"]
    rows = periodic_invariance_table(smiles)

    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "periodic_msbp_invariance_gate.csv"

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    values = {row["periodic_msbp_density"] for row in rows}
    classes = {row["representation_class"] for row in rows}

    print("Step-13 periodic MSBP representation-invariance gate")
    print(f"Rows written: {out_csv}")
    print(f"periodic_msbp_density values: {sorted(values)}")
    print(f"representation classes: {sorted(classes)}")

    if len(values) != 1:
        raise SystemExit("FAIL: pMSBP density is not invariant across supercells")
    if classes != {"*CC*"}:
        raise SystemExit("FAIL: representation class is not stable")

    print("PASS: *CC*, *CCCC*, and *CCCCCC* map to the same pMSBP coordinate.")


if __name__ == "__main__":
    main()
