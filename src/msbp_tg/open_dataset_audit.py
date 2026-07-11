"""Open row-level dataset strategy gate for pMSBP revision.

Step 16 starts the Option-C path: rebuild the study on fully open row-level
polymer Tg data rather than relying on non-redistributable third-party rows.

This gate audits downloaded datasets and answers three questions:

1. Is an open row-level Tg dataset present?
2. Does it expose polymer representations and Tg values?
3. How many rows can the current Step-14 prototype pMSBP parser support?

The gate intentionally separates "dataset found" from "pMSBP re-analysis ready".
A dataset can be open and valid while the current pMSBP parser is still too
limited for complex PSMILES / BigSMILES.  That outcome is expected and useful.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import re
from typing import Iterable

from .periodic_fiber import periodic_msbp


POLYMETRIX_RELATIVE_PATH = Path("data/open_row_level/LAMALAB_CURATED_Tg_structured_polymerclass.csv")
FIGSHARE_ZIP_RELATIVE_PATH = Path("data/open_row_level/figshare_bigsmiles_tg/with_Tg.zip")
POLYVERSE_RELATIVE_DIR = Path("data/open_row_level/polyverse")

POLYMETRIX_SMILES_COL = "PSMILES"
POLYMETRIX_TG_COL = "labels.Exp_Tg(K)"
POLYMETRIX_SOURCE_COL = "meta.source"
POLYMETRIX_CLASS_COL = "meta.polymer_class"
POLYMETRIX_RELIABILITY_COL = "meta.reliability"


@dataclass(frozen=True)
class DatasetPresence:
    dataset: str
    path: str
    exists: bool
    size_bytes: int
    status: str


@dataclass(frozen=True)
class PolyMetriXAudit:
    path: str
    exists: bool
    n_rows: int
    has_psmiles: bool
    has_tg: bool
    n_nonempty_psmiles: int
    n_numeric_tg: int
    n_sources: int
    n_polymer_classes: int
    n_supported_by_current_pmsbp: int
    n_unsupported_by_current_pmsbp: int
    support_fraction: float
    verdict: str


def _read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except UnicodeDecodeError:
        with path.open("r", newline="", encoding="latin-1") as f:
            return list(csv.DictReader(f))


def _float_or_none(x: object) -> float | None:
    if x is None:
        return None
    try:
        y = float(str(x).strip())
    except Exception:
        return None
    if math.isnan(y) or math.isinf(y):
        return None
    return y


def _normalize_psmiles_for_current_gate(psmiles: str) -> str:
    """Normalize common PSMILES dummy spelling for the prototype parser.

    This does not solve BigSMILES/PSMILES parsing. It only converts bracketed
    dummy atoms to the Step-14 parser's `*` token and removes obvious whitespace.
    Unsupported complex strings remain unsupported by design.
    """

    s = str(psmiles).strip()
    s = s.replace("[*]", "*")
    s = s.replace("[*:", "*")  # defensive partial normalization
    s = re.sub(r"\s+", "", s)
    return s


def dataset_presence(root: Path) -> list[DatasetPresence]:
    """Return presence/status rows for downloaded open datasets."""

    checks: list[tuple[str, Path]] = [
        ("PolyMetriX curated Tg", POLYMETRIX_RELATIVE_PATH),
        ("Figshare BigSMILES Tg zip", FIGSHARE_ZIP_RELATIVE_PATH),
        ("polyVERSE archive directory", POLYVERSE_RELATIVE_DIR),
    ]

    out: list[DatasetPresence] = []
    for name, rel in checks:
        p = root / rel
        exists = p.exists()
        if p.is_dir():
            size = sum(q.stat().st_size for q in p.rglob("*") if q.is_file())
        elif p.is_file():
            size = p.stat().st_size
        else:
            size = 0

        if not exists:
            status = "MISSING"
        elif p.is_file() and size == 0:
            status = "EMPTY_DOWNLOAD"
        elif p.is_dir() and size > 0:
            status = "PRESENT_DIRECTORY"
        elif p.is_file() and size > 0:
            status = "PRESENT_FILE"
        else:
            status = "UNKNOWN"

        out.append(DatasetPresence(name, str(rel), exists, size, status))
    return out


def audit_polymetrix(root: Path) -> tuple[PolyMetriXAudit, list[dict[str, object]]]:
    """Audit PolyMetriX row-level Tg file and current pMSBP coverage."""

    path = root / POLYMETRIX_RELATIVE_PATH
    if not path.exists():
        audit = PolyMetriXAudit(
            path=str(POLYMETRIX_RELATIVE_PATH),
            exists=False,
            n_rows=0,
            has_psmiles=False,
            has_tg=False,
            n_nonempty_psmiles=0,
            n_numeric_tg=0,
            n_sources=0,
            n_polymer_classes=0,
            n_supported_by_current_pmsbp=0,
            n_unsupported_by_current_pmsbp=0,
            support_fraction=0.0,
            verdict="POLYMETRIX_MISSING",
        )
        return audit, []

    rows = _read_csv_dicts(path)
    fieldnames = set(rows[0].keys()) if rows else set()
    has_psmiles = POLYMETRIX_SMILES_COL in fieldnames
    has_tg = POLYMETRIX_TG_COL in fieldnames

    nonempty = 0
    numeric_tg = 0
    sources: set[str] = set()
    classes: set[str] = set()
    supported = 0
    unsupported = 0
    sample_rows: list[dict[str, object]] = []

    for idx, row in enumerate(rows):
        psmiles = row.get(POLYMETRIX_SMILES_COL, "") if has_psmiles else ""
        tg = _float_or_none(row.get(POLYMETRIX_TG_COL)) if has_tg else None
        source = row.get(POLYMETRIX_SOURCE_COL, "")
        polymer_class = row.get(POLYMETRIX_CLASS_COL, "")
        reliability = row.get(POLYMETRIX_RELIABILITY_COL, "")

        if str(psmiles).strip():
            nonempty += 1
        if tg is not None:
            numeric_tg += 1
        if source:
            sources.add(source)
        if polymer_class:
            classes.add(polymer_class)

        normalized = _normalize_psmiles_for_current_gate(psmiles)
        pmsbp_value = ""
        rep_class = ""
        status = "unsupported"
        error = ""

        if psmiles and tg is not None:
            try:
                r = periodic_msbp(normalized)
                pmsbp_value = r.periodic_msbp_density
                rep_class = r.representation_class
                status = "supported"
                supported += 1
            except Exception as exc:
                unsupported += 1
                error = type(exc).__name__
        else:
            unsupported += 1
            error = "missing_psmiles_or_tg"

        # Keep an audit sample that is small enough for GitHub but informative.
        if idx < 200 or status == "supported":
            sample_rows.append(
                {
                    "row_index": idx,
                    "PSMILES": psmiles,
                    "normalized_PSMILES_for_current_gate": normalized,
                    "Exp_Tg_K": tg if tg is not None else "",
                    "source": source,
                    "polymer_class": polymer_class,
                    "reliability": reliability,
                    "current_pmsbp_density": pmsbp_value,
                    "representation_class": rep_class,
                    "support_status": status,
                    "support_error": error,
                }
            )

    total_for_support = supported + unsupported
    fraction = supported / total_for_support if total_for_support else 0.0

    if not has_psmiles or not has_tg:
        verdict = "OPEN_DATASET_FOUND_REQUIRED_COLUMNS_MISSING"
    elif fraction >= 0.50:
        verdict = "OPEN_DATASET_FOUND_PMSBP_REANALYSIS_READY"
    elif supported > 0:
        verdict = "OPEN_DATASET_FOUND_PMSBP_PROTOTYPE_COVERAGE_LOW"
    else:
        verdict = "OPEN_DATASET_FOUND_PMSBP_PARSER_NOT_READY"

    audit = PolyMetriXAudit(
        path=str(POLYMETRIX_RELATIVE_PATH),
        exists=True,
        n_rows=len(rows),
        has_psmiles=has_psmiles,
        has_tg=has_tg,
        n_nonempty_psmiles=nonempty,
        n_numeric_tg=numeric_tg,
        n_sources=len(sources),
        n_polymer_classes=len(classes),
        n_supported_by_current_pmsbp=supported,
        n_unsupported_by_current_pmsbp=unsupported,
        support_fraction=fraction,
        verdict=verdict,
    )
    return audit, sample_rows


def find_polyverse_tg_like_files(root: Path) -> list[dict[str, object]]:
    """Find Tg/glass-transition-looking files inside polyVERSE."""

    base = root / POLYVERSE_RELATIVE_DIR
    rows: list[dict[str, object]] = []
    if not base.exists():
        return rows

    patterns = ("tg", "glass", "transition")
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root))
        low = rel.lower()
        if any(k in low for k in patterns):
            rows.append(
                {
                    "path": rel,
                    "size_bytes": p.stat().st_size,
                    "extension": p.suffix.lower(),
                }
            )
    return rows


def write_step16_outputs(root: Path, output_dir: Path) -> str:
    """Run Step-16 audit and write outputs."""

    output_dir.mkdir(parents=True, exist_ok=True)

    presence = dataset_presence(root)
    poly_audit, support_rows = audit_polymetrix(root)
    polyverse_rows = find_polyverse_tg_like_files(root)

    with (output_dir / "open_dataset_presence.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["dataset", "path", "exists", "size_bytes", "status"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in presence:
            w.writerow(r.__dict__)

    with (output_dir / "polymetrix_row_level_audit.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(poly_audit.__dict__.keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerow(poly_audit.__dict__)

    with (output_dir / "polymetrix_current_pmsbp_support_sample.csv").open("w", newline="", encoding="utf-8") as f:
        if support_rows:
            fieldnames = list(support_rows[0].keys())
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(support_rows)

    with (output_dir / "polyverse_tg_like_files.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["path", "size_bytes", "extension"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(polyverse_rows)

    # Overall verdict.
    if poly_audit.verdict == "OPEN_DATASET_FOUND_PMSBP_REANALYSIS_READY":
        final = "STEP16_OPEN_DATA_READY_FOR_PMSBP_REANALYSIS"
    elif poly_audit.exists and poly_audit.has_psmiles and poly_audit.has_tg:
        final = "STEP16_OPEN_ROW_LEVEL_DATA_FOUND_PMSBP_PARSER_MUST_BE_EXTENDED"
    else:
        final = "STEP16_OPEN_ROW_LEVEL_DATA_NOT_READY"

    report = [
        "# Step 16 — Open Row-Level Dataset Strategy Gate",
        "",
        f"Final verdict: `{final}`",
        "",
        "## PolyMetriX audit",
        "",
        f"- File exists: {poly_audit.exists}",
        f"- Rows: {poly_audit.n_rows}",
        f"- Has PSMILES column: {poly_audit.has_psmiles}",
        f"- Has experimental Tg column: {poly_audit.has_tg}",
        f"- Nonempty PSMILES rows: {poly_audit.n_nonempty_psmiles}",
        f"- Numeric Tg rows: {poly_audit.n_numeric_tg}",
        f"- Source count: {poly_audit.n_sources}",
        f"- Polymer class count: {poly_audit.n_polymer_classes}",
        f"- Rows supported by current Step-14 pMSBP parser: {poly_audit.n_supported_by_current_pmsbp}",
        f"- Rows unsupported by current Step-14 pMSBP parser: {poly_audit.n_unsupported_by_current_pmsbp}",
        f"- Support fraction: {poly_audit.support_fraction:.6f}",
        f"- PolyMetriX verdict: `{poly_audit.verdict}`",
        "",
        "## Interpretation",
        "",
    ]

    if final == "STEP16_OPEN_DATA_READY_FOR_PMSBP_REANALYSIS":
        report.append("The open row-level dataset is present and the current pMSBP parser has sufficient coverage to start re-analysis.")
    elif final == "STEP16_OPEN_ROW_LEVEL_DATA_FOUND_PMSBP_PARSER_MUST_BE_EXTENDED":
        report.extend(
            [
                "A real open row-level Tg dataset is present. This resolves the dataset-strategy direction.",
                "",
                "However, the current pMSBP parser is still a prototype. It was designed for simple two-terminal gate strings, not complex PSMILES/BigSMILES. The next step is therefore not journal writing; it is parser extension and feature extraction.",
            ]
        )
    else:
        report.append("The open row-level data strategy is not ready. Download or column structure must be fixed first.")

    report.extend(
        [
            "",
            "## Next required step",
            "",
            "Step 17 should implement a PSMILES-aware pMSBP parser or a conservative conversion layer for the PolyMetriX PSMILES column. Only after row coverage is high enough should source-level statistics be recomputed.",
        ]
    )

    (output_dir / "STEP16_OPEN_ROW_LEVEL_DATASET_GATE_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return final
