"""CLA / سیلا — RDKit chemistry helpers (spec 01 §5, spec 03).

Design principles adapted from Molibrary (third_party/ATTRIBUTION.md):
* RDKit is gated behind a ``HAS_RDKIT`` flag — the application degrades
  gracefully when RDKit is unavailable (spec 03: "Provide graceful
  degradation").
* Structure search: exact match via InChIKey, substructure via
  ``HasSubstructMatch``, similarity via Morgan (radius 2, 2048 bits) +
  Tanimoto — the same approach Molibrary's /api/search uses, implemented
  with the modern ``rdFingerprintGenerator`` API.
"""

from __future__ import annotations

import re
from typing import Optional

try:
    from rdkit import Chem, RDLogger
    from rdkit.Chem import Descriptors, rdMolDescriptors
    from rdkit.Chem import rdFingerprintGenerator
    from rdkit.Chem import inchi as rd_inchi
    from rdkit import DataStructs

    RDLogger.DisableLog("rdApp.*")
    HAS_RDKIT = True
except ImportError:  # pragma: no cover - exercised only without RDKit
    HAS_RDKIT = False

# 2D rendering needs extra system libs (libXrender/libSM on Linux). It is
# imported lazily so that a missing drawing dependency never disables
# identifiers, validation, or structure search (spec 03: graceful degradation).
HAS_RDKIT_DRAW = False
if HAS_RDKIT:
    try:
        from rdkit.Chem import Draw  # noqa: F401
        HAS_RDKIT_DRAW = True
    except ImportError:
        HAS_RDKIT_DRAW = False

# InChIKey validation pattern (same convention as Molibrary's exact search)
INCHIKEY_RE = re.compile(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$")

_FP_GEN = None
if HAS_RDKIT:
    _FP_GEN = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)


def is_valid_inchikey(value: str) -> bool:
    return bool(value and INCHIKEY_RE.match(value.strip()))


def mol_from_smiles(smiles: str):
    """Return an RDKit mol (sanitized) or None. None also when no RDKit."""
    if not HAS_RDKIT or not smiles:
        return None
    try:
        return Chem.MolFromSmiles(smiles.strip())
    except Exception:
        return None


def validate_smiles(smiles: str) -> tuple[bool, str]:
    """(ok, message). Without RDKit we can only do a syntactic no-op check."""
    smiles = (smiles or "").strip()
    if not smiles:
        return False, "empty"
    if not HAS_RDKIT:
        return True, "accepted-unvalidated (RDKit not installed)"
    mol = mol_from_smiles(smiles)
    if mol is None:
        return False, "invalid"
    return True, "valid"


def canonical_smiles(smiles: str) -> Optional[str]:
    mol = mol_from_smiles(smiles)
    return Chem.MolToSmiles(mol) if mol is not None else None


def compute_identifiers(smiles: str) -> dict:
    """Derive canonical SMILES / InChI / InChIKey / formula / MW from SMILES.

    SMILES is the single source of truth for computed identifiers — this
    avoids transcription errors in the seed data and for user input.
    Without RDKit every computed value is None.
    """
    out = {"smiles": None, "inchi": None, "inchikey": None,
           "formula": None, "molecular_weight": None}
    mol = mol_from_smiles(smiles)
    if mol is None:
        return out
    out["smiles"] = Chem.MolToSmiles(mol)
    out["formula"] = rdMolDescriptors.CalcMolFormula(mol)
    out["molecular_weight"] = round(Descriptors.MolWt(mol), 3)
    try:
        inchi_str = rd_inchi.MolToInchi(mol)
        if inchi_str:
            out["inchi"] = inchi_str
            out["inchikey"] = rd_inchi.InchiToInchiKey(inchi_str)
    except Exception:
        pass
    return out


def inchikey_from_smiles(smiles: str) -> Optional[str]:
    return compute_identifiers(smiles)["inchikey"]


def render_png(smiles: str, width: int = 320, height: int = 240) -> Optional[bytes]:
    """2D structure PNG for the browser UI (spec 01 §3: 'View 2D structure')."""
    if not HAS_RDKIT_DRAW:
        return None
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    try:
        return Draw.MolToImage(mol, size=(width, height), format="png")
    except Exception:
        return None


def get_fingerprint(smiles: str):
    mol = mol_from_smiles(smiles)
    if mol is None or _FP_GEN is None:
        return None
    return _FP_GEN.GetFingerprint(mol)


def tanimoto(smiles_a: str, smiles_b: str) -> Optional[float]:
    fp_a, fp_b = get_fingerprint(smiles_a), get_fingerprint(smiles_b)
    if fp_a is None or fp_b is None:
        return None
    return DataStructs.TanimotoSimilarity(fp_a, fp_b)


def has_substructure(target_smiles: str, query_smiles: str) -> bool:
    """True when query (substructure SMARTS/SMILES) matches target."""
    if not HAS_RDKIT:
        return False
    target = mol_from_smiles(target_smiles)
    query = Chem.MolFromSmarts(query_smiles.strip()) if query_smiles else None
    if query is None:
        query = mol_from_smiles(query_smiles)
    if target is None or query is None:
        return False
    try:
        return target.HasSubstructMatch(query)
    except Exception:
        return False


def mol_to_sdf_block(smiles: str) -> Optional[str]:
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    try:
        return Chem.MolToMolBlock(mol)
    except Exception:
        return None


def sdf_block_to_smiles(molblock: str) -> Optional[str]:
    if not HAS_RDKIT or not molblock:
        return None
    try:
        mol = Chem.MolFromMolBlock(molblock)
        return Chem.MolToSmiles(mol) if mol is not None else None
    except Exception:
        return None


def rdkit_status_message() -> str:
    """Human-readable capability note for the UI sidebar."""
    if HAS_RDKIT:
        from rdkit import __version__
        extra = "" if HAS_RDKIT_DRAW else " (2D rendering unavailable — missing system graphics libs)"
        return f"RDKit {__version__}{extra}"
    return "RDKit NOT installed — structure rendering and substructure/similarity search are disabled"
