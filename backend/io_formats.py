"""CLA / سیلا — export / import support: CSV, JSON, SDF (spec 01 §1).

Export covers the whole library; import is best-effort with duplicate
protection (same InChIKey → skipped) and a per-row error report.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

from backend import chemistry, materials

_EXPORT_COLUMNS = [
    "id", "name_en", "name_fa", "smiles", "inchi", "inchikey", "formula",
    "molecular_weight", "cas", "synonyms", "quantity", "unit", "min_stock",
    "status", "ghs_hazards", "notes", "melting_point_c", "boiling_point_c",
    "density_g_ml", "appearance", "solubility", "created_at", "updated_at",
]


def _material_to_dict(m: materials.Material) -> dict:
    d = {c: getattr(m, c, "") for c in _EXPORT_COLUMNS}
    d["synonyms"] = m.synonyms
    d["ghs_hazards"] = m.ghs_hazards
    return d


# --------------------------------------------------------------------------
# Export
# --------------------------------------------------------------------------

def export_csv(db_path: Path | None = None) -> str:
    rows = [_material_to_dict(m) for m in materials.list_materials(db_path=db_path)]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=_EXPORT_COLUMNS)
    writer.writeheader()
    for r in rows:
        r = dict(r)
        r["synonyms"] = "; ".join(r["synonyms"])
        r["ghs_hazards"] = "; ".join(r["ghs_hazards"])
        writer.writerow(r)
    return buf.getvalue()


def export_json(db_path: Path | None = None) -> str:
    rows = [_material_to_dict(m) for m in materials.list_materials(db_path=db_path)]
    return json.dumps({"materials": rows}, ensure_ascii=False, indent=2)


def export_sdf(db_path: Path | None = None) -> str:
    """SDF with material metadata as property tags (requires RDKit)."""
    if not chemistry.HAS_RDKIT:
        raise RuntimeError("RDKit is required for SDF export")
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors

    writer = io.StringIO()
    for m in materials.list_materials(db_path=db_path):
        mol = chemistry.mol_from_smiles(m.smiles) if m.smiles else None
        if mol is None:
            continue
        mol.SetProp("_Name", m.name_en)
        for tag, value in (
            ("name_en", m.name_en), ("name_fa", m.name_fa), ("cas", m.cas),
            ("inchikey", m.inchikey), ("quantity", str(m.quantity)),
            ("unit", m.unit), ("status", m.status), ("min_stock", str(m.min_stock)),
            ("synonyms", "; ".join(m.synonyms)),
            ("ghs_hazards", "; ".join(m.ghs_hazards)), ("notes", m.notes),
        ):
            if value:
                mol.SetProp(tag, str(value))
        writer.write(Chem.MolToMolBlock(mol))
        for tag in ("name_en", "name_fa", "cas", "inchikey", "quantity", "unit",
                    "status", "min_stock", "synonyms", "ghs_hazards", "notes"):
            val = mol.GetProp(tag) if mol.HasProp(tag) else ""
            if val:
                writer.write(f"> <{tag}>\n{val}\n\n")
        writer.write("$$$$\n")
    return writer.getvalue()


# --------------------------------------------------------------------------
# Import
# --------------------------------------------------------------------------

def parse_csv(text: str) -> list[dict]:
    """Accepts both CLA exports and generic CSVs with recognizable headers."""
    reader = csv.DictReader(io.StringIO(text))
    out = []
    for raw in reader:
        row = { (k or "").strip().lower(): (v or "").strip() for k, v in raw.items() }
        out.append(_normalize_row(row))
    return [r for r in out if r.get("name_en") or r.get("smiles")]


def parse_json(text: str) -> list[dict]:
    data = json.loads(text)
    rows = data.get("materials", data) if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError("JSON must contain a list of materials")
    out = []
    for raw in rows:
        if not isinstance(raw, dict):
            continue
        row = { str(k).strip().lower(): v for k, v in raw.items() }
        out.append(_normalize_row(row))
    return [r for r in out if r.get("name_en") or r.get("smiles")]


def parse_sdf(text: str) -> list[dict]:
    if not chemistry.HAS_RDKIT:
        raise RuntimeError("RDKit is required for SDF import")
    from rdkit import Chem
    out = []
    supplier = Chem.ForwardSDMolSupplier(io.BytesIO(text.encode("utf-8")), sanitize=True)
    for mol in supplier:
        if mol is None:
            continue
        props = mol.GetPropsAsDict()
        row = {str(k).lower(): v for k, v in props.items()}
        row.setdefault("smiles", Chem.MolToSmiles(mol))
        if not row.get("name_en"):
            row["name_en"] = mol.GetProp("_Name") if mol.HasProp("_Name") else row["smiles"]
        out.append(_normalize_row(row))
    return out


def _normalize_row(row: dict) -> dict:
    """Map heterogeneous import keys onto the canonical material dict."""
    def pick(*names, default=""):
        for n in names:
            if n in row and row[n] not in (None, ""):
                return row[n]
        return default

    def num(*names):
        v = pick(*names, default=None)
        try:
            return float(v) if v is not None and v != "" else None
        except (TypeError, ValueError):
            return None

    synonyms = pick("synonyms", default=[])
    if isinstance(synonyms, str):
        synonyms = [s.strip() for s in synonyms.replace(";", ",").split(",") if s.strip()]
    ghs = pick("ghs_hazards", "ghs", default=[])
    if isinstance(ghs, str):
        ghs = [s.strip() for s in ghs.replace(";", ",").split(",") if s.strip()]

    smiles = str(pick("smiles", "canonical_smiles", default=""))
    canon = chemistry.canonical_smiles(smiles) or smiles

    return {
        "name_en": str(pick("name_en", "name", default="")).strip(),
        "name_fa": str(pick("name_fa", default="")).strip(),
        "smiles": canon,
        "cas": str(pick("cas", "cas_number", default="")).strip(),
        "synonyms": synonyms,
        "ghs_hazards": ghs,
        "quantity": num("quantity") or 0.0,
        "unit": str(pick("unit", default="g")).strip() or "g",
        "min_stock": num("min_stock") or 0.0,
        "status": str(pick("status", default="Active")).strip() or "Active",
        "notes": str(pick("notes", default="")),
        "melting_point_c": num("melting_point_c", "mp", "mp_c"),
        "boiling_point_c": num("boiling_point_c", "bp", "bp_c"),
        "density_g_ml": num("density_g_ml", "density"),
        "appearance": str(pick("appearance", default="")),
    }


def import_rows(rows: list[dict], db_path: Path | None = None) -> dict:
    """Insert parsed rows; skip InChIKey duplicates. Returns a summary."""
    summary = {"imported": 0, "skipped": 0, "errors": 0, "names": []}
    existing = {
        (m.inchikey or "").upper()
        for m in materials.list_materials(db_path=db_path) if m.inchikey
    }
    for row in rows:
        try:
            if not row.get("name_en") and row.get("smiles"):
                row["name_en"] = row["smiles"]
            if not row.get("name_en"):
                summary["errors"] += 1
                continue
            key = (chemistry.inchikey_from_smiles(row.get("smiles", "")) or "").upper()
            if key and key in existing:
                summary["skipped"] += 1
                continue
            m = materials.add_material(row, db_path=db_path, action="imported")
            if key:
                existing.add(key)
            summary["imported"] += 1
            summary["names"].append(m.name_en)
        except Exception:
            summary["errors"] += 1
    return summary
