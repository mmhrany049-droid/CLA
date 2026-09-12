# CLA / سیلا - Starting Materials Manager Specification

## Purpose
This is a separate but tightly integrated module responsible for managing all laboratory starting materials (reagents, solvents, building blocks).

The main CLA application will only use materials that are marked as **available** in this module.

## Core Requirements

### 1. Data Storage
- All data must be stored locally inside the project (recommended path: `data/starting_materials/`).
- Preferred database: SQLite.
- Support export/import (CSV, SDF, JSON).

### 2. Required Fields for Each Material
- Unique ID
- Name (English + Persian)
- SMILES
- InChI / InChIKey
- Molecular Formula
- Molecular Weight
- CAS Number
- Common synonyms
- Physical properties (melting point, boiling point, density, etc. if available)
- GHS hazard information
- Current quantity
- Unit (g, mL, mol, etc.)
- Minimum stock level
- Status: Active / Inactive / Out of stock
- Notes / Comments
- Date added / last modified

### 3. User Controls (Very Important)
The user must be able to:
- Add new materials (by SMILES, name, CAS, or structure drawing)
- Edit existing materials
- Increase or decrease quantity
- Mark a material as Active or Inactive
- Completely disable a material so it cannot be used in synthesis
- Search by name, SMILES, CAS, substructure, or similarity
- View 2D structure

### 4. Default Pre-loaded Materials
The system must come with a rich set of common and important materials already loaded, including but not limited to:

**Solvents:**
- Water
- Ethanol
- Methanol
- Acetone
- Dichloromethane (DCM)
- Tetrahydrofuran (THF)
- Diethyl ether
- Hexane
- Ethyl acetate
- Acetonitrile
- DMSO
- DMF

**Acids & Bases:**
- Hydrochloric acid
- Sulfuric acid
- Acetic acid
- Sodium hydroxide
- Potassium hydroxide
- Triethylamine
- Sodium carbonate
- etc.

**Common reagents and simple building blocks** should also be included.

### 5. Technical Preferences
- Base project recommendation: Fork and adapt **Molibrary (chem_db_web)**  
  Repository: https://github.com/HiroYokoyama/chem_db_web
- Use RDKit for structure handling, rendering, and search.
- Structure editor in browser (JSME or Ketcher recommended).
- Substructure and similarity search must be supported.
- Completely offline capable.

### 6. Integration with Main CLA
- The main application should only read materials that have `status = Active` and sufficient quantity.
- Changes in the Starting Materials Manager should be immediately visible to the main application (shared database or clear file-based communication).

### 7. UI Requirements
- Clean and modern browser interface.
- Support both Persian and English.
- Easy filtering (Active only, Out of stock, etc.).
- Clear visual indication of material status (Active / Inactive / Low stock).

## Important Notes for Coding AI
- This module is foundational. Build it solidly first.
- Prioritize reliability and ease of control over fancy features.
- Make sure the user has complete power to enable/disable any material.
