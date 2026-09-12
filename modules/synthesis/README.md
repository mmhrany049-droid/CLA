# Synthesis Module — PLACEHOLDER (Phase 2)

Per the Development Roadmap (`CLA_Prompts/07_Development_Roadmap_and_Priorities.md`),
this module is **not** implemented in Phase 1.

Phase 2 will add here:

- AiZynthFinder integration (route generation) — spec `04_Synthesis_and_Safety.md`
- Route generation **only** from starting materials with effective status
  `Active` and quantity > 0, consumed via
  `backend.materials.available_for_synthesis()` (already implemented in Phase 1 —
  that function is the Phase-1→Phase-2 contract).
- User controls: max search time, depth/iterations, number of routes,
  cancellable searches (spec 03).
- Step-by-step route display with confidence scores (spec 04 §3).

**Safety is mandatory in every step** (spec 04 §4) — implemented together with
`modules/safety/`, never as an afterthought.
