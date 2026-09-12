# CLA / سیلا - Project Overview & Master Specification

## Project Name
- **English**: CLA (Chemistry Lab Assistant)
- **Persian**: سیلا

## Core Vision
Build a **Virtual Chemist** named سیلا (CLA), not a simple assistant.  
The system should reason about synthesis routes, laboratory conditions, safety, property prediction, and new molecule design as close as possible to how an experienced chemist thinks.

### Key Principles
- Aim for the highest possible chemical intelligence.
- Be scientifically honest about limitations and uncertainties.
- Prioritize chemical correctness and safety over convenience.
- Quality of results is more important than speed.
- Completely offline-first.
- Fully bilingual (Persian + English).

## High-Level Architecture

The system consists of two main parts:

1. **Main CLA Application** (Browser-based)
   - Synthesis planning
   - Property prediction
   - New molecule design
   - Safety-aware route presentation
   - Connection to local AI (Ollama)

2. **Starting Materials Manager** (Separate but integrated module)
   - Full control over reagents and building blocks
   - Local database stored inside the project
   - Pre-loaded with common important chemicals

## Mandatory Global Requirements

- Offline by default. Internet only when user explicitly requests updates.
- All data stored locally inside the project folder structure.
- Browser-based graphical interface.
- Full Persian + English support (UI and outputs).
- User must be able to enable/disable any starting material and control its quantity.
- Every synthesis step must include relevant safety information.
- Support for connecting to local LLMs (especially Ollama).
- Designed with weak hardware in mind (old Intel i5, 16GB RAM, weak GPU).
- Prefer longer computation time for higher quality results.
- Maximize reuse of existing high-quality open-source GitHub projects.

## Technology Preferences

- Core chemistry engine: RDKit
- Retrosynthesis foundation: AiZynthFinder
- Starting materials base: Molibrary (chem_db_web) or similar
- Backend: Python (FastAPI preferred, or Flask/Streamlit for faster MVP)
- Frontend: Modern web UI (React preferred, Streamlit acceptable for first versions)
- Local database: SQLite (preferred for simplicity and offline use)
- Local AI: Ollama

## Folder Structure Recommendation

```
CLA/
├── data/
│   ├── starting_materials/
│   ├── models/
│   ├── stocks/
│   └── cache/
├── backend/
├── frontend/
├── modules/
│   ├── synthesis/
│   ├── properties/
│   ├── design/
│   └── safety/
├── local_ai/
└── docs/
```

## Important Notes for the Coding AI
- Never claim the system is a perfect replacement for a human chemist.
- Always show uncertainty and limitations clearly to the user.
- Safety must be integrated into synthesis routes, not treated as an afterthought.
- The Starting Materials Manager must allow full control (add, remove, quantity, enable/disable).
- Design the system to be modular so advanced features can be added later.
