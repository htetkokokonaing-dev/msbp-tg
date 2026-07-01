#!/usr/bin/env python
from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {'.pyc', '.pyo'}
TRANSIENT_DIRS = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}
FORBIDDEN_DATA_PATTERNS = [
    'data/processed/stage10_',
    'data/processed/stage11_',
    'data/processed/stage13_',
    'data/external/Tg_dataset',
    'data/external/neurips',
    'data/external/Leeds_',
]
STRUCTURE_COLUMNS = {
    'smiles', 'smiles_raw', 'smiles_clean', 'canonical_smiles', 'psmiles',
    'canonical_psmiles', 'repeat_unit_smiles', 'polymer_smiles',
}
TG_COLUMNS = {
    'tg', 'tg_c', 'tg_k', 'tg_value', 'tg_value_raw', 'tg_resid',
    'tg_residual', 'glass_transition_temperature', 'target_tg',
}
CSV_SCAN_EXEMPT_PATHS = {
    'data/manifest.csv',
}

def normalized_header(path: Path) -> set[str]:
    """Return lowercase normalized CSV headers, or an empty set if unreadable."""
    try:
        with path.open(newline='', encoding='utf-8-sig') as fh:
            reader = csv.reader(fh)
            header = next(reader, [])
    except Exception:
        return set()
    return {h.strip().lower() for h in header if h and h.strip()}

def is_row_level_third_party_risk_csv(path: Path, root: Path = ROOT) -> tuple[bool, set[str], set[str]]:
    """Flag CSVs that combine structural identifiers with Tg-like row fields.

    Public releases intentionally avoid third-party-derived row-level SMILES/Tg
    tables. Aggregate validation tables are allowed because they do not include
    structural identifiers. The scan is conservative and header-based.
    """
    rel = path.relative_to(root).as_posix()
    if rel in CSV_SCAN_EXEMPT_PATHS:
        return False, set(), set()
    header = normalized_header(path)
    structure_hits = header & STRUCTURE_COLUMNS
    tg_hits = header & TG_COLUMNS
    return bool(structure_hits and tg_hits), structure_hits, tg_hits

def main() -> int:
    problems: list[str] = []
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in TRANSIENT_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f'forbidden compiled file: {rel}')
        if path.is_file():
            for pattern in FORBIDDEN_DATA_PATTERNS:
                if rel.startswith(pattern):
                    problems.append(f'possible third-party data file in public-safe repo: {rel}')
            if path.suffix.lower() == '.csv':
                risky, structure_hits, tg_hits = is_row_level_third_party_risk_csv(path)
                if risky:
                    problems.append(
                        'possible row-level third-party SMILES/Tg table: '
                        f'{rel} (structure columns={sorted(structure_hits)}, '
                        f'Tg-like columns={sorted(tg_hits)})'
)
    if problems:
        print('Public-safe check failed:')
        for p in problems:
            print(f'- {p}')
        return 1
    print('Public-safe check passed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
