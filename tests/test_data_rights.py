from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_public_safe_checker():
    path = ROOT / 'scripts' / 'check_public_safe_repo.py'
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def test_csv_scanner_flags_structural_identifier_plus_tg(tmp_path):
    module = load_public_safe_checker()
    risky = tmp_path / 'risky.csv'
    risky.write_text(','.join(['canonical_smiles', 'Tg_C', 'source']) + '\n*CC*,100,x\n')
    is_risky, structure_hits, tg_hits = module.is_row_level_third_party_risk_csv(risky, root=tmp_path)
    assert is_risky
    assert 'canonical_smiles' in structure_hits
    assert 'tg_c' in tg_hits

def test_csv_scanner_allows_aggregate_validation_summary(tmp_path):
    module = load_public_safe_checker()
    ok = tmp_path / 'summary.csv'
    ok.write_text('source,n,spearman_rho,entropy_gain_nats\nStage 10,739,0.745,0.157\n')
    is_risky, structure_hits, tg_hits = module.is_row_level_third_party_risk_csv(ok, root=tmp_path)
    assert not is_risky
    assert not structure_hits

def test_removed_representative_row_level_case_table_is_absent():
    assert not (ROOT / 'tables' / ('representative_' + 'contradiction_and_support_cases.csv')).exists()
