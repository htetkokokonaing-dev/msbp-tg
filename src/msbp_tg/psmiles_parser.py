"""PSMILES-aware pMSBP parser extension gate.

Step 17 extends the descriptor pipeline from simple gate strings such as
``*CC*`` toward PolyMetriX-style PSMILES strings such as ``[*]CC[*]`` and more
complex bracketed/branched repeat-unit strings.

This is still a conservative parser-extension gate, not a final polymer graph
canonicalizer.  It produces an auditable token-sequence pMSBP coordinate and a
coverage taxonomy so the project can decide whether full open-data re-analysis
is now possible.

Scientific caution
------------------
The parser below is a PSMILES token-sequence quotient.  It supports the
open-row-level rebuild path and gives reproducible feature coverage, but it
does not yet prove full chemical equivalence for all BigSMILES/PSMILES forms,
stereochemistry, tacticity, branching semantics, or polymer graph quotienting.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import re
import statistics


POLYMETRIX_PATH = Path("data/open_row_level/LAMALAB_CURATED_Tg_structured_polymerclass.csv")

PSMILES_COL = "PSMILES"
TG_COL = "labels.Exp_Tg(K)"
SOURCE_COL = "meta.source"
CLASS_COL = "meta.polymer_class"
RELIABILITY_COL = "meta.reliability"

_ATOM_TOKEN_RE = re.compile(r"Cl|Br|Si|[BCNOFPSIbcnops]")
_BRACKET_ATOM_RE = re.compile(r"\[([A-Z][a-z]?|[bcnops])([^\]]*)\]")


@dataclass(frozen=True)
class PSMILESParseResult:
    psmiles: str
    normalized_psmiles: str
    atom_tokens: tuple[str, ...]
    primitive_period_tokens: tuple[str, ...]
    canonical_period_tokens: tuple[str, ...]
    representation_class: str
    pmsbp_density: float
    parser_mode: str
    status: str
    reason: str


def _normalize_atom_token(token: str) -> str:
    if token in {"c", "C"}:
        return "C"
    if token in {"n", "N"}:
        return "N"
    if token in {"o", "O"}:
        return "O"
    if token in {"s", "S"}:
        return "S"
    if token in {"p", "P"}:
        return "P"
    if token in {"b", "B"}:
        return "B"
    return token


def normalize_psmiles(psmiles: str) -> str:
    """Normalize common PSMILES spelling without claiming full canonicalization."""

    s = str(psmiles).strip()
    s = re.sub(r"\s+", "", s)

    # Dummy attachment atoms: [*], [*:1], [*:2], etc.
    s = re.sub(r"\[\*[^]]*\]", "*", s)

    # Normalize bracketed simple atoms: [SiH2] -> Si, [C@@H] -> C, [nH] -> N.
    def repl(match: re.Match[str]) -> str:
        atom = match.group(1)
        return _normalize_atom_token(atom)

    s = _BRACKET_ATOM_RE.sub(repl, s)
    return s


def atom_tokens_from_psmiles(psmiles: str) -> tuple[str, ...]:
    """Extract conservative atom tokens from normalized PSMILES."""

    s = normalize_psmiles(psmiles)
    # Remove dummy markers but keep atom order for the token-sequence quotient.
    s = s.replace("*", "")
    tokens = tuple(_normalize_atom_token(t) for t in _ATOM_TOKEN_RE.findall(s))
    return tokens


def _shortest_repeating_period(tokens: tuple[str, ...]) -> tuple[str, ...]:
    n = len(tokens)
    if n == 0:
        return tuple()
    for k in range(1, n + 1):
        if n % k != 0:
            continue
        unit = tokens[:k]
        if unit * (n // k) == tokens:
            # Preserve Step-13 carbon-chain gate.
            if unit == ("C",) and n >= 2:
                return ("C", "C")
            return unit
    return tokens


def _rotations(tokens: tuple[str, ...]) -> list[tuple[str, ...]]:
    return [tokens[i:] + tokens[:i] for i in range(len(tokens))]


def _canonical_necklace(tokens: tuple[str, ...]) -> tuple[str, ...]:
    if not tokens:
        return tuple()
    candidates = _rotations(tokens) + _rotations(tuple(reversed(tokens)))
    return min(candidates, key=lambda xs: "|".join(xs))


def parse_psmiles_to_pmsbp(psmiles: str) -> PSMILESParseResult:
    """Parse one PSMILES string into a prototype pMSBP coordinate."""

    original = str(psmiles)
    normalized = normalize_psmiles(original)

    dummy_count = normalized.count("*")
    if dummy_count < 2:
        return PSMILESParseResult(
            psmiles=original,
            normalized_psmiles=normalized,
            atom_tokens=tuple(),
            primitive_period_tokens=tuple(),
            canonical_period_tokens=tuple(),
            representation_class="",
            pmsbp_density=math.nan,
            parser_mode="psmiles_token_sequence",
            status="unsupported",
            reason="fewer_than_two_attachment_markers",
        )

    tokens = atom_tokens_from_psmiles(normalized)
    if not tokens:
        return PSMILESParseResult(
            psmiles=original,
            normalized_psmiles=normalized,
            atom_tokens=tuple(),
            primitive_period_tokens=tuple(),
            canonical_period_tokens=tuple(),
            representation_class="",
            pmsbp_density=math.nan,
            parser_mode="psmiles_token_sequence",
            status="unsupported",
            reason="no_supported_atom_tokens",
        )

    period = _shortest_repeating_period(tokens)
    canonical = _canonical_necklace(period)

    period_heavy = len(canonical)
    if period_heavy == 0:
        density = math.nan
    else:
        periodic_rot = max(period_heavy - 1, 1)
        density = -periodic_rot / period_heavy

    rep = "*{}*".format("".join(canonical))
    return PSMILESParseResult(
        psmiles=original,
        normalized_psmiles=normalized,
        atom_tokens=tokens,
        primitive_period_tokens=period,
        canonical_period_tokens=canonical,
        representation_class=rep,
        pmsbp_density=density,
        parser_mode="psmiles_token_sequence",
        status="supported",
        reason="supported_token_sequence_periodic_quotient",
    )


def _read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except UnicodeDecodeError:
        with path.open("r", newline="", encoding="latin-1") as f:
            return list(csv.DictReader(f))


def _float_or_none(value: object) -> float | None:
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
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = avg
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
    return _pearson(_rank(xs), _rank(ys))


def _safe_float_text(x: float | None) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return ""
    return f"{x:.12g}"


def audit_polymetrix_psmiles(root: Path) -> dict[str, object]:
    """Audit PolyMetriX pMSBP parser coverage and preliminary association."""

    path = root / POLYMETRIX_PATH
    if not path.exists():
        return {
            "verdict": "STEP17_POLYMETRIX_DATA_MISSING",
            "summary": {
                "path": str(POLYMETRIX_PATH),
                "exists": False,
                "n_rows": 0,
                "n_supported": 0,
                "n_unsupported": 0,
                "support_fraction": 0.0,
                "spearman_rho_supported_all": "",
                "n_supported_numeric_tg": 0,
            },
            "sample_rows": [],
            "taxonomy_rows": [],
            "class_summary_rows": [],
        }

    rows = _read_csv_dicts(path)
    if not rows:
        return {
            "verdict": "STEP17_POLYMETRIX_EMPTY",
            "summary": {
                "path": str(POLYMETRIX_PATH),
                "exists": True,
                "n_rows": 0,
                "n_supported": 0,
                "n_unsupported": 0,
                "support_fraction": 0.0,
                "spearman_rho_supported_all": "",
                "n_supported_numeric_tg": 0,
            },
            "sample_rows": [],
            "taxonomy_rows": [],
            "class_summary_rows": [],
        }

    fieldnames = set(rows[0].keys())
    required_missing = [c for c in [PSMILES_COL, TG_COL] if c not in fieldnames]
    if required_missing:
        return {
            "verdict": "STEP17_REQUIRED_COLUMNS_MISSING",
            "summary": {
                "path": str(POLYMETRIX_PATH),
                "exists": True,
                "n_rows": len(rows),
                "missing_columns": ";".join(required_missing),
                "n_supported": 0,
                "n_unsupported": len(rows),
                "support_fraction": 0.0,
                "spearman_rho_supported_all": "",
                "n_supported_numeric_tg": 0,
            },
            "sample_rows": [],
            "taxonomy_rows": [],
            "class_summary_rows": [],
        }

    sample_rows: list[dict[str, object]] = []
    reason_counts: dict[str, int] = {}
    class_counts: dict[str, dict[str, object]] = {}
    xs: list[float] = []
    ys: list[float] = []

    supported = 0
    unsupported = 0

    for idx, row in enumerate(rows):
        psmiles = row.get(PSMILES_COL, "")
        tg = _float_or_none(row.get(TG_COL))
        source = row.get(SOURCE_COL, "")
        polymer_class = row.get(CLASS_COL, "")
        reliability = row.get(RELIABILITY_COL, "")

        parsed = parse_psmiles_to_pmsbp(psmiles)
        is_supported = parsed.status == "supported" and not math.isnan(parsed.pmsbp_density)

        if is_supported:
            supported += 1
            if tg is not None:
                xs.append(parsed.pmsbp_density)
                ys.append(tg)
        else:
            unsupported += 1

        reason_counts[parsed.reason] = reason_counts.get(parsed.reason, 0) + 1

        key = polymer_class or "unknown_class"
        if key not in class_counts:
            class_counts[key] = {
                "polymer_class": key,
                "n_rows": 0,
                "n_supported": 0,
                "n_numeric_tg_supported": 0,
                "xs": [],
                "ys": [],
            }
        class_counts[key]["n_rows"] += 1
        if is_supported:
            class_counts[key]["n_supported"] += 1
            if tg is not None:
                class_counts[key]["n_numeric_tg_supported"] += 1
                class_counts[key]["xs"].append(parsed.pmsbp_density)
                class_counts[key]["ys"].append(tg)

        if idx < 500:
            sample_rows.append(
                {
                    "row_index": idx,
                    "PSMILES": psmiles,
                    "normalized_PSMILES": parsed.normalized_psmiles,
                    "Exp_Tg_K": "" if tg is None else tg,
                    "source": source,
                    "polymer_class": polymer_class,
                    "reliability": reliability,
                    "atom_token_count": len(parsed.atom_tokens),
                    "primitive_period": "".join(parsed.primitive_period_tokens),
                    "canonical_period": "".join(parsed.canonical_period_tokens),
                    "representation_class": parsed.representation_class,
                    "pmsbp_density": "" if math.isnan(parsed.pmsbp_density) else parsed.pmsbp_density,
                    "parser_status": parsed.status,
                    "parser_reason": parsed.reason,
                }
            )

    n = supported + unsupported
    support_fraction = supported / n if n else 0.0
    rho = spearman(xs, ys)

    taxonomy_rows = [
        {"reason": reason, "count": count, "fraction": count / n if n else 0.0}
        for reason, count in sorted(reason_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]

    class_summary_rows: list[dict[str, object]] = []
    for item in class_counts.values():
        cx = item.pop("xs")
        cy = item.pop("ys")
        crho = spearman(cx, cy)
        item["support_fraction"] = item["n_supported"] / item["n_rows"] if item["n_rows"] else 0.0
        item["spearman_rho_supported"] = "" if crho is None else crho
        class_summary_rows.append(item)
    class_summary_rows.sort(key=lambda r: (-int(r["n_rows"]), str(r["polymer_class"])))

    if support_fraction >= 0.80:
        verdict = "STEP17_PSMILES_PARSER_EXTENDED_COVERAGE_PASS"
    elif support_fraction >= 0.30:
        verdict = "STEP17_PSMILES_PARSER_EXTENDED_BUT_COVERAGE_LIMITED"
    elif supported > 0:
        verdict = "STEP17_PSMILES_PARSER_LOW_COVERAGE"
    else:
        verdict = "STEP17_PSMILES_PARSER_NO_COVERAGE"

    summary = {
        "path": str(POLYMETRIX_PATH),
        "exists": True,
        "n_rows": len(rows),
        "n_supported": supported,
        "n_unsupported": unsupported,
        "support_fraction": support_fraction,
        "n_supported_numeric_tg": len(xs),
        "spearman_rho_supported_all": "" if rho is None else rho,
        "parser_mode": "psmiles_token_sequence",
    }

    return {
        "verdict": verdict,
        "summary": summary,
        "sample_rows": sample_rows,
        "taxonomy_rows": taxonomy_rows,
        "class_summary_rows": class_summary_rows,
    }


def write_step17_outputs(root: Path, output_dir: Path) -> str:
    """Run Step 17 and write output artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    result = audit_polymetrix_psmiles(root)
    verdict = str(result["verdict"])
    summary = dict(result["summary"])

    with (output_dir / "polymetrix_psmiles_parser_coverage_summary.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(summary.keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerow(summary)

    with (output_dir / "psmiles_unsupported_reason_taxonomy.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["reason", "count", "fraction"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(result["taxonomy_rows"])

    with (output_dir / "polymetrix_pmsbp_supported_sample.csv").open("w", newline="", encoding="utf-8") as f:
        rows = result["sample_rows"]
        if rows:
            fieldnames = list(rows[0].keys())
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

    with (output_dir / "polymetrix_class_level_pmsbp_preliminary_summary.csv").open("w", newline="", encoding="utf-8") as f:
        rows = result["class_summary_rows"]
        fieldnames = [
            "polymer_class",
            "n_rows",
            "n_supported",
            "n_numeric_tg_supported",
            "support_fraction",
            "spearman_rho_supported",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})

    report = [
        "# Step 17 — PSMILES-aware pMSBP Parser Extension Gate",
        "",
        f"Verdict: `{verdict}`",
        "",
        "## Summary",
        "",
        f"- Rows: {summary.get('n_rows', 0)}",
        f"- Supported rows: {summary.get('n_supported', 0)}",
        f"- Unsupported rows: {summary.get('n_unsupported', 0)}",
        f"- Support fraction: {float(summary.get('support_fraction', 0.0)):.6f}",
        f"- Supported numeric Tg rows: {summary.get('n_supported_numeric_tg', 0)}",
        f"- Preliminary all-supported Spearman rho: {summary.get('spearman_rho_supported_all', '')}",
        "",
        "## Interpretation",
        "",
    ]

    if verdict == "STEP17_PSMILES_PARSER_EXTENDED_COVERAGE_PASS":
        report.extend(
            [
                "The parser-extension gate has enough coverage to move to Step 18: open-data pMSBP re-analysis with proper grouping, cluster-aware uncertainty, and source/class stratification.",
                "",
                "This is not yet a journal result. The current coordinate is a reproducible PSMILES token-sequence quotient, not a final validated polymer graph quotient.",
            ]
        )
    elif verdict == "STEP17_PSMILES_PARSER_EXTENDED_BUT_COVERAGE_LIMITED":
        report.extend(
            [
                "The parser extension works but coverage is limited. Step 18 should either restrict analysis to the supported subset or extend the parser further before statistical claims.",
            ]
        )
    else:
        report.extend(
            [
                "The parser extension does not yet provide enough coverage for re-analysis. More PSMILES/BigSMILES parsing work is required.",
            ]
        )

    report.extend(
        [
            "",
            "## Next required step",
            "",
            "Step 18 should compute open-data pMSBP statistics on supported PolyMetriX rows, including class/source stratification, within-class residualization, and cluster-aware uncertainty. No journal claim should be made from the preliminary Spearman value alone.",
        ]
    )

    (output_dir / "STEP17_PSMILES_PARSER_EXTENSION_GATE_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return verdict
