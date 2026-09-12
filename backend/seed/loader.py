"""CLA / سیلا — seed loader: pre-loads the default materials (spec 01 §4).

Idempotent: a compound is inserted only when no existing row shares its
InChIKey (when RDKit computed one) or its English name. Existing user data
is never modified or deleted.
"""

from __future__ import annotations

from pathlib import Path

from backend import chemistry, db, materials
from backend.seed.compounds import SEED_COMPOUNDS


def _existing_keys(conn) -> set[str]:
    names = {r["name_en"].strip().lower() for r in conn.execute("SELECT name_en FROM materials")}
    keys = {r["inchikey"] for r in conn.execute("SELECT inchikey FROM materials") if r["inchikey"]}
    return names | keys


def seed_if_empty(db_path: Path | None = None, force_missing: bool = True) -> int:
    """Seed the database. Returns the number of inserted compounds.

    * First run: inserts the full default library.
    * Later runs (``force_missing=True``): inserts only defaults that are
      still absent — safe to call on every app start (Settings page also
      exposes this as an explicit action).
    """
    db.init_db(db_path)
    inserted = 0
    with db.get_conn(db_path) as conn:
        seen = _existing_keys(conn)
    for entry in SEED_COMPOUNDS:
        name_key = entry["en"].strip().lower()
        inchikey = ""
        if entry.get("smi") and chemistry.HAS_RDKIT:
            inchikey = chemistry.inchikey_from_smiles(entry["smi"]) or ""
        if name_key in seen or (inchikey and inchikey in seen):
            continue
        data = {
            "name_en": entry["en"],
            "name_fa": entry.get("fa", ""),
            "smiles": entry.get("smi", ""),
            "cas": entry.get("cas", ""),
            "synonyms": entry.get("syn", []),
            "ghs_hazards": entry.get("ghs", []),
            "quantity": entry.get("qty", 0),
            "unit": entry.get("unit", "g"),
            "min_stock": entry.get("min", 0),
            "status": materials.STATUS_ACTIVE,
            "notes": entry.get("notes", ""),
            "melting_point_c": entry.get("mp"),
            "boiling_point_c": entry.get("bp"),
            "density_g_ml": entry.get("d"),
            "appearance": entry.get("app", ""),
        }
        try:
            materials.add_material(data, db_path=db_path, action="reseeded"
                                   if not force_missing else "created")
            inserted += 1
            if name_key:
                seen.add(name_key)
            if inchikey:
                seen.add(inchikey)
        except Exception:
            # Never let one bad seed entry break startup (spec 03: graceful)
            continue
    return inserted


def seed_count() -> int:
    return len(SEED_COMPOUNDS)
