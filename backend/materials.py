"""CLA / سیلا — Starting Materials repository (spec 01, spec 06).

All user-facing operations go through this module:
* CRUD with automatic identifier computation (RDKit) and change history
* Stock control: set / adjust quantity with unit (spec 01 §3)
* Status control: Active / Inactive  (+ derived OutOfStock / LowStock)
* Search: text (name/synonyms/CAS/SMILES/InChIKey), exact InChIKey,
  substructure, similarity (spec 01 §3)

The main CLA application (Phase 2) will consume ``available_for_synthesis()``
— only materials with effective status Active and quantity > 0
(spec 01 §6: Integration with Main CLA).
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from backend import chemistry, db
from backend.db import utc_now_iso

# --------------------------------------------------------------------------
# Material model
# --------------------------------------------------------------------------

STATUS_ACTIVE = "Active"
STATUS_INACTIVE = "Inactive"
# Derived (never stored as user intent, kept for filtering/display):
STATUS_OUT_OF_STOCK = "OutOfStock"
STATUS_LOW_STOCK = "LowStock"

UNITS = ["g", "mg", "kg", "mL", "L", "mol", "mmol"]


@dataclass
class Material:
    id: int
    name_en: str
    name_fa: str = ""
    smiles: str = ""
    inchi: str = ""
    inchikey: str = ""
    formula: str = ""
    molecular_weight: Optional[float] = None
    cas: str = ""
    synonyms: list[str] = field(default_factory=list)
    quantity: float = 0.0
    unit: str = "g"
    min_stock: float = 0.0
    status: str = STATUS_ACTIVE          # user intent: Active | Inactive
    ghs_hazards: list[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""
    # optional 1:1 properties row
    melting_point_c: Optional[float] = None
    boiling_point_c: Optional[float] = None
    density_g_ml: Optional[float] = None
    appearance: str = ""
    solubility: str = ""

    # -- derived state -----------------------------------------------------
    @property
    def effective_status(self) -> str:
        """Active / Inactive / OutOfStock / LowStock (see backend.db docstring)."""
        if self.status == STATUS_INACTIVE:
            return STATUS_INACTIVE
        if (self.quantity or 0) <= 0:
            return STATUS_OUT_OF_STOCK
        if (self.quantity or 0) <= (self.min_stock or 0):
            return STATUS_LOW_STOCK
        return STATUS_ACTIVE

    @property
    def is_available(self) -> bool:
        """Phase-2 gate: usable in synthesis (spec 01 §6)."""
        return self.status == STATUS_ACTIVE and (self.quantity or 0) > 0

    @property
    def display_name(self) -> str:
        return self.name_en


def _row_to_material(row: sqlite3.Row, prop_row: Optional[sqlite3.Row] = None) -> Material:
    m = Material(
        id=row["id"],
        name_en=row["name_en"] or "",
        name_fa=row["name_fa"] or "",
        smiles=row["smiles"] or "",
        inchi=row["inchi"] or "",
        inchikey=row["inchikey"] or "",
        formula=row["formula"] or "",
        molecular_weight=row["molecular_weight"],
        cas=row["cas"] or "",
        synonyms=json.loads(row["synonyms"] or "[]"),
        quantity=float(row["quantity"] or 0),
        unit=row["unit"] or "g",
        min_stock=float(row["min_stock"] or 0),
        status=row["status"] or STATUS_ACTIVE,
        ghs_hazards=json.loads(row["ghs_hazards"] or "[]"),
        notes=row["notes"] or "",
        created_at=row["created_at"] or "",
        updated_at=row["updated_at"] or "",
    )
    if prop_row is not None:
        m.melting_point_c = prop_row["melting_point_c"]
        m.boiling_point_c = prop_row["boiling_point_c"]
        m.density_g_ml = prop_row["density_g_ml"]
        m.appearance = prop_row["appearance"] or ""
        m.solubility = prop_row["solubility"] or ""
    return m


def _fetch_props(conn: sqlite3.Connection, material_id: int) -> Optional[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM properties WHERE material_id = ?", (material_id,)
    ).fetchone()


def _log_history(conn: sqlite3.Connection, material_id: int, action: str,
                 detail: str = "", qty_before: Optional[float] = None,
                 qty_after: Optional[float] = None) -> None:
    conn.execute(
        "INSERT INTO history (material_id, action, detail, quantity_before,"
        " quantity_after, created_at) VALUES (?,?,?,?,?,?)",
        (material_id, action, detail, qty_before, qty_after, utc_now_iso()),
    )


def _upsert_props(conn: sqlite3.Connection, material_id: int, data: dict) -> None:
    vals = (
        data.get("melting_point_c"), data.get("boiling_point_c"),
        data.get("density_g_ml"), data.get("appearance") or None,
        data.get("solubility") or None,
    )
    if all(v is None for v in vals):
        return
    conn.execute(
        """INSERT INTO properties (material_id, melting_point_c, boiling_point_c,
               density_g_ml, appearance, solubility)
           VALUES (?,?,?,?,?,?)
           ON CONFLICT(material_id) DO UPDATE SET
               melting_point_c = excluded.melting_point_c,
               boiling_point_c = excluded.boiling_point_c,
               density_g_ml    = excluded.density_g_ml,
               appearance      = excluded.appearance,
               solubility      = excluded.solubility""",
        (material_id, *vals),
    )


# --------------------------------------------------------------------------
# CRUD
# --------------------------------------------------------------------------

def add_material(data: dict, db_path: Path | None = None,
                 action: str = "created") -> Material:
    """Insert a new material. Identifiers are computed from SMILES via RDKit.

    ``data`` keys mirror the Material fields; synonyms/ghs_hazards may be
    passed as lists or JSON strings.
    """
    now = utc_now_iso()
    smiles = (data.get("smiles") or "").strip()
    ident = chemistry.compute_identifiers(smiles) if smiles else {}
    row = {
        "name_en": (data.get("name_en") or "").strip(),
        "name_fa": (data.get("name_fa") or "").strip(),
        "smiles": ident.get("smiles") or smiles,
        "inchi": data.get("inchi") or ident.get("inchi") or "",
        "inchikey": data.get("inchikey") or ident.get("inchikey") or "",
        "formula": data.get("formula") or ident.get("formula") or "",
        "molecular_weight": data.get("molecular_weight")
        if data.get("molecular_weight") is not None
        else ident.get("molecular_weight"),
        "cas": (data.get("cas") or "").strip(),
        "synonyms": json.dumps(_as_list(data.get("synonyms")), ensure_ascii=False),
        "quantity": float(data.get("quantity") or 0),
        "unit": (data.get("unit") or "g").strip(),
        "min_stock": float(data.get("min_stock") or 0),
        "status": data.get("status") or STATUS_ACTIVE,
        "ghs_hazards": json.dumps(_as_list(data.get("ghs_hazards")), ensure_ascii=False),
        "notes": (data.get("notes") or "").strip(),
        "created_at": now,
        "updated_at": now,
    }
    if not row["name_en"]:
        raise ValueError("name_en is required")
    with db.get_conn(db_path) as conn:
        cur = conn.execute(
            """INSERT INTO materials (name_en, name_fa, smiles, inchi, inchikey,
                   formula, molecular_weight, cas, synonyms, quantity, unit,
                   min_stock, status, ghs_hazards, notes, created_at, updated_at)
               VALUES (:name_en, :name_fa, :smiles, :inchi, :inchikey, :formula,
                   :molecular_weight, :cas, :synonyms, :quantity, :unit,
                   :min_stock, :status, :ghs_hazards, :notes, :created_at, :updated_at)""",
            row,
        )
        mid = cur.lastrowid
        _upsert_props(conn, mid, data)
        _log_history(conn, mid, action,
                     detail=row["name_en"],
                     qty_after=row["quantity"])
        m = get_material(mid, db_path=db_path, _conn=conn)
    return m  # type: ignore[return-value]


def update_material(material_id: int, data: dict,
                    db_path: Path | None = None) -> Optional[Material]:
    """Update editable fields; identifiers recomputed when SMILES changes."""
    existing = get_material(material_id, db_path=db_path)
    if existing is None:
        return None
    merged: dict[str, Any] = {
        "name_en": data.get("name_en", existing.name_en),
        "name_fa": data.get("name_fa", existing.name_fa),
        "cas": data.get("cas", existing.cas),
        "synonyms": _as_list(data.get("synonyms", existing.synonyms)),
        "unit": data.get("unit", existing.unit),
        "min_stock": data.get("min_stock", existing.min_stock),
        "ghs_hazards": _as_list(data.get("ghs_hazards", existing.ghs_hazards)),
        "notes": data.get("notes", existing.notes),
        "smiles": data.get("smiles", existing.smiles),
        "inchi": data.get("inchi", existing.inchi),
        "inchikey": data.get("inchikey", existing.inchikey),
        "formula": data.get("formula", existing.formula),
        "molecular_weight": data.get("molecular_weight", existing.molecular_weight),
    }
    new_smiles = (merged["smiles"] or "").strip()
    if new_smiles != existing.smiles and new_smiles:
        ident = chemistry.compute_identifiers(new_smiles)
        merged["smiles"] = ident.get("smiles") or new_smiles
        merged["inchi"] = ident.get("inchi") or ""
        merged["inchikey"] = ident.get("inchikey") or ""
        merged["formula"] = ident.get("formula") or ""
        merged["molecular_weight"] = ident.get("molecular_weight")
    with db.get_conn(db_path) as conn:
        conn.execute(
            """UPDATE materials SET
                   name_en=:name_en, name_fa=:name_fa, smiles=:smiles,
                   inchi=:inchi, inchikey=:inchikey, formula=:formula,
                   molecular_weight=:molecular_weight, cas=:cas,
                   synonyms=:synonyms_json, unit=:unit, min_stock=:min_stock,
                   ghs_hazards=:ghs_json, notes=:notes, updated_at=:updated_at
               WHERE id=:id""",
            {
                "id": material_id,
                "name_en": (merged["name_en"] or "").strip(),
                "name_fa": (merged["name_fa"] or "").strip(),
                "smiles": merged["smiles"] or "",
                "inchi": merged["inchi"] or "",
                "inchikey": merged["inchikey"] or "",
                "formula": merged["formula"] or "",
                "molecular_weight": merged["molecular_weight"],
                "cas": (merged["cas"] or "").strip(),
                "synonyms_json": json.dumps(merged["synonyms"], ensure_ascii=False),
                "unit": merged["unit"] or "g",
                "min_stock": float(merged["min_stock"] or 0),
                "ghs_json": json.dumps(merged["ghs_hazards"], ensure_ascii=False),
                "notes": merged["notes"] or "",
                "updated_at": utc_now_iso(),
            },
        )
        _upsert_props(conn, material_id, data)
        _log_history(conn, material_id, "edited", detail=merged["name_en"] or "")
    return get_material(material_id, db_path=db_path)


def get_material(material_id: int, db_path: Path | None = None,
                 _conn: sqlite3.Connection | None = None) -> Optional[Material]:
    if _conn is not None:
        row = _conn.execute(
            "SELECT * FROM materials WHERE id = ?", (material_id,)
        ).fetchone()
        return _row_to_material(row, _fetch_props(_conn, material_id)) if row else None
    with db.get_conn(db_path) as conn:
        return get_material(material_id, _conn=conn)


def delete_material(material_id: int, db_path: Path | None = None) -> bool:
    """Hard delete (spec: user can REMOVE materials). History rows cascade."""
    with db.get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT name_en, quantity FROM materials WHERE id = ?", (material_id,)
        ).fetchone()
        if row is None:
            return False
        conn.execute("DELETE FROM materials WHERE id = ?", (material_id,))
    return True


def list_materials(status_filter: Optional[str] = None,
                   text: Optional[str] = None,
                   db_path: Path | None = None) -> list[Material]:
    """List materials with optional derived-status filter and quick text match."""
    with db.get_conn(db_path) as conn:
        rows = conn.execute("SELECT * FROM materials ORDER BY name_en COLLATE NOCASE").fetchall()
        props = {r["material_id"]: r for r in conn.execute("SELECT * FROM properties")}
    out = [_row_to_material(r, props.get(r["id"])) for r in rows]
    if text:
        q = text.strip().lower()
        out = [m for m in out if _text_match(m, q)]
    if status_filter and status_filter != "All":
        out = [m for m in out if m.effective_status == status_filter]
    return out


def available_for_synthesis(db_path: Path | None = None) -> list[Material]:
    """Phase-2 contract (spec 01 §6): Active AND quantity > 0."""
    return [m for m in list_materials(db_path=db_path) if m.is_available]


# --------------------------------------------------------------------------
# Stock & status control (spec 01 §3 — full user control)
# --------------------------------------------------------------------------

def set_quantity(material_id: int, value: float, db_path: Path | None = None,
                 unit: Optional[str] = None) -> Optional[Material]:
    if value < 0:
        raise ValueError("quantity cannot be negative")
    with db.get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT quantity, unit FROM materials WHERE id = ?", (material_id,)
        ).fetchone()
        if row is None:
            return None
        before = float(row["quantity"] or 0)
        new_unit = unit or row["unit"]
        conn.execute(
            "UPDATE materials SET quantity = ?, unit = ?, updated_at = ? WHERE id = ?",
            (float(value), new_unit, utc_now_iso(), material_id),
        )
        _log_history(conn, material_id, "quantity_set",
                     detail=f"{before} -> {value} {new_unit}",
                     qty_before=before, qty_after=float(value))
    return get_material(material_id, db_path=db_path)


def adjust_quantity(material_id: int, delta: float,
                    db_path: Path | None = None) -> Optional[Material]:
    """Increase (+) or decrease (−) the current quantity."""
    with db.get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT quantity FROM materials WHERE id = ?", (material_id,)
        ).fetchone()
        if row is None:
            return None
        before = float(row["quantity"] or 0)
        after = max(0.0, before + float(delta))
        conn.execute(
            "UPDATE materials SET quantity = ?, updated_at = ? WHERE id = ?",
            (after, utc_now_iso(), material_id),
        )
        _log_history(conn, material_id, "quantity_adjusted",
                     detail=f"{before:+.4g} -> {after:.4g} (delta {delta:+.4g})",
                     qty_before=before, qty_after=after)
    return get_material(material_id, db_path=db_path)


def set_status(material_id: int, status: str,
               db_path: Path | None = None) -> Optional[Material]:
    """Enable / completely disable a material (spec 01 §3)."""
    if status not in (STATUS_ACTIVE, STATUS_INACTIVE):
        raise ValueError("status must be 'Active' or 'Inactive'")
    with db.get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT status FROM materials WHERE id = ?", (material_id,)
        ).fetchone()
        if row is None:
            return None
        conn.execute(
            "UPDATE materials SET status = ?, updated_at = ? WHERE id = ?",
            (status, utc_now_iso(), material_id),
        )
        _log_history(conn, material_id, "status_changed",
                     detail=f"{row['status']} -> {status}")
    return get_material(material_id, db_path=db_path)


def get_history(material_id: int, db_path: Path | None = None) -> list[dict]:
    with db.get_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM history WHERE material_id = ? ORDER BY id DESC",
            (material_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# --------------------------------------------------------------------------
# Search (spec 01 §3: name, SMILES, CAS, substructure, similarity)
# --------------------------------------------------------------------------

def _text_match(m: Material, q: str) -> bool:
    hay = " ".join(filter(None, [
        m.name_en, m.name_fa, m.cas, m.smiles, m.inchikey, m.formula,
        " ".join(m.synonyms),
    ])).lower()
    return q in hay


def text_search(query: str, db_path: Path | None = None) -> list[Material]:
    """Case-insensitive match on names (en+fa), synonyms, CAS, SMILES, InChIKey."""
    q = (query or "").strip().lower()
    if not q:
        return []
    return [m for m in list_materials(db_path=db_path) if _text_match(m, q)]


def exact_search(query: str, db_path: Path | None = None) -> list[Material]:
    """Exact match by InChIKey (accepts an InChIKey or anything RDKit can
    convert into one — Molibrary's 'exact' mode)."""
    query = (query or "").strip()
    if not query:
        return []
    if chemistry.is_valid_inchikey(query):
        key = query.upper()
    else:
        key = chemistry.inchikey_from_smiles(query) or ""
        if not key:
            return []
    return [m for m in list_materials(db_path=db_path)
            if (m.inchikey or "").upper() == key]


def substructure_search(query: str, db_path: Path | None = None) -> list[Material]:
    """All materials whose structure contains the query (SMILES or SMARTS)."""
    if not chemistry.HAS_RDKIT or not (query or "").strip():
        return []
    return [m for m in list_materials(db_path=db_path)
            if m.smiles and chemistry.has_substructure(m.smiles, query)]


def similarity_search(query: str, threshold: float = 0.5,
                      db_path: Path | None = None) -> list[tuple[Material, float]]:
    """Tanimoto similarity on Morgan fingerprints, sorted descending."""
    if not chemistry.HAS_RDKIT or not (query or "").strip():
        return []
    fp_q = chemistry.get_fingerprint(query)
    if fp_q is None:
        return []
    from rdkit import DataStructs
    results: list[tuple[Material, float]] = []
    for m in list_materials(db_path=db_path):
        fp = chemistry.get_fingerprint(m.smiles) if m.smiles else None
        if fp is None:
            continue
        sim = DataStructs.TanimotoSimilarity(fp_q, fp)
        if sim >= threshold:
            results.append((m, round(sim, 3)))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def find_by_inchikey(inchikey: str, db_path: Path | None = None) -> Optional[Material]:
    if not inchikey:
        return None
    with db.get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM materials WHERE inchikey = ?", (inchikey,)
        ).fetchone()
        if row is None:
            return None
        return _row_to_material(row, _fetch_props(conn, row["id"]))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        if s.startswith("["):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [str(v).strip() for v in parsed if str(v).strip()]
            except json.JSONDecodeError:
                pass
        return [part.strip() for part in s.split(",") if part.strip()]
    return [str(value)]
