# CLA / سیلا - Main Application Specification

## Purpose
This is the core browser-based application of سیلا (CLA).  
It serves as the main interface where the user interacts with the Virtual Chemist.

## Core Modules

### 1. Synthesis Planning Module
- Accept a target molecule (SMILES, name, or drawn structure).
- Generate possible synthesis routes using available starting materials only.
- Preferred foundation: AiZynthFinder.
- Allow user to control search depth and maximum computation time (quality over speed).
- Display routes in a clear, step-by-step manner.

### 2. Safety Integration (Mandatory)
For every step in a synthesis route, the system must show:
- Relevant GHS hazards
- Required personal protective equipment (PPE)
- Special precautions (e.g. inert atmosphere, temperature control, incompatible materials)
- Potential risks (toxic gases, exothermic reaction, etc.)

### 3. Property Prediction Module
- Predict basic physicochemical properties of molecules.
- Use RDKit descriptors + machine learning models where possible.
- Show uncertainty when applicable.

### 4. New Molecule Design Module
- Accept desired properties from the user.
- Suggest candidate molecules.
- This is the most advanced and difficult module (implement later or in simplified form first).

### 5. Local AI Connection
- Ability to connect to a local LLM (via Ollama recommended).
- Use the local AI for:
  - Explaining routes in natural language (Persian or English)
  - Reasoning about alternative strategies
  - Answering chemistry questions in context of the current molecule/route

## Technical Requirements

- Completely offline by default.
- Browser-based UI.
- Full bilingual support (Persian + English).
- Must read the Starting Materials database and only use Active materials.
- Designed to run on weak hardware (old i5 + 16GB RAM).
- Prefer modular architecture.

## Recommended Technology Stack

- Backend: FastAPI (preferred) or Flask
- Chemistry: RDKit + AiZynthFinder
- Frontend: React (preferred) or Streamlit for faster development
- Database access: Shared SQLite with Starting Materials Manager
- Local AI: Ollama API

## UI/UX Guidelines

- Clean, professional, chemistry-oriented interface.
- Clear separation between different modules.
- Always show when the system is working offline.
- Provide controls for increasing search depth / computation time.
- Display safety information prominently in synthesis routes.

## Development Priority Order

1. Connect to Starting Materials Manager and display available materials.
2. Basic molecule input and visualization.
3. Integration with AiZynthFinder for route generation.
4. Add safety information to each step.
5. Bilingual support.
6. Local AI connection.
7. Property prediction and molecule design (later stages).

## Important Notes for Coding AI
- Never hide limitations. Always communicate uncertainty.
- Safety information is not optional.
- The system should feel like a knowledgeable chemist, not a simple tool.
- Keep the code modular so each part can be improved independently.
