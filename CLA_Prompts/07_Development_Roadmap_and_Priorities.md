# CLA / سیلا - Development Roadmap & Priorities

## Overall Strategy
Build the system step by step, starting from the most foundational and reliable parts.  
Always keep the offline-first and weak-hardware constraints in mind.

---

## Phase 1: Foundation (Highest Priority)

### Goals
- Establish solid project structure
- Create working Starting Materials Manager
- Make the main application able to read available materials

### Tasks
1. Set up project folder structure
2. Implement / adapt Starting Materials Manager (based on Molibrary or similar)
3. Pre-load common materials (water, ethanol, solvents, acids, bases...)
4. Create shared SQLite database
5. Basic bilingual support (at least language switching)

**Success Criteria:**  
User can add, edit, enable/disable materials and see them in a clean web interface.

---

## Phase 2: Core Virtual Chemist Capabilities

### Goals
- Molecule input and visualization
- Basic synthesis route generation
- Safety information attached to steps

### Tasks
1. Integrate RDKit for molecule handling
2. Integrate AiZynthFinder
3. Connect synthesis engine to Active starting materials only
4. Display routes step-by-step
5. Add safety information to each step
6. Add user controls for search depth and time

**Success Criteria:**  
User can input a molecule and receive synthesis routes that respect available materials and include safety notes.

---

## Phase 3: Intelligence Layer

### Goals
- Connect local AI (Ollama)
- Improve explanations and reasoning
- Add property prediction

### Tasks
1. Integrate Ollama API
2. Use local AI to explain routes in Persian and English
3. Implement basic property prediction (RDKit + simple models)
4. Allow user to choose local model

---

## Phase 4: Advanced Features

### Goals
- New molecule design (simplified first)
- Better route ranking
- Saving and managing previous routes
- Performance optimizations

### Tasks
1. Simple property-based molecule suggestion
2. Route saving and history
3. Improved UI/UX
4. Export capabilities
5. Optional internet update system (user-triggered only)

---

## Phase 5: Polish & Expansion (Future)

- Stronger generative design
- Better kinetics / condition prediction
- Advanced safety scoring
- Multi-user support (if needed)
- Mobile-friendly interface

---

## Development Principles

1. **Quality > Speed** — Allow longer computation for better results.
2. **Offline First** — Everything must work without internet.
3. **Modular** — Each part should be independently improvable.
4. **Honest** — Always communicate limitations.
5. **Hardware Aware** — Design for old i5 + 16GB RAM.
6. **User Control** — User must control materials, depth, and time.

---

## Recommended Starting Point for Coding AI

Begin with **Phase 1**.  
First deliverable should be a working Starting Materials Manager with pre-loaded common chemicals and full control (add / edit / quantity / active-inactive).

Only after Phase 1 is solid, move to synthesis integration.
