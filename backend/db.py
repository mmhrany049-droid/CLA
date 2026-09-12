"""CLA / سیلا — SQLite database layer (spec 06: Data Structures & Storage).

Schema notes
------------
* ``materials``  — main table, exactly the columns suggested in spec 06.
* ``properties`` — optional extra physical properties (spec 06 §1).
* ``history``    — quantity/status change log (spec 06 §1, "history" table).

Status semantics (documented decision, see docs/phase1_notes.md):
    The stored ``status`` column holds the USER INTENT: 'Active' or 'Inactive'.
    'OutOfStock' and 'LowStock' are *derived* states computed from quantity
    (quantity <= 0  ->  OutOfStock;  quantity <= min_stock  ->  LowStock),
    so the quantity field stays the single source of truth and a material the
    user deliberately disabled can never be silently re-enabled.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from backend import config

SCHEMA_VERSION = 1

_DDL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS materials (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en          TEXT NOT NULL,
    name_fa          TEXT,
    smiles           TEXT,
    inchi            TEXT,
    inchikey         TEXT,
    formula          TEXT,
    molecular_weight REAL,
    cas              TEXT,
    synonyms         TEXT NOT NULL DEFAULT '[]',   -- JSON list
    quantity         REAL NOT NULL DEFAULT 0,
    unit             TEXT NOT NULL DEFAULT 'g',
    min_stock        REAL NOT NULL DEFAULT 0,
    status           TEXT NOT NULL DEFAULT 'Active'
                     CHECK (status IN ('Active', 'Inactive', 'OutOfStock')),
    ghs_hazards      TEXT NOT NULL DEFAULT '[]',   -- JSON list of H-codes
    notes            TEXT NOT NULL DEFAULT '',
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_materials_name_en   ON materials (name_en);
CREATE INDEX IF NOT EXISTS idx_materials_inchikey  ON materials (inchikey);
CREATE INDEX IF NOT EXISTS idx_materials_status    ON materials (status);
CREATE INDEX IF NOT EXISTS idx_materials_cas       ON materials (cas);

CREATE TABLE IF NOT EXISTS properties (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id      INTEGER NOT NULL UNIQUE
                     REFERENCES materials (id) ON DELETE CASCADE,
    melting_point_c  REAL,
    boiling_point_c  REAL,
    density_g_ml     REAL,
    appearance       TEXT,
    solubility       TEXT,
    extra            TEXT NOT NULL DEFAULT '{}'    -- JSON, future fields
);

CREATE TABLE IF NOT EXISTS history (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id      INTEGER NOT NULL
                     REFERENCES materials (id) ON DELETE CASCADE,
    action           TEXT NOT NULL,   -- created/edited/quantity_set/quantity_adjusted/
                                      -- status_changed/deleted/imported/reseeded
    detail           TEXT NOT NULL DEFAULT '',
    quantity_before  REAL,
    quantity_after   REAL,
    created_at       TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_history_material ON history (material_id);

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

# Column-existence migrations (pattern adapted from Molibrary's init_db,
# see third_party/ATTRIBUTION.md): new columns are added via ALTER TABLE
# when missing, so old databases keep working after upgrades.
_EXPECTED_COLUMNS = {
    "materials": [
        ("id", "INTEGER"), ("name_en", "TEXT"), ("name_fa", "TEXT"),
        ("smiles", "TEXT"), ("inchi", "TEXT"), ("inchikey", "TEXT"),
        ("formula", "TEXT"), ("molecular_weight", "REAL"), ("cas", "TEXT"),
        ("synonyms", "TEXT"), ("quantity", "REAL"), ("unit", "TEXT"),
        ("min_stock", "REAL"), ("status", "TEXT"), ("ghs_hazards", "TEXT"),
        ("notes", "TEXT"), ("created_at", "TEXT"), ("updated_at", "TEXT"),
    ],
}


def utc_now_iso() -> str:
    """Timestamps are stored as ISO-8601 UTC strings."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def get_conn(db_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    """Short-lived connection per operation (safe for Streamlit reruns)."""
    config.ensure_data_dirs()
    path = db_path or config.DB_PATH
    conn = sqlite3.connect(str(path), timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: Path | None = None) -> Path:
    """Create schema if needed; idempotent. Returns the database path."""
    path = db_path or config.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with get_conn(path) as conn:
        conn.executescript(_DDL)
        # Migrations: add missing columns to pre-existing tables
        for table, cols in _EXPECTED_COLUMNS.items():
            existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
            for name, typ in cols:
                if name not in existing:
                    conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {typ}")
        conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )
    return path


def db_stats(db_path: Path | None = None) -> dict:
    """Basic counts + file size, shown on the Settings page."""
    path = db_path or config.DB_PATH
    stats = {"path": str(path), "exists": path.exists(), "size_bytes": 0,
             "materials": 0, "active": 0, "inactive": 0, "out_of_stock": 0,
             "low_stock": 0}
    if not path.exists():
        return stats
    stats["size_bytes"] = path.stat().st_size
    with get_conn(path) as conn:
        stats["materials"] = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        rows = conn.execute(
            "SELECT status, quantity, min_stock FROM materials"
        ).fetchall()
    for r in rows:
        if r["status"] == "Inactive":
            stats["inactive"] += 1
        elif (r["quantity"] or 0) <= 0:
            stats["out_of_stock"] += 1
        elif (r["quantity"] or 0) <= (r["min_stock"] or 0):
            stats["low_stock"] += 1
        else:
            stats["active"] += 1
    return stats
