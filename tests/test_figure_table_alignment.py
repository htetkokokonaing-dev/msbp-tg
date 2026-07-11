from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MSBP_Tg_Journal_Submission_Manuscript.md"


def test_manuscript_figure_links_exist():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    assert links, "No figure links found in manuscript"
    for link in links:
        target = (MANUSCRIPT.parent / link).resolve() if link.startswith("../") else (ROOT / link).resolve()
        assert target.exists(), f"Missing figure link target: {link}"
        assert target.stat().st_size > 0, f"Empty figure file: {link}"


def test_required_public_safe_table_files_exist_and_are_referenced():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    required = [
        "results/three_source_recomputed_summary.csv",
        "tables/residual_centering_sensitivity.csv",
        "tables/bootstrap_ci_spearman.csv",
        "tables/entropy_shuffle_empirical_p.csv",
        "tables/known_descriptor_comparison_compact.csv",
        "tables/paired_descriptor_bootstrap_ring_summary.csv",
        "tables/effect_size_slope_compact.csv",
        "tables/contradiction_taxonomy_source_summary.csv",
        "tables/source_role_notes.csv",
    ]
    for rel in required:
        path = ROOT / rel
        assert path.exists(), f"Missing public-safe table file: {rel}"
        assert path.stat().st_size > 0, f"Empty public-safe table file: {rel}"
        assert rel in text, f"Manuscript does not reference table file: {rel}"
