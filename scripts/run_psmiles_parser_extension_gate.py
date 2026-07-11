#!/usr/bin/env python
"""Run Step-17 PSMILES-aware pMSBP parser extension gate."""

from __future__ import annotations

from pathlib import Path

from msbp_tg.psmiles_parser import write_step17_outputs


def main() -> None:
    root = Path(".").resolve()
    out = root / "results" / "step17_psmiles_parser_extension_gate"
    verdict = write_step17_outputs(root, out)

    print("Step-17 PSMILES-aware pMSBP parser extension gate")
    print(f"Output directory: {out}")
    print(f"Verdict: {verdict}")

    if verdict == "STEP17_PSMILES_PARSER_EXTENDED_COVERAGE_PASS":
        print("PASS: PSMILES parser coverage is high enough to proceed to Step 18 open-data re-analysis.")
    elif verdict == "STEP17_PSMILES_PARSER_EXTENDED_BUT_COVERAGE_LIMITED":
        print("PASS with limitation: parser works but coverage is limited. Extend parser or restrict supported subset.")
    else:
        print("AUDIT COMPLETE: parser coverage is not yet enough for full re-analysis.")


if __name__ == "__main__":
    main()
