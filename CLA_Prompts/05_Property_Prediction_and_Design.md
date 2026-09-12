# CLA / سیلا - Property Prediction & New Molecule Design

## 1. Property Prediction Module

### Purpose
Predict physicochemical and basic chemical properties of molecules to support decision-making by the virtual chemist.

### Core Capabilities
- Calculate standard RDKit descriptors (MW, LogP, TPSA, HBD, HBA, rotatable bonds, etc.)
- Predict additional properties using machine learning models when available
- Show both calculated and predicted values clearly
- Indicate confidence / uncertainty when possible

### Recommended Properties to Support (Priority Order)
1. Molecular Weight
2. LogP (lipophilicity)
3. Topological Polar Surface Area (TPSA)
4. Hydrogen Bond Donors / Acceptors
5. Number of Rotatable Bonds
6. Melting Point / Boiling Point (if models available)
7. Solubility (approximate)
8. Basic drug-likeness filters (Lipinski, Veber, etc.)

### Technical Approach
- Primary engine: RDKit
- Optional: Pre-trained models (ChemProp, scikit-learn models, or simple neural nets)
- All models must run offline
- Prefer lightweight models due to hardware limitations

### UI Requirements
- Accept molecule via SMILES or structure drawing
- Display results in a clean table
- Support both Persian and English labels
- Allow batch prediction for multiple molecules later

---

## 2. New Molecule Design Module (Advanced)

### Purpose
Suggest new molecules based on user-defined desired properties.

### Current Realistic Scope
This is the most difficult part of the project.  
In the first versions, implement a **simplified** version:

- User specifies desired property ranges (e.g. LogP between 1–3, MW < 400, etc.)
- System searches or generates candidates from:
  - Known building blocks
  - Simple enumeration
  - Existing generative models (if lightweight enough)

### Long-term Vision
- Inverse design using generative models
- Multi-objective optimization
- Synthesizability filtering using the synthesis module
- Safety filtering

### Implementation Priority
- Phase 1: Property filtering + simple suggestion from known chemical space
- Phase 2: Lightweight generative approaches (if hardware allows)
- Phase 3: Full inverse design (future)

### Important Constraints
- Must respect available starting materials when evaluating synthesizability
- Always show that suggestions are computational and need experimental validation
- Keep models as lightweight as possible

## Notes for Coding AI
- Property prediction should be reliable and fast.
- Molecule design should start simple and honest about its limitations.
- Never oversell the generative capabilities.
- Integrate with the synthesis module so suggested molecules can be checked for synthetic accessibility.
