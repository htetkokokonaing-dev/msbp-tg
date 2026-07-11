from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    'data/external_sources.csv',
    'data/external_sources.md',
    'data/README_data_public_safe.md',
    'data/license_audit.md',
    'data/raw/README.md',
    'data/processed/README.md',
    'docs/data_provenance_protocol.md',
    'docs/data_availability_statement.md',
]


def test_data_provenance_files_exist():
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    assert missing == []


def test_public_safe_data_policy_mentions_no_raw_redistribution():
    text = (ROOT / 'data' / 'README_data_public_safe.md').read_text(encoding='utf-8').lower()
    assert 'does not redistribute raw third-party datasets' in text
    assert 'external_sources.csv' in text
    assert 'data/processed' in text


def test_processed_readme_documents_expected_local_feature_tables():
    text = (ROOT / 'data' / 'processed' / 'README.md').read_text(encoding='utf-8')
    for name in [
        'stage10_tsaicying_leak_excluded_novel_features.csv',
        'stage11_neurips_public_private_tg_known_novel_features.csv',
        'stage13_leeds_paek_novel_features.csv',
    ]:
        assert name in text
