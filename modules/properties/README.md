# Property Prediction Module — PLACEHOLDER (Phase 3)

Per the Development Roadmap (Phase 3) and spec `05_Property_Prediction_and_Design.md`:

- RDKit descriptors first: MW, LogP, TPSA, HBD/HBA, rotatable bonds
  (`backend/chemistry.py` from Phase 1 is the place this will build on)
- Then melting/boiling point, approximate solubility, drug-likeness filters
  (Lipinski, Veber) with lightweight offline models
- Calculated vs predicted values clearly distinguished; uncertainty shown
- All models run offline, stored under `data/models/`
