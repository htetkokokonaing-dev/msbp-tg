#!/usr/bin/env python
"""Run Step-16 open row-level dataset strategy gate."""

from __future__ import annotations

from pathlib import Path

from msbp_tg.open_dataset_audit import write_step16_outputs


def main() -> None:
    root = Path(".").resolve()
    out = root / "results" / "step16_open_row_level_dataset_gate"
    verdict = write_step16_outputs(root, out)

    print("Step-16 open row-level dataset strategy gate")
    print(f"Output directory: {out}")
    print(f"Verdict: {verdict}")

    if verdict == "STEP16_OPEN_ROW_LEVEL_DATA_FOUND_PMSBP_PARSER_MUST_BE_EXTENDED":
        print("PASS: open row-level dataset found. Current pMSBP parser must be extended before full re-analysis.")
    elif verdict == "STEP16_OPEN_DATA_READY_FOR_PMSBP_REANALYSIS":
        print("PASS: open row-level dataset and sufficient current pMSBP coverage found.")
    else:
        print("AUDIT COMPLETE: open row-level data is not ready yet.")


if __name__ == "__main__":
    main()
