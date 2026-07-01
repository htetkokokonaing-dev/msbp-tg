from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, rdMolDescriptors
except Exception:  # pragma: no cover
    Chem = None
    Descriptors = None
    rdMolDescriptors = None

@dataclass
class SmilesFeatures:
    canonical_smiles: str | None
    valid_rdkit: bool
    heavy_atoms: int | None
    mol_wt: float | None
    rotatable_bonds: int | None
    rings: int | None
    aromatic_rings: int | None
    aliphatic_rings: int | None
    hetero_atoms: int | None
    silicon_atoms: int | None
    rot_per_heavy: float | None
    rings_per_heavy: float | None
    arom_per_heavy: float | None
    hetero_per_heavy: float | None
    mobility_suppression_raw: float | None
    mobility_suppression_density: float | None

def canonicalize_smiles(smiles: str) -> str | None:
    """Canonicalize a SMILES/repeat-unit string using RDKit if available."""
    if Chem is None or not isinstance(smiles, str) or not smiles.strip():
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return Chem.MolToSmiles(mol, canonical=True)

def extract_smiles_features(smiles: str) -> SmilesFeatures:
    """Extract locked MSBP feature columns from a repeat-unit SMILES.

    RDKit's NumRotatableBonds is used as the rotatable-bond count. Polymer
    dummy atoms (*) are left in the repeat-unit representation when RDKit can
    parse them; unparseable rows are screened out by setting valid_rdkit=False.

    Important transparency note: mobility_suppression_density is not a new
    molecular descriptor. It is exactly the suppression-oriented sign reversal
    of rotatable-bond density: -NumRotatableBonds/heavy_atoms.
    """
    if Chem is None:
        raise RuntimeError('RDKit is required for raw SMILES feature extraction. Use environment.yml or install rdkit.')
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return SmilesFeatures(None, False, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    canonical = Chem.MolToSmiles(mol, canonical=True)
    heavy = int(mol.GetNumHeavyAtoms())
    rot = int(Descriptors.NumRotatableBonds(mol))
    rings = int(rdMolDescriptors.CalcNumRings(mol))
    aromatic_rings = int(rdMolDescriptors.CalcNumAromaticRings(mol))
    aliphatic_rings = int(rdMolDescriptors.CalcNumAliphaticRings(mol))
    hetero = int(sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() not in [0, 1, 6]))
    silicon = int(sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 14))
    mw = float(Descriptors.MolWt(mol))
    rot_density = (rot / heavy) if heavy else None
    rings_density = (rings / heavy) if heavy else None
    arom_density = (aromatic_rings / heavy) if heavy else None
    hetero_density = (hetero / heavy) if heavy else None
    return SmilesFeatures(
        canonical_smiles=canonical,
        valid_rdkit=True,
        heavy_atoms=heavy,
        mol_wt=mw,
        rotatable_bonds=rot,
        rings=rings,
        aromatic_rings=aromatic_rings,
        aliphatic_rings=aliphatic_rings,
        hetero_atoms=hetero,
        silicon_atoms=silicon,
        rot_per_heavy=rot_density,
        rings_per_heavy=rings_density,
        arom_per_heavy=arom_density,
        hetero_per_heavy=hetero_density,
        mobility_suppression_raw=-float(rot),
        mobility_suppression_density=-float(rot_density) if rot_density is not None else None,
)

def add_smiles_features(df: pd.DataFrame, smiles_col: str = 'SMILES') -> pd.DataFrame:
    rows = []
    for s in df[smiles_col].astype(str):
        rows.append(extract_smiles_features(s).__dict__)
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)
