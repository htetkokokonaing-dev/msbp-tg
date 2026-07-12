#!/usr/bin/env python
from __future__ import annotations
import argparse
from pathlib import Path
from msbp_tg.comparator_evidence import write_step19_outputs


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--n-bootstrap', type=int, default=200)
    ap.add_argument('--seed', type=int, default=19019)
    args=ap.parse_args()
    out=Path('results/step19_comparator_descriptor_evidence_hardening')
    v=write_step19_outputs(Path('.').resolve(), out, n_bootstrap=args.n_bootstrap, seed=args.seed)
    print('Step-19 comparator descriptor and journal evidence hardening')
    print(f'Output directory: {out.resolve()}')
    print(f'Verdict: {v}')

if __name__ == '__main__': main()
