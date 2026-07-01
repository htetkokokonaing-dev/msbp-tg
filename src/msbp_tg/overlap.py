from __future__ import annotations

from.features import canonicalize_smiles

def canonical_overlap(candidate_smiles, prior_smiles):
    """Return candidate indices whose canonical SMILES overlap the prior set."""
    prior_can = {canonicalize_smiles(s) for s in prior_smiles}
    prior_can.discard(None)
    out = set()
    for i, s in enumerate(candidate_smiles):
        can = canonicalize_smiles(s)
        if can in prior_can:
            out.add(i)
    return out
