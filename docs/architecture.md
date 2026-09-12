# CLA / سیلا — Architecture (Phase 1)

## Layering

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Streamlit)  —  app.py → frontend/main.py         │
│  pages: library · add_edit · search · transfer · settings   │
│  ui_utils: RTL/Persian layout, badges, formatters           │
├─────────────────────────────────────────────────────────────┤
│  Backend (pure Python, no UI imports)                        │
│  materials.py  — repository: CRUD, stock & status control,  │
│                  search, Phase-2 gate available_for_synthesis│
│  chemistry.py  — RDKit wrapper (optional-import, graceful)  │
│  db.py         — SQLite schema + connections (WAL)          │
│  io_formats.py — CSV / JSON / SDF import-export             │
│  i18n.py       — fa/en UI strings + GHS H-statement texts   │
│  settings.py   — data/user_settings/settings.json           │
│  seed/         — 70 curated default compounds + loader      │
├─────────────────────────────────────────────────────────────┤
│  Storage (all local, all relative — spec 06)                 │
│  data/starting_materials/compounds.db  (SQLite)             │
│  data/user_settings/settings.json                           │
│  data/{routes,models,stocks,cache}/    (later phases)       │
└─────────────────────────────────────────────────────────────┘
```

## Key design decisions

1. **SMILES is the single source of truth.** InChI, InChIKey, formula and MW
   are always *computed* by RDKit at write time — never hand-typed (prevents
   transcription errors in seed data and user input).

2. **Status semantics.** The stored `status` column holds user intent
   (`Active`/`Inactive`). `OutOfStock` (quantity ≤ 0) and `LowStock`
   (quantity ≤ min_stock) are *derived* at read time. This keeps quantity as
   the single source of truth and guarantees a deliberately disabled material
   can never be silently re-enabled. The spec's three-value status vocabulary
   is preserved in the CHECK constraint and in all UI filters.

3. **Phase 1 → Phase 2 contract.** `backend.materials.available_for_synthesis()`
   is the single function the future synthesis engine (AiZynthFinder) will
   call: it returns only materials with stored status `Active` AND quantity > 0
   (spec 01 §6).

4. **Graceful degradation (spec 03).** RDKit is imported behind a
   `HAS_RDKIT` flag; 2D rendering behind a separate `HAS_RDKIT_DRAW` flag
   (Cairo drawing needs extra system libs on Linux). JSME editor rendering is
   guarded too. The app always runs; chemistry-powered features light up when
   their dependencies are present.

5. **Offline-first enforcement.** No network calls anywhere in the codebase.
   Streamlit telemetry is disabled in `.streamlit/config.toml`; JSME assets
   ship inside the `streamlit-jsme` wheel (no CDN); name/CAS resolution is
   local-database-only.

6. **Short-lived SQLite connections + WAL.** Streamlit reruns the script on
   every interaction; connections open per operation with WAL journaling and
   foreign keys enabled. Timestamps are ISO-8601 UTC strings.

7. **Bilingual by construction.** Every UI string goes through
   `i18n.t(key, lang)`; the database stores `name_en` + `name_fa` side by
   side; GHS H-codes are stored as codes and rendered with localized
   statements; Persian gets a real RTL CSS layout with LTR-isolated technical
   content (SMILES, InChIKey, numbers).

8. **History log.** Every create/edit/quantity-change/status-change is written
   to the `history` table (spec 06's optional table) — auditability for lab
   stock management.

## Data flow (add material)

```
UI form (SMILES | JSME drawing | local name/CAS lookup)
      → materials.add_material(data)
          → chemistry.compute_identifiers(smiles)   [canonical SMILES, InChI,
                                                     InChIKey, formula, MW]
          → INSERT materials (+ properties row)
          → INSERT history('created')
      → UI re-renders library from SQLite (single source of truth)
```

## Migration path to FastAPI + React (later, if desired)

The backend layer has **zero Streamlit imports** — `backend/` can be exposed
as a FastAPI service unchanged; only `frontend/` would be replaced. The SQLite
schema is the spec-06 schema, so no data migration is needed.
