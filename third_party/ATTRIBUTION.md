# Third-Party Attribution & Licensing

CLA / سیلا builds on excellent open-source work. This file records what is
used, how, and under which license — kept honest per the project's principles.

## Molibrary (chem_db_web)

- **Project**: https://github.com/HiroYokoyama/chem_db_web — "Molibrary",
  a local chemical structure & protocol database (Flask + RDKit + SQLite + JSME).
- **License**: GPL-3.0.
- **How used**: as the *design base* for the Starting Materials Manager, per
  spec 01 §5 ("Fork and adapt Molibrary … or similar") and the owner's
  decision. Its architecture and algorithms were studied and equivalent
  functionality was **re-implemented natively** for the Streamlit stack with
  the spec-06 database schema (see `docs/phase1_notes.md` for the exact
  pattern-by-pattern mapping). **No Molibrary source files are copied or
  redistributed in this repository.**
- **Licensing note**: because the specifications direct deriving the design
  from a GPL-3.0 project, if CLA is ever *distributed*, a conservative reading
  is that derivative parts should remain GPL-3.0-compatible. For personal,
  offline use (the project's actual deployment model) there is no practical
  constraint. The project owner should choose the repository license with this
  in mind; this note is not legal advice.

## JSME Molecular Editor

- **Project**: https://jsme-editor.github.io/ — JSME, by Peter Ertl
  (developed at Novartis).
- **License/terms**: distributed free of charge for use in web applications;
  see the official site for terms. The editor's JavaScript assets (GWT build)
  are redistributed inside the `streamlit-jsme` Python package (not in this
  repository's source tree).
- **How used**: in-browser 2D structure drawing for adding materials and
  structure queries — loaded entirely from local package assets, never a CDN
  (offline-first compliance).

## streamlit-jsme

- **Project**: https://pypi.org/project/streamlit-jsme/ — Streamlit V2 custom
  component wrapping JSME (by Chanin Nantasenamat).
- **License**: MIT.
- **How used**: `st_jsme()` on the Add/Edit and Search pages; bundles the
  JSME assets locally, so no internet is needed at runtime.

## RDKit

- **Project**: https://www.rdkit.org/ — RDKit cheminformatics toolkit.
- **License**: BSD-3-Clause (permissive).
- **How used**: SMILES validation/canonicalization, InChI/InChIKey/formula/MW
  computation, 2D PNG rendering, substructure matching, Morgan fingerprints +
  Tanimoto similarity, SDF handling. Imported behind availability flags so the
  app degrades gracefully without it.

## Streamlit

- **Project**: https://streamlit.io/
- **License**: Apache-2.0.
- **How used**: Phase-1 web framework. Telemetry/usage stats are **disabled**
  in `.streamlit/config.toml` (offline-first compliance).

## pandas

- **License**: BSD-3-Clause. Used for table rendering in the UI layer.
