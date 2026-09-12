# Safety Module — PLACEHOLDER (Phase 2)

Per the Development Roadmap, safety integration ships together with synthesis
in Phase 2 — spec `04_Synthesis_and_Safety.md` §4 (mandatory):

- GHS hazard statements per step (Phase 1 already stores GHS H-codes per
  material in the database and renders them bilingually via
  `backend/i18n.py::GHS_H_STATEMENTS`)
- Main risks: toxicity, flammability, corrosivity, reactivity
- Recommended PPE
- Special precautions: fume hood, inert atmosphere, temperature control,
  incompatible materials, gas evolution / exotherm risk
- Regulatory / dual-use warnings where applicable (Phase 1 seed data already
  flags regulated precursors in material notes)

Safety information must be presented clearly and prominently — never hidden.
