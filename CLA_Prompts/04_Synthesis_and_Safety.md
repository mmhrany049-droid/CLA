# CLA / سیلا - Synthesis Planning & Safety Module

## Purpose
This module is responsible for generating synthesis routes and integrating safety information into every step.

## Core Goals
- Generate realistic synthesis routes for a target molecule.
- Only use starting materials that are currently **Active** and available.
- Provide clear, step-by-step routes.
- Attach relevant safety information to every step.
- Allow the user to increase search depth and computation time for better quality results.

## Recommended Foundation
- Primary tool: **AiZynthFinder** (https://github.com/MolecularAI/aizynthfinder)
- Supporting chemistry engine: RDKit
- Optional complementary tools: SynPlanner, RetroChem

## Functional Requirements

### 1. Input
- Target molecule can be provided as:
  - SMILES
  - Drawn structure (Ketcher / JSME)
  - Common name (resolved locally if possible)

### 2. Route Generation
- Use only materials marked as Active in the Starting Materials Manager.
- Support multi-step retrosynthesis.
- Allow user controls:
  - Maximum search time
  - Search depth / number of iterations
  - Maximum number of routes to return
  - Preference for shorter routes vs. higher confidence routes

### 3. Output Format for Each Route
Each route must clearly show:
- Step number
- Reaction type / transformation
- Reactants and reagents used
- Conditions (temperature, solvent, catalysts, time) when available
- Expected product of that step
- Confidence / score (if available)

### 4. Safety Integration (Mandatory)
For **every step**, the system must display relevant safety information, including:

- GHS hazard statements (when available)
- Main risks (toxicity, flammability, corrosivity, reactivity, etc.)
- Recommended personal protective equipment (PPE)
- Special laboratory precautions:
  - Need for fume hood
  - Inert atmosphere
  - Temperature control
  - Incompatible materials
  - Risk of gas evolution or exothermic reaction
- Any regulatory or dual-use warnings (if applicable)

Safety information should be presented clearly and prominently, not hidden.

### 5. Limitations & Honesty
- Clearly communicate when a route is speculative.
- Show uncertainty when reaction conditions are estimated rather than taken from real data.
- Never present the system as infallible.

## Technical Implementation Notes

- Prefer running AiZynthFinder in a controlled way that respects hardware limitations.
- Cache results when possible.
- Make long-running searches cancellable by the user.
- Store generated routes locally if the user wants to save them.

## Future Extensions
- Ranking routes by safety score
- Suggesting greener alternatives
- Estimating approximate cost and availability of reagents
- Linking steps to literature precedents (offline cache)

## Notes for Coding AI
- Safety is not optional. Every generated step must include safety context.
- The module must respect the current status of starting materials (Active / Inactive).
- Design for weak hardware: allow the user to trade time for quality.
