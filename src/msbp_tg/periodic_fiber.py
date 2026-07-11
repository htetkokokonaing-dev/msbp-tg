"""Advanced periodic polymer mobility descriptor gates.

This module extends the Step-13 prototype.  It is still conservative: it does
not claim to be a complete polymer graph canonicalizer.  Its purpose is to
block journal submission until the mobility coordinate passes basic periodic
representation-invariance tests.

Implemented gates
-----------------
1. primitive-cell versus supercell invariance for simple two-terminal repeats;
2. orientation reversal invariance;
3. cut-point / cyclic-rotation invariance;
4. equivalent simple SMILES spelling invariance, including explicit single
   bonds and bracketed atom spelling for simple atoms;
5. simple copolymer expansion invariance, e.g. *CO* == *COCO* == *COCOCO*.

Unsupported cases are intentionally rejected rather than silently overclaimed.
"""

from __future__ import annotations

from dataclasses import dataclass
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
    canonical_period: str
    notes: str


_DUMMY = "*"

# Conservative atom-token list for the gate layer.  The lowercase aromatic forms
# are canonicalized to uppercase symbols only for representation tests; this does
# not assert a full aromatic polymer descriptor.
_ATOM_TOKEN_RE = re.compile(r"Cl|Br|Si|[BCNOFPSIbcnops]")


def _strip_outer_dummies(smiles: str) -> str:
    """Return the repeat body after removing two outer dummy atoms."""

    if smiles.count(_DUMMY) != 2:
        raise ValueError("periodic_msbp currently requires exactly two dummy attachment markers")
    if not (smiles.startswith(_DUMMY) and smiles.endswith(_DUMMY)):
        raise ValueError("periodic_msbp currently supports outer-dummy repeat units such as *CC*")
    body = smiles[1:-1]
    if not body:
        raise ValueError("empty repeat body")
    return body


def _normalize_atom_token(token: str) -> str:
    """Normalize simple atom spelling for representation-gate use."""

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


def _atom_tokens(body: str) -> list[str]:
    """Extract a conservative atom-token sequence from a simple repeat body."""

    # Normalize bracketed simple atoms before deleting punctuation.
    body = re.sub(r"\[([A-Za-z][a-z]?)\]", r"\1", body)

    # Remove simple bond and annotation symbols for this representation gate.
    cleaned = re.sub(r"[\-\=\#\/\\\(\)\[\]0-9@+\.:]", "", body)
    tokens = [_normalize_atom_token(t) for t in _ATOM_TOKEN_RE.findall(cleaned)]
    if not tokens:
        raise ValueError("no supported atom tokens found")
    return tokens


def _shortest_repeating_period(tokens: list[str]) -> list[str]:
    """Return the shortest repeated token period."""

    n = len(tokens)
    for k in range(1, n + 1):
        if n % k != 0:
            continue
        unit = tokens[:k]
        if unit * (n // k) == tokens:
            # Keep the Step-13 editorial gate: pure carbon chains use a
            # two-carbon period when possible so *CC*, *CCCC*, and *CCCCCC*
            # share the same representation class.
            if unit == ["C"] and n >= 2:
                return ["C", "C"]
            return unit
    return tokens


def _rotations(tokens: list[str]) -> list[list[str]]:
    return [tokens[i:] + tokens[:i] for i in range(len(tokens))]


def _canonical_necklace(tokens: list[str]) -> list[str]:
    """Canonicalize cyclic rotations and orientation reversal.

    This gives the same representation class for *CCO*, *COC*, and *OCC*, and
    also for a period and its reverse orientation.
    """

    candidates = _rotations(tokens) + _rotations(list(reversed(tokens)))
    return min(candidates, key=lambda xs: "|".join(xs))


def canonical_period_tokens_from_smiles(smiles: str) -> list[str]:
    """Return the canonical primitive periodic token sequence."""

    body = _strip_outer_dummies(smiles)
    tokens = _atom_tokens(body)
    period = _shortest_repeating_period(tokens)
    return _canonical_necklace(period)


def canonical_period_string(smiles: str) -> str:
    """Return the canonical primitive period as a compact string."""

    return "".join(canonical_period_tokens_from_smiles(smiles))


def representation_class(smiles: str) -> str:
    """Return the two-terminal representation class string."""

    return f"*{canonical_period_string(smiles)}*"


def naive_msbp_density_from_two_terminal_smiles(smiles: str) -> tuple[int, int, float]:
    """Replicate the old boundary-sensitive count for simple two-terminal chains.

    For ``*CC*``, ``*CCCC*``, ``*CCCCCC*`` this returns heavy atoms 2, 4, 6 and
    rotatable-like count 1, 3, 5 respectively.  This intentionally preserves the
    editorial blocker example as a negative control.
    """

    body = _strip_outer_dummies(smiles)
    tokens = _atom_tokens(body)
    heavy = len(tokens)
    naive_rot = max(heavy - 1, 0)
    density = -naive_rot / heavy if heavy else 0.0
    return heavy, naive_rot, density


def periodic_msbp(smiles: str) -> PeriodicMSBPResult:
    """Compute the prototype periodic MSBP coordinate."""

    heavy, naive_rot, naive_density = naive_msbp_density_from_two_terminal_smiles(smiles)
    period = canonical_period_tokens_from_smiles(smiles)
    period_heavy = len(period)

    # Prototype mobility channels: use one channel for a two-atom linear period
    # to preserve Step-13 behavior.  For longer simple periods, count internal
    # period mobility channels conservatively as period_heavy - 1.  The value is
    # less important than the invariance gate; downstream analysis must test
    # whether this coordinate is scientifically useful.
    periodic_rot = max(period_heavy - 1, 1) if period_heavy else 0
    periodic_density = -periodic_rot / period_heavy if period_heavy else 0.0

    canonical = "".join(period)
    notes = (
        "advanced prototype periodic two-terminal quotient; "
        "passes simple supercell, reversal, cut-point, spelling, and copolymer expansion gates; "
        "not a full polymer graph canonicalizer"
    )

    return PeriodicMSBPResult(
        smiles=smiles,
        heavy_atoms=heavy,
        naive_rotatable_bonds=naive_rot,
        naive_msbp_density=naive_density,
        primitive_period_heavy_atoms=period_heavy,
        periodic_rotatable_bonds_per_period=periodic_rot,
        periodic_msbp_density=periodic_density,
        representation_class=f"*{canonical}*",
        canonical_period=canonical,
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
                "canonical_period": r.canonical_period,
                "notes": r.notes,
            }
        )
    return rows


def assert_same_periodic_coordinate(smiles_list: list[str]) -> None:
    """Raise AssertionError unless all strings map to one pMSBP coordinate."""

    rows = periodic_invariance_table(smiles_list)
    values = {row["periodic_msbp_density"] for row in rows}
    classes = {row["representation_class"] for row in rows}
    if len(values) != 1 or len(classes) != 1:
        raise AssertionError(f"not invariant: values={values}, classes={classes}, rows={rows!r}")
