#!/usr/bin/env python
"""Run Step-14 advanced periodic MSBP invariance gates."""

from __future__ import annotations

import csv
from pathlib import Path

from msbp_tg.periodic_fiber import periodic_invariance_table


GATES = {
    "step13_carbon_supercell": ["*CC*", "*CCCC*", "*CCCCCC*"],
    "orientation_reversal": ["*CO*", "*OC*"],
    "cut_point_relocation": ["*CCO*", "*COC*", "*OCC*"],
    "equivalent_simple_spelling": ["*CC*", "*C-C*", "*[C][C]*"],
    "noncarbon_supercell": ["*CO*", "*COCO*", "*COCOCO*"],
    "simple_copolymer_expansion": ["*CN*", "*CNCN*", "*CNCNCN*"],
}


def main() -> None:
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "periodic_msbp_advanced_invariance_gate.csv"

    all_rows: list[dict[str, object]] = []
    for gate, smiles_list in GATES.items():
        rows = periodic_invariance_table(smiles_list)
        values = {row["periodic_msbp_density"] for row in rows}
        classes = {row["representation_class"] for row in rows}
        status = "PASS" if len(values) == 1 and len(classes) == 1 else "FAIL"

        print(f"{gate}: {status}")
        print(f"  values: {sorted(values)}")
        print(f"  classes: {sorted(classes)}")

        for row in rows:
            row = dict(row)
            row["gate"] = gate
            row["gate_status"] = status
            all_rows.append(row)

        if status != "PASS":
            raise SystemExit(f"FAIL: {gate}")

    fieldnames = ["gate", "gate_status"] + [k for k in all_rows[0].keys() if k not in {"gate", "gate_status"}]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Rows written: {out_csv}")
    print("PASS: all Step-14 advanced periodic MSBP invariance gates passed.")


if __name__ == "__main__":
    main()
