"""pMSBP re-feature and re-analysis audit utilities.

Step 15 is deliberately an audit gate, not a new journal claim.  It checks
whether the existing public repository contains row-level, public-safe inputs
that can be re-featured with the Step-14 periodic MSBP coordinate.

The intended outcomes are:

- PASS_WITH_ROW_LEVEL_REANALYSIS:
    row-level SMILES/Tg data are present and pMSBP source summaries are
    computed.

- PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS:
    no public-safe row-level SMILES/Tg table is present.  This is not a code
    failure; it means the current repository can archive descriptors and
    aggregate outputs, but cannot yet regenerate the scientific results from
    row-level evidence.

The module avoids overclaiming.  It never fabricates row-level data from
aggregate CSV files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import csv
import math
import statistics

from .periodic_fiber import periodic_msbp


SMILES_CANDIDATES = [
    "smiles",
    "SMILES",
    "polymer_smiles",
    "Polymer_SMILES",
    "repeat_unit_smiles",
    "repeat_smiles",
    "canonical_smiles",
    "structure",
]

TG_CANDIDATES = [
    "Tg",
    "tg",
    "Tg_C",
    "Tg_degC",
    "Tg_Celsius",
    "glass_transition_temperature",
    "target",
    "y",
]

SOURCE_CANDIDATES = [
    "source",
    "dataset",
    "source_name",
    "Source",
    "dataset_name",
]

FIBER_CANDIDATES = [
    "visible_fiber",
    "fiber",
    "family",
    "source_family",
    "class",
    "group",
]


@dataclass(frozen=True)
class CandidateTable:
    path: str
    n_rows: int
    smiles_col: str | None
    tg_col: str | None
    source_col: str | None
    fiber_col: str | None
    is_row_level_candidate: bool


@dataclass(frozen=True)
class RefeatureSummary:
    table_path: str
    source_name: str
    n_rows: int
    n_supported_pmsbp: int
    n_unsupported_pmsbp: int
    n_fibers: int
    spearman_rho: float | None
    sign_accuracy: float | None
    status: str


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except UnicodeDecodeError:
        with path.open("r", newline="", encoding="latin-1") as f:
            return list(csv.DictReader(f))


def _first_present(fieldnames: Iterable[str], candidates: list[str]) -> str | None:
    fields = list(fieldnames)
    lower_map = {f.lower(): f for f in fields}
    for c in candidates:
        if c in fields:
            return c
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    return None


def discover_candidate_tables(root: Path) -> list[CandidateTable]:
    """Find CSV tables and classify whether they look row-level re-featureable."""

    candidates: list[CandidateTable] = []
    for path in sorted(root.rglob("*.csv")):
        if ".git" in path.parts:
            continue
        try:
            rows = _read_csv_rows(path)
        except Exception:
            continue

        fieldnames = rows[0].keys() if rows else []
        smiles_col = _first_present(fieldnames, SMILES_CANDIDATES)
        tg_col = _first_present(fieldnames, TG_CANDIDATES)
        source_col = _first_present(fieldnames, SOURCE_CANDIDATES)
        fiber_col = _first_present(fieldnames, FIBER_CANDIDATES)
        is_candidate = smiles_col is not None and tg_col is not None and len(rows) > 0

        candidates.append(
            CandidateTable(
                path=str(path.relative_to(root)),
                n_rows=len(rows),
                smiles_col=smiles_col,
                tg_col=tg_col,
                source_col=source_col,
                fiber_col=fiber_col,
                is_row_level_candidate=is_candidate,
            )
        )

    return candidates


def _to_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        x = float(str(value).strip())
    except Exception:
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x


def _rank(values: list[float]) -> list[float]:
    """Average ranks, 1-based."""

    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j
    return ranks


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def spearman(xs: list[float], ys: list[float]) -> float | None:
    """Spearman rho without external dependencies."""

    return _pearson(_rank(xs), _rank(ys))


def _sign_accuracy(xs: list[float], ys: list[float]) -> float | None:
    """Direction agreement after median centering.

    Because pMSBP is negative mobility, an upward Tg boundary displacement is
    expected when pMSBP is more negative only if the model states so.  To avoid
    baking in a journal claim at audit stage, this simply reports the dominant
    monotone sign agreement against the observed Spearman sign.
    """

    rho = spearman(xs, ys)
    if rho is None:
        return None
    med_x = statistics.median(xs)
    med_y = statistics.median(ys)
    valid = [(x - med_x, y - med_y) for x, y in zip(xs, ys) if x != med_x and y != med_y]
    if not valid:
        return None
    sgn = 1 if rho >= 0 else -1
    hits = sum(1 for dx, dy in valid if sgn * dx * dy > 0)
    return hits / len(valid)


def refeature_candidate_table(root: Path, table: CandidateTable) -> tuple[RefeatureSummary, list[dict[str, object]]]:
    """Apply pMSBP to one row-level candidate table."""

    if not table.is_row_level_candidate or table.smiles_col is None or table.tg_col is None:
        raise ValueError("not a row-level candidate table")

    path = root / table.path
    rows = _read_csv_rows(path)

    out_rows: list[dict[str, object]] = []
    xs: list[float] = []
    ys: list[float] = []
    fibers: set[str] = set()
    unsupported = 0

    for i, row in enumerate(rows):
        smiles = str(row.get(table.smiles_col, "")).strip()
        tg = _to_float(row.get(table.tg_col))
        source = str(row.get(table.source_col, "unknown_source")) if table.source_col else "unknown_source"
        fiber = str(row.get(table.fiber_col, "unknown_fiber")) if table.fiber_col else "unknown_fiber"

        p_value = None
        rep_class = ""
        status = "unsupported"
        try:
            r = periodic_msbp(smiles)
            p_value = r.periodic_msbp_density
            rep_class = r.representation_class
            status = "supported"
        except Exception as exc:
            unsupported += 1
            status = f"unsupported:{type(exc).__name__}"

        if p_value is not None and tg is not None:
            xs.append(float(p_value))
            ys.append(float(tg))
            fibers.add(fiber)

        out_rows.append(
            {
                "table_path": table.path,
                "row_index": i,
                "source": source,
                "fiber": fiber,
                "smiles": smiles,
                "tg": tg if tg is not None else "",
                "pmsbp_density": p_value if p_value is not None else "",
                "representation_class": rep_class,
                "status": status,
            }
        )

    supported = len([r for r in out_rows if r["pmsbp_density"] != ""])
    rho = spearman(xs, ys)
    acc = _sign_accuracy(xs, ys)

    summary = RefeatureSummary(
        table_path=table.path,
        source_name="mixed_or_unknown",
        n_rows=len(rows),
        n_supported_pmsbp=supported,
        n_unsupported_pmsbp=unsupported,
        n_fibers=len(fibers),
        spearman_rho=rho,
        sign_accuracy=acc,
        status="REFEATURED_PUBLIC_ROW_LEVEL_TABLE",
    )
    return summary, out_rows


def run_reanalysis_audit(root: Path) -> dict[str, object]:
    """Run the Step-15 audit and return a structured result."""

    candidates = discover_candidate_tables(root)
    row_level = [c for c in candidates if c.is_row_level_candidate]

    refeature_summaries: list[RefeatureSummary] = []
    refeature_rows: list[dict[str, object]] = []

    for table in row_level:
        try:
            summary, rows = refeature_candidate_table(root, table)
        except Exception:
            continue
        refeature_summaries.append(summary)
        refeature_rows.extend(rows)

    if refeature_summaries:
        verdict = "PASS_WITH_ROW_LEVEL_REANALYSIS"
    else:
        verdict = "PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS"

    return {
        "verdict": verdict,
        "candidate_tables": candidates,
        "row_level_candidate_count": len(row_level),
        "refeature_summaries": refeature_summaries,
        "refeature_rows": refeature_rows,
    }


def write_step15_outputs(root: Path, output_dir: Path) -> str:
    """Write Step-15 audit outputs and return the verdict."""

    output_dir.mkdir(parents=True, exist_ok=True)
    result = run_reanalysis_audit(root)

    # Candidate table audit
    with (output_dir / "pmsbp_candidate_table_audit.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "path",
            "n_rows",
            "smiles_col",
            "tg_col",
            "source_col",
            "fiber_col",
            "is_row_level_candidate",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in result["candidate_tables"]:
            writer.writerow(t.__dict__)

    # Summary
    with (output_dir / "pmsbp_refeature_summary.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "table_path",
            "source_name",
            "n_rows",
            "n_supported_pmsbp",
            "n_unsupported_pmsbp",
            "n_fibers",
            "spearman_rho",
            "sign_accuracy",
            "status",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in result["refeature_summaries"]:
            writer.writerow(s.__dict__)

    # Row-level pMSBP table only if public row-level candidates exist.
    if result["refeature_rows"]:
        with (output_dir / "pmsbp_refeature_rows_public_safe.csv").open("w", newline="", encoding="utf-8") as f:
            fieldnames = list(result["refeature_rows"][0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result["refeature_rows"])

    verdict = str(result["verdict"])
    report = [
        "# Step 15 pMSBP Re-feature / Re-analysis Audit",
        "",
        f"Verdict: `{verdict}`",
        "",
        f"CSV tables scanned: {len(result['candidate_tables'])}",
        f"Row-level candidate tables found: {result['row_level_candidate_count']}",
        f"Re-feature summary tables produced: {len(result['refeature_summaries'])}",
        "",
    ]
    if verdict == "PASS_AUDIT_ONLY_NO_ROW_LEVEL_REANALYSIS":
        report.extend(
            [
                "Interpretation:",
                "",
                "The repository does not currently expose a public-safe row-level table containing both SMILES/repeat-unit strings and Tg values. The pMSBP descriptor can be validated on representation gates, but the scientific result cannot yet be regenerated from public row-level evidence.",
                "",
                "Journal implication:",
                "",
                "Do not claim full Journal of Cheminformatics reproducibility until compatible row-level inputs or a complete open-data reconstruction are available.",
            ]
        )
    else:
        report.extend(
            [
                "Interpretation:",
                "",
                "At least one row-level public-safe candidate table was found and re-featured with pMSBP. These outputs are audit-level summaries only; cluster-aware inference and source-specific scientific interpretation are still required before a new manuscript claim.",
            ]
        )

    (output_dir / "STEP15_PMSBP_REANALYSIS_AUDIT_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return verdict
