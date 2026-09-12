# New Molecule Design Module — PLACEHOLDER (Phase 4+)

Per the Development Roadmap (Phase 4) and spec `05_Property_Prediction_and_Design.md` §2:

- Start simplified and honest: user gives desired property ranges
  (e.g. LogP 1–3, MW < 400); candidates from known building blocks /
  simple enumeration / lightweight generative models only
- Synthesizability checks must respect the Starting Materials Manager
  (active stock) via `modules/synthesis/`
- Every suggestion must state that it is computational and requires
  experimental validation — never oversell generative capabilities
- Full inverse design is long-term (Phase 5)
