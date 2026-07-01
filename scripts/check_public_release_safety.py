#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSIENT_DIRS = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}
FORBIDDEN_NAME_PARTS = [
    'Private_Manuscript', 'STAGE18_PRIVATE_REPORT', 'build_stage19_revision.py',
]
FORBIDDEN_SUFFIXES = {'.pyc', '.pyo'}
# Avoid spelling private-path tokens literally in this file, so the checker does not flag itself.
FORBIDDEN_TEXT_PARTS = [
    '/mnt/data/' + 'tg_private_',
    '/mnt/data/' + 'stage',
    'user-' + 'OOPJ5qj5zAll2LRKjPJvGS4z',
]

errors = []
for path in ROOT.rglob('*'):
    rel_path = path.relative_to(ROOT)
    rel = rel_path.as_posix()
    if any(part in TRANSIENT_DIRS for part in rel_path.parts):
        continue
    if any(part in rel for part in FORBIDDEN_NAME_PARTS):
        errors.append(f'Forbidden path/name: {rel}')
    if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
        errors.append(f'Forbidden compiled file: {rel}')
    if path.is_file() and path.suffix.lower() in {'.py', '.md', '.txt', '.json', '.yml', '.yaml', '.cff'}:
        try:
            text = path.read_text(errors='ignore')
        except Exception:
            continue
        for token in FORBIDDEN_TEXT_PARTS:
            if token in text:
                errors.append(f'Forbidden private path token in {rel}: {token}')
if errors:
    print('PUBLIC RELEASE SAFETY CHECK: FAIL')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('PUBLIC RELEASE SAFETY CHECK: PASS')
