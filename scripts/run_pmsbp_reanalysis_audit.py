#!/usr/bin/env python
"""Run Step-15 pMSBP re-feature / re-analysis audit."""

from __future__ import annotations

from pathlib import Path

from msbp_tg.pmsbp_reanalysis import write_step15_outputs


def main() -> None:
    root = Path(".").resolve()
    output_dir = root / "results" / "step15_pmsbp_reanalysis_audit"
    verdict = write_step15_outputs(root, output_dir)

    print("Step-15 pMSBP re-feature / re-analysis audit")
    print(f"Output directory: {output_dir}")
    print(f"Verdict: {verdict}")

    if verdict == "PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS":
        print("PASS: audit completed. No public-safe row-level SMILES/Tg table was found for full re-analysis.")
    elif verdict == "PASS_WITH_ROW_LEVEL_REANALYSIS":
        print("PASS: audit completed and at least one row-level candidate table was re-featured.")
    else:
        raise SystemExit(f"Unexpected verdict: {verdict}")


if __name__ == "__main__":
    main()
