"""Step 18 open-data pMSBP statistical re-analysis.

This module runs the first real Option-C statistical re-analysis on the open
row-level PolyMetriX Tg dataset after Step 17 achieved full PSMILES parser
coverage.

The analysis is intentionally conservative:

- it uses only open row-level rows available in PolyMetriX;
- it reports overall association separately from within-class residual
  association;
- it includes row bootstrap, class-cluster bootstrap, within-class permutation,
  and leave-one-class-out sensitivity;
- it emits a go/no-go audit verdict rather than a journal claim.

No pandas/scipy dependency is required.  This keeps Termux execution practical.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import random
import statistics
from collections import defaultdict

from .psmiles_parser import parse_psmiles_to_pmsbp


POLYMETRIX_PATH = Path("data/open_row_level/LAMALAB_CURATED_Tg_structured_polymerclass.csv")
PSMILES_COL = "PSMILES"
TG_COL = "labels.Exp_Tg(K)"
SOURCE_COL = "meta.source"
CLASS_COL = "meta.polymer_class"
RELIABILITY_COL = "meta.reliability"


@dataclass(frozen=True)
class ReanalysisRow:
    row_index: int
    psmiles: str
    exp_tg_k: float
    pmsbp_density: float
    representation_class: str
    polymer_class: str
    source: str
    reliability: str


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


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    return pearson(_rank(xs), _rank(ys))


def _median(values: list[float]) -> float:
    return statistics.median(values)


def _mean(values: list[float]) -> float:
    return statistics.fmean(values)


def _quantile(sorted_values: list[float], q: float) -> float | None:
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return sorted_values[lo]
    w = pos - lo
    return sorted_values[lo] * (1 - w) + sorted_values[hi] * w


def _ci(values: list[float], low: float = 0.025, high: float = 0.975) -> tuple[float | None, float | None]:
    vals = sorted(v for v in values if v is not None and not math.isnan(v))
    return _quantile(vals, low), _quantile(vals, high)


def load_polymetrix_supported_rows(root: Path) -> list[ReanalysisRow]:
    """Load PolyMetriX rows supported by Step-17 pMSBP parser."""

    path = root / POLYMETRIX_PATH
    if not path.exists():
        raise FileNotFoundError(str(path))

    raw_rows = _read_csv_dicts(path)
    out: list[ReanalysisRow] = []

    for idx, row in enumerate(raw_rows):
        psmiles = row.get(PSMILES_COL, "")
        tg = _float_or_none(row.get(TG_COL))
        if tg is None:
            continue

        parsed = parse_psmiles_to_pmsbp(psmiles)
        if parsed.status != "supported" or math.isnan(parsed.pmsbp_density):
            continue

        out.append(
            ReanalysisRow(
                row_index=idx,
                psmiles=psmiles,
                exp_tg_k=tg,
                pmsbp_density=float(parsed.pmsbp_density),
                representation_class=parsed.representation_class,
                polymer_class=row.get(CLASS_COL, "") or "unknown_class",
                source=row.get(SOURCE_COL, "") or "unknown_source",
                reliability=row.get(RELIABILITY_COL, "") or "unknown_reliability",
            )
        )

    return out


def _xy(rows: list[ReanalysisRow]) -> tuple[list[float], list[float]]:
    return [r.pmsbp_density for r in rows], [r.exp_tg_k for r in rows]


def center_within_group(rows: list[ReanalysisRow], group_attr: str = "polymer_class", center: str = "median") -> tuple[list[float], list[float]]:
    """Return within-group residual x/y arrays."""

    groups: dict[str, list[ReanalysisRow]] = defaultdict(list)
    for r in rows:
        groups[str(getattr(r, group_attr))].append(r)

    xs_res: list[float] = []
    ys_res: list[float] = []

    center_fn = _median if center == "median" else _mean

    for group_rows in groups.values():
        xs, ys = _xy(group_rows)
        cx = center_fn(xs)
        cy = center_fn(ys)
        for x, y in zip(xs, ys):
            xs_res.append(x - cx)
            ys_res.append(y - cy)

    return xs_res, ys_res


def overall_summary(rows: list[ReanalysisRow]) -> dict[str, object]:
    xs, ys = _xy(rows)
    xres, yres = center_within_group(rows, "polymer_class", "median")
    xres_mean, yres_mean = center_within_group(rows, "polymer_class", "mean")

    classes = {r.polymer_class for r in rows}
    sources = {r.source for r in rows}
    reps = {r.representation_class for r in rows}

    return {
        "n_rows": len(rows),
        "n_polymer_classes": len(classes),
        "n_sources": len(sources),
        "n_representation_classes": len(reps),
        "overall_spearman_rho": spearman(xs, ys),
        "within_class_median_residual_spearman_rho": spearman(xres, yres),
        "within_class_mean_residual_spearman_rho": spearman(xres_mean, yres_mean),
        "pmsbp_min": min(xs) if xs else "",
        "pmsbp_max": max(xs) if xs else "",
        "tg_k_min": min(ys) if ys else "",
        "tg_k_max": max(ys) if ys else "",
    }


def group_summary(rows: list[ReanalysisRow], group_attr: str) -> list[dict[str, object]]:
    groups: dict[str, list[ReanalysisRow]] = defaultdict(list)
    for r in rows:
        groups[str(getattr(r, group_attr))].append(r)

    out: list[dict[str, object]] = []
    for name, gr in groups.items():
        xs, ys = _xy(gr)
        out.append(
            {
                group_attr: name,
                "n_rows": len(gr),
                "n_representation_classes": len({r.representation_class for r in gr}),
                "spearman_rho": spearman(xs, ys),
                "pmsbp_min": min(xs) if xs else "",
                "pmsbp_max": max(xs) if xs else "",
                "tg_k_median": statistics.median(ys) if ys else "",
            }
        )

    out.sort(key=lambda row: (-int(row["n_rows"]), str(row[group_attr])))
    return out


def bootstrap_row_ci(rows: list[ReanalysisRow], n_bootstrap: int, seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    n = len(rows)
    raw_vals: list[float] = []
    residual_vals: list[float] = []

    for _ in range(n_bootstrap):
        sample = [rows[rng.randrange(n)] for _ in range(n)]
        xs, ys = _xy(sample)
        rho = spearman(xs, ys)
        if rho is not None:
            raw_vals.append(rho)

        xres, yres = center_within_group(sample, "polymer_class", "median")
        rrho = spearman(xres, yres)
        if rrho is not None:
            residual_vals.append(rrho)

    raw_lo, raw_hi = _ci(raw_vals)
    res_lo, res_hi = _ci(residual_vals)
    return {
        "bootstrap_type": "row_bootstrap",
        "n_bootstrap": n_bootstrap,
        "overall_rho_ci_low": raw_lo,
        "overall_rho_ci_high": raw_hi,
        "within_class_residual_rho_ci_low": res_lo,
        "within_class_residual_rho_ci_high": res_hi,
    }


def bootstrap_class_cluster_ci(rows: list[ReanalysisRow], n_bootstrap: int, seed: int) -> dict[str, object]:
    """Bootstrap polymer classes as clusters."""

    rng = random.Random(seed)
    groups: dict[str, list[ReanalysisRow]] = defaultdict(list)
    for r in rows:
        groups[r.polymer_class].append(r)

    class_names = list(groups.keys())
    k = len(class_names)
    raw_vals: list[float] = []
    residual_vals: list[float] = []

    for _ in range(n_bootstrap):
        sampled_classes = [class_names[rng.randrange(k)] for _ in range(k)]
        sample: list[ReanalysisRow] = []
        for cname in sampled_classes:
            sample.extend(groups[cname])

        xs, ys = _xy(sample)
        rho = spearman(xs, ys)
        if rho is not None:
            raw_vals.append(rho)

        xres, yres = center_within_group(sample, "polymer_class", "median")
        rrho = spearman(xres, yres)
        if rrho is not None:
            residual_vals.append(rrho)

    raw_lo, raw_hi = _ci(raw_vals)
    res_lo, res_hi = _ci(residual_vals)
    return {
        "bootstrap_type": "polymer_class_cluster_bootstrap",
        "n_bootstrap": n_bootstrap,
        "overall_rho_ci_low": raw_lo,
        "overall_rho_ci_high": raw_hi,
        "within_class_residual_rho_ci_low": res_lo,
        "within_class_residual_rho_ci_high": res_hi,
    }


def within_class_permutation(rows: list[ReanalysisRow], n_permutation: int, seed: int) -> dict[str, object]:
    """Within-class permutation test for residual Spearman magnitude."""

    rng = random.Random(seed)
    observed_x, observed_y = center_within_group(rows, "polymer_class", "median")
    observed = spearman(observed_x, observed_y)

    groups: dict[str, list[ReanalysisRow]] = defaultdict(list)
    for r in rows:
        groups[r.polymer_class].append(r)

    exceed = 0
    perm_values: list[float] = []

    for _ in range(n_permutation):
        px: list[float] = []
        py: list[float] = []

        for gr in groups.values():
            xs, ys = _xy(gr)
            # Keep pMSBP fixed and shuffle Tg within class.
            yperm = ys[:]
            rng.shuffle(yperm)
            cx = statistics.median(xs)
            cy = statistics.median(yperm)
            px.extend([x - cx for x in xs])
            py.extend([y - cy for y in yperm])

        val = spearman(px, py)
        if val is None:
            continue
        perm_values.append(val)
        if observed is not None and abs(val) >= abs(observed):
            exceed += 1

    p_value = (exceed + 1) / (len(perm_values) + 1) if perm_values else ""
    return {
        "test": "within_class_tg_permutation",
        "n_permutation": n_permutation,
        "observed_within_class_residual_rho": observed,
        "two_sided_empirical_p": p_value,
    }


def leave_one_class_out(rows: list[ReanalysisRow]) -> list[dict[str, object]]:
    classes = sorted({r.polymer_class for r in rows})
    out: list[dict[str, object]] = []
    for cname in classes:
        sample = [r for r in rows if r.polymer_class != cname]
        xs, ys = _xy(sample)
        xres, yres = center_within_group(sample, "polymer_class", "median")
        out.append(
            {
                "left_out_polymer_class": cname,
                "n_rows_remaining": len(sample),
                "overall_spearman_rho": spearman(xs, ys),
                "within_class_median_residual_spearman_rho": spearman(xres, yres),
            }
        )
    return out


def verdict_from_results(summary: dict[str, object], boot_cluster: dict[str, object], perm: dict[str, object]) -> str:
    """Return conservative go/no-go audit verdict."""

    n = int(summary.get("n_rows", 0))
    residual_rho = summary.get("within_class_median_residual_spearman_rho")
    cluster_low = boot_cluster.get("within_class_residual_rho_ci_low")
    cluster_high = boot_cluster.get("within_class_residual_rho_ci_high")
    p = perm.get("two_sided_empirical_p")

    if not isinstance(residual_rho, float) or n < 500:
        return "STEP18_NO_GO_INSUFFICIENT_ANALYSIS_SIGNAL"

    # Strongest state: residual effect direction is stable under class-cluster
    # bootstrap and permutation.
    if isinstance(cluster_low, float) and isinstance(cluster_high, float) and isinstance(p, float):
        if cluster_high < 0 and p <= 0.05:
            return "STEP18_GO_NEGATIVE_WITHIN_CLASS_SIGNAL_REANALYSIS_SUPPORTED"
        if cluster_low > 0 and p <= 0.05:
            return "STEP18_GO_POSITIVE_WITHIN_CLASS_SIGNAL_REANALYSIS_SUPPORTED"

    # Weaker but still useful: raw overall association exists but within-class
    # residual evidence is not stable.
    overall = summary.get("overall_spearman_rho")
    if isinstance(overall, float) and abs(overall) >= 0.25:
        return "STEP18_MIXED_RAW_SIGNAL_WITHIN_CLASS_NOT_LOCKED"

    return "STEP18_NO_GO_SIGNAL_NOT_STABLE"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_step18_outputs(root: Path, output_dir: Path, n_bootstrap: int = 200, n_permutation: int = 200, seed: int = 1729) -> str:
    """Run full Step 18 and write audit outputs."""

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = load_polymetrix_supported_rows(root)

    # Main pMSBP feature table.
    feature_rows = [
        {
            "row_index": r.row_index,
            "PSMILES": r.psmiles,
            "Exp_Tg_K": r.exp_tg_k,
            "pmsbp_density": r.pmsbp_density,
            "representation_class": r.representation_class,
            "polymer_class": r.polymer_class,
            "source": r.source,
            "reliability": r.reliability,
        }
        for r in rows
    ]
    write_csv(output_dir / "polymetrix_open_pmsbp_feature_table.csv", feature_rows)

    summary = overall_summary(rows)
    write_csv(output_dir / "overall_pmsbp_association_summary.csv", [summary])

    class_rows = group_summary(rows, "polymer_class")
    write_csv(output_dir / "polymer_class_stratified_summary.csv", class_rows)

    source_rows = group_summary(rows, "source")
    write_csv(output_dir / "source_stratified_summary.csv", source_rows)

    boot_row = bootstrap_row_ci(rows, n_bootstrap=n_bootstrap, seed=seed)
    boot_cluster = bootstrap_class_cluster_ci(rows, n_bootstrap=n_bootstrap, seed=seed + 1)
    write_csv(output_dir / "bootstrap_uncertainty_summary.csv", [boot_row, boot_cluster])

    perm = within_class_permutation(rows, n_permutation=n_permutation, seed=seed + 2)
    write_csv(output_dir / "within_class_permutation_summary.csv", [perm])

    loo_rows = leave_one_class_out(rows)
    write_csv(output_dir / "leave_one_class_out_sensitivity.csv", loo_rows)

    verdict = verdict_from_results(summary, boot_cluster, perm)
    write_csv(output_dir / "step18_reanalysis_verdict.csv", [{"verdict": verdict}])

    report = [
        "# Step 18 — Open-data pMSBP Statistical Re-analysis",
        "",
        f"Verdict: `{verdict}`",
        "",
        "## Main results",
        "",
        f"- Supported open rows: {summary.get('n_rows')}",
        f"- Polymer classes: {summary.get('n_polymer_classes')}",
        f"- Sources: {summary.get('n_sources')}",
        f"- Representation classes: {summary.get('n_representation_classes')}",
        f"- Overall Spearman rho: {summary.get('overall_spearman_rho')}",
        f"- Within-class median-residual Spearman rho: {summary.get('within_class_median_residual_spearman_rho')}",
        f"- Within-class mean-residual Spearman rho: {summary.get('within_class_mean_residual_spearman_rho')}",
        "",
        "## Uncertainty checks",
        "",
        f"- Row bootstrap: {n_bootstrap}",
        f"- Class-cluster bootstrap: {n_bootstrap}",
        f"- Within-class permutation: {n_permutation}",
        f"- Class-cluster bootstrap residual CI: [{boot_cluster.get('within_class_residual_rho_ci_low')}, {boot_cluster.get('within_class_residual_rho_ci_high')}]",
        f"- Within-class permutation empirical p: {perm.get('two_sided_empirical_p')}",
        "",
        "## Interpretation",
        "",
    ]

    if verdict.startswith("STEP18_GO"):
        report.extend(
            [
                "The open-data pMSBP re-analysis has a stable within-class signal under the current audit tests.",
                "",
                "This still does not make the journal manuscript final. The next step is Step 19: inspect whether the token-sequence pMSBP coordinate is chemically defensible, compare against existing descriptors, and write the revised manuscript around the open-data result only.",
            ]
        )
    elif verdict == "STEP18_MIXED_RAW_SIGNAL_WITHIN_CLASS_NOT_LOCKED":
        report.extend(
            [
                "The raw association is present, but within-class residual evidence is not locked under conservative uncertainty checks.",
                "",
                "Do not submit the journal paper as a strong principle claim. Step 19 should either refine the descriptor, use a narrower class/source scope, or reposition the paper as a limited open-data observation.",
            ]
        )
    else:
        report.extend(
            [
                "The current open-data result is not stable enough for a journal claim.",
                "",
                "Do not proceed to journal submission. Refine descriptor chemistry or data stratification first.",
            ]
        )

    report.extend(
        [
            "",
            "## Output files",
            "",
            "```text",
            "polymetrix_open_pmsbp_feature_table.csv",
            "overall_pmsbp_association_summary.csv",
            "polymer_class_stratified_summary.csv",
            "source_stratified_summary.csv",
            "bootstrap_uncertainty_summary.csv",
            "within_class_permutation_summary.csv",
            "leave_one_class_out_sensitivity.csv",
            "step18_reanalysis_verdict.csv",
            "```",
        ]
    )

    (output_dir / "STEP18_OPEN_DATA_PMSBP_REANALYSIS_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return verdict
