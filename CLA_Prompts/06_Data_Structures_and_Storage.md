# CLA / سیلا - Data Structures & Local Storage

## Core Principle
Everything must be stored locally inside the project.  
No mandatory cloud or external database.

## Recommended Root Data Folder
```
CLA/
└── data/
    ├── starting_materials/
    ├── routes/
    ├── models/
    ├── stocks/
    ├── cache/
    └── user_settings/
```

---

## 1. Starting Materials Database

**Preferred format:** SQLite  
**Location:** `data/starting_materials/compounds.db`

### Suggested Main Table: `materials`

| Column              | Type          | Description                              |
|---------------------|---------------|------------------------------------------|
| id                  | INTEGER PK    | Unique ID                                |
| name_en             | TEXT          | English name                             |
| name_fa             | TEXT          | Persian name                             |
| smiles              | TEXT          | Canonical SMILES                         |
| inchi               | TEXT          | InChI                                    |
| inchikey            | TEXT          | InChIKey                                 |
| formula             | TEXT          | Molecular formula                        |
| molecular_weight    | REAL          | MW                                       |
| cas                 | TEXT          | CAS number                               |
| synonyms            | TEXT          | JSON or comma-separated                  |
| quantity            | REAL          | Current quantity                         |
| unit                | TEXT          | g, mL, mol, etc.                         |
| min_stock           | REAL          | Minimum stock level                      |
| status              | TEXT          | Active / Inactive / OutOfStock           |
| ghs_hazards         | TEXT          | JSON list of hazards                     |
| notes               | TEXT          | Free text notes                          |
| created_at          | TIMESTAMP     |                                          |
| updated_at          | TIMESTAMP     |                                          |

### Additional Tables (Optional)
- `properties` (extra physical properties)
- `suppliers` (if needed later)
- `history` (quantity change log)

---

## 2. Synthesis Routes Storage

**Location:** `data/routes/`  
**Format:** JSON files or SQLite

Each saved route should contain:
- Target molecule
- Full step-by-step route
- Materials used
- Safety information per step
- Score / confidence
- Timestamp
- User notes

---

## 3. Models & Stocks

- `data/models/` → Local AI models or property prediction models
- `data/stocks/` → AiZynthFinder stock files and related data
- `data/cache/` → Temporary calculation results

---

## 4. User Settings

**Location:** `data/user_settings/settings.json`

Suggested settings:
- Language (fa / en)
- Default search depth
- Maximum computation time
- Preferred local AI model
- Theme (light / dark)
- Safety display level

---

## Rules for Coding AI
- Always use relative paths inside the project.
- Prefer SQLite for structured data.
- Make backup and export easy.
- Never hard-code absolute paths.
- Design so the entire `data/` folder can be copied to another machine and work offline.
