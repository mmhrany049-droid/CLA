# Phase 1 Implementation Notes — Starting Materials Manager

Status: **implemented, tested (22/22), running**. Synthesis work has NOT
been started (per roadmap: "Only after Phase 1 is solid, move to synthesis").

## Roadmap compliance (spec 07, Phase 1)

| Phase-1 task | Status | Where |
|---|---|---|
| Set up project folder structure | ✅ | spec-00 layout: `backend/ frontend/ modules/ local_ai/ data/ docs/ scripts/ tests/ third_party/` |
| Implement/adapt Starting Materials Manager (Molibrary-based) | ✅ | see "Molibrary adaptation" below |
| Pre-load common materials | ✅ | **70 compounds** — all 12 mandated solvents, all mandated acids/bases, reagents & building blocks (`backend/seed/compounds.py`) |
| Create shared SQLite database | ✅ | `data/starting_materials/compounds.db`, spec-06 schema exactly (`backend/db.py`) |
| Basic bilingual support (language switching) | ✅ | full fa/en UI + RTL + persisted choice (`backend/i18n.py`, `backend/settings.py`) |

**Success criterion** ("User can add, edit, enable/disable materials and see
them in a clean web interface") — verified by `tests/test_app_smoke.py::test_ui_add_material_end_to_end`
(add through the real UI) plus backend tests for edit/quantity/status/delete.

## Spec-01 requirement coverage

- §1 Data storage: local SQLite in `data/starting_materials/` ✅; export/import CSV, SDF, JSON ✅ (`backend/io_formats.py`, Transfer page)
- §2 Required fields: all present (spec-06 `materials` table + `properties` table for mp/bp/density/appearance/solubility) ✅
- §3 User controls: add by SMILES/name/CAS/drawing ✅ · edit ✅ · quantity ± and exact set ✅ · Active/Inactive ✅ · complete disable honored by `available_for_synthesis()` ✅ · search by name/SMILES/CAS/substructure/similarity ✅ · 2D structure view ✅
- §4 Pre-loaded defaults: 12 mandated solvents ✅, mandated acids & bases ✅, common reagents/building blocks ✅, bilingual names + GHS + properties ✅
- §5 Technical: RDKit for handling/rendering/search ✅ · JSME editor in browser ✅ · substructure + similarity ✅ · offline ✅ · Molibrary as base ✅ (adapted — see below)
- §6 Integration: main app reads only `status=Active` with quantity > 0 via one function ✅; shared SQLite = changes immediately visible ✅
- §7 UI: clean modern browser UI ✅ · fa+en ✅ · status filters (Active/Inactive/OutOfStock/LowStock) ✅ · visual status badges ✅

## Technology decisions (as confirmed by the project owner)

1. **Streamlit for Phase 1** (fast MVP on weak hardware); backend is
   UI-agnostic so a later FastAPI + React migration only replaces `frontend/`.
2. **Molibrary (chem_db_web) as the base**, adapted to specs 01/06.

## Molibrary adaptation report (honest accounting)

Molibrary is a Flask + RDKit + SQLite compound library (GPL-3.0). We studied
its codebase and **re-implemented its proven patterns natively** inside the
Streamlit architecture with the spec-06 schema (its own schema — name/smiles/
molblock/pdf/notes/author — does not carry bilingual names, CAS, stock, status
or GHS, so a literal fork could not satisfy specs 01/06):

| Taken from Molibrary | Where it lives now |
|---|---|
| RDKit-optional gating (`RDKIT` flag → graceful degradation) | `backend/chemistry.py` (`HAS_RDKIT` / `HAS_RDKIT_DRAW`) |
| Schema-migration approach (`ALTER TABLE` on missing columns) | `backend/db.py::init_db` |
| InChIKey validation regex + "exact search accepts InChIKey or SMILES" | `backend/chemistry.py::INCHIKEY_RE`, `materials.exact_search` |
| Search modes: substructure (`HasSubstructMatch`) + similarity (Morgan r2/2048 + Tanimoto, threshold, sorted) | `backend/materials.py` (modern `rdFingerprintGenerator` API) |
| JSME editor integration concept (offline assets, SMILES ⇄ editor sync) | `streamlit-jsme` component (bundles JSME locally; Apply → SMILES → form) |
| Offline-asset philosophy (setup downloads once, runtime offline) | project-wide (see architecture.md §5) |

No Molibrary source files are redistributed in this repository; attribution
and licensing analysis are in `third_party/ATTRIBUTION.md`.

## Seed-data policy (scientific honesty, spec 00)

- 70 curated common laboratory materials; identifiers computed by RDKit from
  SMILES at seed time (never hand-typed).
- GHS = principal hazard H-codes (not exhaustive SDS replacements); entries
  with uncertain classification carry a "verify against supplier SDS" note.
- Regulated/dual-use precursors (acetic anhydride, thionyl chloride, HCl,
  H₂SO₄, toluene, KMnO₄, benzaldehyde…) carry explicit regulatory notes.
- Quantities are plausible lab defaults, fully editable; seeding is idempotent
  and never touches user-modified rows (re-seed only adds still-missing
  defaults, exposed on the Settings page).
- Known data points were cross-verified externally where memory could err
  (e.g. ethanol InChIKey checked against NIST WebBook — an early test caught a
  mis-remembered constant; RDKit was right).

## Known limitations (honest, per spec 00)

- Runtime light/dark theme switching is not implemented (Streamlit themes are
  config-file based); `theme` is persisted in settings for later.
- Structure drawing requires clicking **Apply** in JSME to transfer SMILES.
- SDF import/export requires RDKit; CSV/JSON work without it.
- On headless Linux without `libxrender1`, 2D rendering is disabled (banner
  shown) — everything else keeps working.
- The AppTest harness cannot navigate multiple pages in one simulated session
  (Streamlit test-framework bug); real runtime navigation is unaffected and
  the preview verifies it.

## Verification evidence

- `python -m pytest tests/` → **22 passed** (schema, CRUD, stock/status +
  history, all 4 search modes, seed completeness/idempotence/bilingualism,
  CSV/JSON/SDF round-trips, settings, i18n, UI renders in both languages,
  UI end-to-end add flow with computed identifiers).
- Live preview: Streamlit server healthy (`/_stcore/health` → ok).

## Next step (awaiting owner confirmation)

Phase 2 — molecule input/visualization, AiZynthFinder integration against
`available_for_synthesis()`, step-by-step routes with mandatory per-step
safety, user controls for depth/time. **Not started.**
