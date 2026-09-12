"""CLA / سیلا — Advanced search page (spec 01 §3: name, SMILES, CAS,
substructure, similarity). Structure queries can be drawn with JSME."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from backend import chemistry, i18n, materials
from frontend import ui_utils

try:
    from streamlit_jsme import st_jsme
    HAS_JSME = True
except ImportError:
    HAS_JSME = False


def _jsme_or_none(height: int, key: str):
    """Graceful degradation: custom components may be unavailable in some
    runtimes (e.g. Streamlit AppTest)."""
    if not HAS_JSME:
        return None
    try:
        return st_jsme(molecule="", height=height, key=key)
    except Exception:
        return None

MODE_TEXT = "text"
MODE_EXACT = "exact"
MODE_SUB = "substructure"
MODE_SIM = "similarity"


def render(lang: str) -> None:
    st.title(i18n.t("search.title", lang))

    mode = st.radio(
        i18n.t("search.mode", lang),
        options=[MODE_TEXT, MODE_EXACT, MODE_SUB, MODE_SIM],
        format_func=lambda x: i18n.t(f"search.mode_{x}", lang),
        horizontal=True,
        key="search_mode",
    )

    needs_rdkit = mode in (MODE_SUB, MODE_SIM) or (mode == MODE_EXACT and not
                                                    chemistry.is_valid_inchikey(
                                                        st.session_state.get("sq", "")))
    if mode in (MODE_SUB, MODE_SIM) and not chemistry.HAS_RDKIT:
        st.error(i18n.t("search.needs_rdkit", lang))
        return

    query = ""
    if mode in (MODE_TEXT, MODE_EXACT):
        query = st.text_input(i18n.t("search.query", lang), key="sq",
                              placeholder="اتانول / ethanol / 64-17-5 / CCO / LFQSCWTRJHTGHV-UHFFFAOYSA-N")
    else:
        st.markdown(f"**{i18n.t('search.query_structure', lang)}**")
        q1, q2 = st.columns([2, 3])
        with q1:
            query = st.text_input(i18n.t("addedit.smiles_label", lang), key="sq_struct",
                                  placeholder="c1ccccc1  (benzene ring)")
        with q2:
            if HAS_JSME:
                drawn = _jsme_or_none(300, "jsme_search")
                if drawn and drawn != st.session_state.get("last_jsme_search"):
                    st.session_state["last_jsme_search"] = drawn
                    st.session_state["sq_struct"] = drawn
                    st.rerun()

    threshold = 0.5
    if mode == MODE_SIM:
        threshold = st.slider(i18n.t("search.threshold", lang), 0.1, 1.0, 0.5, 0.05)

    if not st.button(i18n.t("search.run", lang), type="primary", key="run_search"):
        return
    if not (query or "").strip():
        return

    # ------------------------------- run ---------------------------------
    sims: dict[int, float] = {}
    if mode == MODE_TEXT:
        results = materials.text_search(query)
    elif mode == MODE_EXACT:
        results = materials.exact_search(query)
    elif mode == MODE_SUB:
        results = materials.substructure_search(query)
    else:
        pairs = materials.similarity_search(query, threshold=threshold)
        results = [m for m, _ in pairs]
        sims = {m.id: s for m, s in pairs}

    st.caption(f"{len(results)} {i18n.t('search.results', lang)}")
    if not results:
        return

    rows = []
    for m in results:
        r = ui_utils.material_row_for_table(m, lang)
        if mode == MODE_SIM:
            r[i18n.t("col.similarity", lang)] = sims.get(m.id, 0)
        rows.append(r)
    df = pd.DataFrame(rows)

    event = st.dataframe(
        df.drop(columns=["id"]), width="stretch", hide_index=True,
        on_select="rerun", selection_mode="single-row", key="search_table")
    sel = (event.selection.rows or [None])[0] if event and event.selection else None
    if sel is None:
        return

    m = results[sel]
    st.divider()
    c1, c2 = st.columns([1, 3])
    png = chemistry.render_png(m.smiles) if m.smiles else None
    if png is not None:
        c1.image(png, width="stretch")
    with c2:
        st.markdown(f"**{ui_utils.localized_name(m, lang)}** — "
                    f"{ui_utils.status_badge(m, lang)}")
        st.markdown(f"<span class='code-ltr'>CAS: {m.cas or '—'} · "
                    f"{m.formula or '—'} · MW {ui_utils.fmt_num(m.molecular_weight)} · "
                    f"{ui_utils.fmt_qty(m)} · SMILES: {m.smiles or '—'}</span>",
                    unsafe_allow_html=True)
        st.markdown(ui_utils.ghs_html(m, lang), unsafe_allow_html=True)
        if st.button(i18n.t("library.edit", lang), key=f"search_edit_{m.id}"):
            st.session_state["edit_material_id"] = m.id
            st.session_state["nav_page"] = "add_edit"
            st.rerun()
