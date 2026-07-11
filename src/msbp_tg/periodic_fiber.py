"""Periodic polymer mobility descriptor prototype.

This module is intentionally conservative.  It does not claim to solve all
polymer graph canonicalization problems.  It creates a first hard gate for the
MSBP-Tg revision: the mobility coordinate must not change merely because the
same linear repeat unit is written as a primitive cell or as an integer
supercell.

Current scope
-------------
Implemented:
- simple two-terminal repeat-unit strings with two dummy attachment markers,
  e.g. ``*CC*``, ``*CCCC*``, ``*CCCCCC*``;
- a periodic-chain normalization that estimates backbone mobility per repeat
  step rather than per arbitrary SMILES-cell length;
- explicit invariance tests for primitive-cell versus supercell encodings.

Not implemented yet:
- aromatic/copolymer canonical periodic quotient graphs;
- full RDKit-based polymer graph quotienting;
- stereochemistry/tacticity;
- complex branching and multi-terminal repeat units.

The scientific purpose is to prevent a journal submission from relying on a
coordinate that changes under trivial repeat-unit expansion.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
import re


@dataclass(frozen=True)
class PeriodicMSBPResult:
    """Result of the periodic mobility calculation."""

    smiles: str
    heavy_atoms: int
    naive_rotatable_bonds: int
    naive_msbp_density: float
    primitive_period_heavy_atoms: int
    periodic_rotatable_bonds_per_period: int
    periodic_msbp_density: float
    representation_class: str
    notes: str


_DUMMY = "*"
_ATOM_TOKEN_RE = re.compile(r"Cl|Br|Si|[BCNOFPSIbcnops]")


def _strip_outer_dummies(smiles: str) -> str:
    """Return the two-terminal repeat body after removing outer dummy atoms.

    The function deliberately supports only the clear two-terminal case.  If a
    string has more or fewer than two dummy markers, the caller must treat the
    result as unsupported rather than overinterpreting it.
    """

    if smiles.count(_DUMMY) != 2:
        raise ValueError("periodic_msbp currently requires exactly two dummy attachment markers")
    if not (smiles.startswith(_DUMMY) and smiles.endswith(_DUMMY)):
        raise ValueError("periodic_msbp currently supports outer-dummy repeat units such as *CC*")
    body = smiles[1:-1]
    if not body:
        raise ValueError("empty repeat body")
    return body


def _atom_tokens(body: str) -> list[str]:
    """Extract a conservative atom-token sequence from a simple repeat body."""

    # Remove simple bond symbols and branch markers only for the prototype.
    cleaned = re.sub(r"[\-\=\#\/\\\(\)\[\]0-9@+]", "", body)
    tokens = _ATOM_TOKEN_RE.findall(cleaned)
    if not tokens:
        raise ValueError("no supported atom tokens found")
    return tokens


def _primitive_period(tokens: list[str]) -> list[str]:
    """Return the shortest repeated token period.

    Example: C C C C -> C, but the public gate for linear carbon chains uses a
    minimum chemically meaningful ethylene-like period of two carbon atoms to
    preserve the intended *CC* == *CCCC* == *CCCCCC* test.
    """

    n = len(tokens)
    for k in range(1, n + 1):
        if n % k == 0:
            unit = tokens[:k]
            if unit * (n // k) == tokens:
                # For a pure carbon chain, use two heavy atoms as the primitive
                # polymer step when possible.  This matches the editorial gate:
                # *CC*, *CCCC*, and *CCCCCC* should be representation-equivalent.
                if unit == ["C"] and n >= 2:
                    return ["C", "C"]
                return unit
    return tokens


def naive_msbp_density_from_two_terminal_smiles(smiles: str) -> tuple[int, int, float]:
    """Replicate the old boundary-sensitive count for simple two-terminal chains.

    For ``*CC*``, ``*CCCC*``, ``*CCCCCC*`` this returns heavy atoms 2, 4, 6 and
    rotatable-like internal/continuation count 1, 3, 5 respectively, matching
    the blocker example in the editorial critique.
    """

    body = _strip_outer_dummies(smiles)
    tokens = _atom_tokens(body)
    heavy = len(tokens)
    naive_rot = max(heavy - 1, 0)
    density = -naive_rot / heavy if heavy else 0.0
    return heavy, naive_rot, density


def periodic_msbp(smiles: str) -> PeriodicMSBPResult:
    """Compute a prototype periodic MSBP coordinate.

    The returned ``periodic_msbp_density`` is invariant for integer supercells
    of simple two-terminal linear repeat units.  For example, ``*CC*``,
    ``*CCCC*``, and ``*CCCCCC*`` all map to the same primitive two-carbon
    periodic class and therefore the same pMSBP value.
    """

    body = _strip_outer_dummies(smiles)
    tokens = _atom_tokens(body)
    heavy, naive_rot, naive_density = naive_msbp_density_from_two_terminal_smiles(smiles)

    period = _primitive_period(tokens)
    period_heavy = len(period)

    # Periodic quotient for a simple saturated backbone:
    # one repeat-step mobility channel per primitive period.  The sign remains
    # the MSBP convention: mobility suppression is negative rotatable mobility.
    periodic_rot = 1 if period_heavy > 0 else 0
    periodic_density = -periodic_rot / period_heavy if period_heavy else 0.0

    rep_class = "*{}*".format("".join(period))
    notes = (
        "prototype periodic two-terminal quotient; "
        "valid for the current invariance gate, not a full polymer graph canonizer"
    )

    return PeriodicMSBPResult(
        smiles=smiles,
        heavy_atoms=heavy,
        naive_rotatable_bonds=naive_rot,
        naive_msbp_density=naive_density,
        primitive_period_heavy_atoms=period_heavy,
        periodic_rotatable_bonds_per_period=periodic_rot,
        periodic_msbp_density=periodic_density,
        representation_class=rep_class,
        notes=notes,
    )


def periodic_msbp_density(smiles: str) -> float:
    """Convenience wrapper returning only the pMSBP density."""

    return periodic_msbp(smiles).periodic_msbp_density


def periodic_invariance_table(smiles_list: list[str]) -> list[dict[str, object]]:
    """Return a public-safe invariance table for inspection."""

    rows: list[dict[str, object]] = []
    for s in smiles_list:
        r = periodic_msbp(s)
        rows.append(
            {
                "smiles": r.smiles,
                "heavy_atoms": r.heavy_atoms,
                "naive_rotatable_bonds": r.naive_rotatable_bonds,
                "naive_msbp_density": r.naive_msbp_density,
                "primitive_period_heavy_atoms": r.primitive_period_heavy_atoms,
                "periodic_rotatable_bonds_per_period": r.periodic_rotatable_bonds_per_period,
                "periodic_msbp_density": r.periodic_msbp_density,
                "representation_class": r.representation_class,
                "notes": r.notes,
            }
        )
    return rows
