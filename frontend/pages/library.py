"""CLA / سیلا — Materials Library page (browse + full user control, spec 01 §3)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from backend import i18n, materials
from backend.materials import (STATUS_ACTIVE, STATUS_INACTIVE,
                               STATUS_LOW_STOCK, STATUS_OUT_OF_STOCK)
from frontend import ui_utils


def render(lang: str) -> None:
    st.title(i18n.t("library.title", lang))

    # ------------------------- filters ------------------------------------
    c1, c2 = st.columns([1, 2])
    with c1:
        status_opts = ["All", STATUS_ACTIVE, STATUS_INACTIVE,
                       STATUS_OUT_OF_STOCK, STATUS_LOW_STOCK]
        status_filter = st.selectbox(
            i18n.t("library.filter_status", lang),
            options=status_opts,
            format_func=lambda s: i18n.t(f"status.{s}", lang),
        )
    with c2:
        quick = st.text_input(i18n.t("library.quick_search", lang),
                              placeholder="H2O / 64-17-5 / اتانول / CCO …")

    rows = materials.list_materials(status_filter=status_filter, text=quick or None)
    st.caption(f"{len(rows)} {i18n.t('library.count', lang)}")

    if not rows:
        st.info(i18n.t("search.results", lang) + ": 0")
        return

    # ------------------------- table --------------------------------------
    df = pd.DataFrame([ui_utils.material_row_for_table(m, lang) for m in rows])
    id_to_material = {m.id: m for m in rows}
    event = st.dataframe(
        df.drop(columns=["id"]),
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="library_table",
    )

    sel_idx = (event.selection.rows or [None])[0] if event and event.selection else None
    if sel_idx is None:
        st.caption(i18n.t("library.select_hint", lang))
        return

    # map dataframe row -> material (dataframe keeps the same order as rows)
    m = id_to_material[df.iloc[sel_idx]["id"]]
    _render_detail(m, lang)


# ---------------------------------------------------------------------------

def _render_detail(m, lang: str) -> None:
    st.divider()
    st.subheader(f"{i18n.t('library.details', lang)} — {ui_utils.localized_name(m, lang)}")

    left, right = st.columns([2, 3], gap="large")

    with left:
        # 2D structure (spec 01 §3)
        st.markdown(f"**{i18n.t('library.structure', lang)}**")
        png = None
        if m.smiles:
            from backend import chemistry
            png = chemistry.render_png(m.smiles)
        if png is not None:
            st.image(png, width="stretch")
        else:
            st.caption(i18n.t("library.no_structure", lang))
            if m.smiles:
                st.code(m.smiles)

        # GHS (spec 00: safety integrated everywhere)
        st.markdown(f"**{i18n.t('library.ghs', lang)}**")
        st.markdown(ui_utils.ghs_html(m, lang), unsafe_allow_html=True)

        if m.notes:
            st.markdown(f"**{i18n.t('library.notes', lang)}**")
            st.warning(m.notes)

    with right:
        st.markdown(f"**{i18n.t('col.status', lang)}:** {ui_utils.status_badge(m, lang)}")
        cols = st.columns(2)
        fields = {
            i18n.t("col.name_en", lang): m.name_en or "—",
            i18n.t("col.name_fa", lang): m.name_fa or "—",
            i18n.t("col.cas", lang): m.cas or "—",
            i18n.t("col.formula", lang): m.formula or "—",
            i18n.t("col.mw", lang): ui_utils.fmt_num(m.molecular_weight),
            i18n.t("col.inchikey", lang): m.inchikey or "—",
            i18n.t("col.smiles", lang): m.smiles or "—",
            i18n.t("col.synonyms", lang): ", ".join(m.synonyms) or "—",
            i18n.t("col.quantity", lang): ui_utils.fmt_qty(m),
            i18n.t("col.min_stock", lang): f"{m.min_stock:g} {m.unit}",
            i18n.t("col.created_at", lang): (m.created_at or "—")[:19],
            i18n.t("col.updated_at", lang): (m.updated_at or "—")[:19],
        }
        for i, (k, v) in enumerate(fields.items()):
            with cols[i % 2]:
                st.markdown(f"<span class='code-ltr'>**{k}:** {v}</span>",
                            unsafe_allow_html=True)

        # physical properties (spec 01 §2)
        props = [
            (i18n.t("addedit.mp", lang), m.melting_point_c),
            (i18n.t("addedit.bp", lang), m.boiling_point_c),
            (i18n.t("addedit.density", lang), m.density_g_ml),
        ]
        props = [(k, v) for k, v in props if v is not None]
        if props or m.appearance:
            st.markdown(f"**{i18n.t('library.properties', lang)}**")
            st.markdown(
                " · ".join(
                    [f"{k}: {ui_utils.fmt_num(v)}" for k, v in props]
                    + ([m.appearance] if m.appearance else [])
                )
            )

    # ------------------------- stock control (spec 01 §3) ------------------
    st.divider()
    st.markdown(f"**{i18n.t('library.stock_control', lang)}**")
    if m.status == STATUS_INACTIVE:
        st.error(i18n.t("library.status_note_disabled", lang))

    a, b, c = st.columns([2, 2, 1.4], gap="medium")

    with a:
        with st.form("adjust_qty", clear_on_submit=True):
            st.markdown(i18n.t("library.adjust_delta", lang))
            delta = st.number_input(
                "Δ", value=0.0, step=1.0, format="%.4g",
                help="+ increase / − decrease", label_visibility="collapsed",
            )
            if st.form_submit_button(i18n.t("library.apply_delta", lang),
                                     width="stretch"):
                materials.adjust_quantity(m.id, delta)
                ui_utils.toast(i18n.t("library.saved_qty", lang))
                st.rerun()

    with b:
        with st.form("set_qty"):
            st.markdown(i18n.t("library.set_quantity", lang))
            exact = st.number_input(
                "Q", value=float(m.quantity), min_value=0.0, step=1.0,
                format="%.4g", label_visibility="collapsed",
            )
            unit = st.selectbox(i18n.t("col.unit", lang), materials.UNITS,
                                index=materials.UNITS.index(m.unit)
                                if m.unit in materials.UNITS else 0)
            if st.form_submit_button(i18n.t("col.quantity", lang) + " ⏎",
                                     width="stretch"):
                materials.set_quantity(m.id, exact, unit=unit)
                ui_utils.toast(i18n.t("library.saved_qty", lang))
                st.rerun()

    with c:
        st.markdown(i18n.t("col.status", lang))
        if m.status == STATUS_ACTIVE:
            if st.button(i18n.t("library.disable", lang), width="stretch"):
                materials.set_status(m.id, STATUS_INACTIVE)
                ui_utils.toast(i18n.t("library.saved_status", lang))
                st.rerun()
        else:
            if st.button(i18n.t("library.enable", lang), width="stretch"):
                materials.set_status(m.id, STATUS_ACTIVE)
                ui_utils.toast(i18n.t("library.saved_status", lang))
                st.rerun()

        if st.button(i18n.t("library.edit", lang), width="stretch"):
            st.session_state["edit_material_id"] = m.id
            st.session_state["nav_page"] = "add_edit"
            st.rerun()

    # ------------------------- delete (with confirmation) ------------------
    with st.expander(i18n.t("library.delete", lang), expanded=False):
        confirm = st.checkbox(i18n.t("library.delete_confirm", lang), key=f"del_confirm_{m.id}")
        if st.button(i18n.t("library.delete", lang), disabled=not confirm,
                     type="primary", key=f"del_btn_{m.id}"):
            name = ui_utils.localized_name(m, lang)
            materials.delete_material(m.id)
            ui_utils.toast(i18n.t("library.deleted", lang, name=name))
            st.rerun()

    # ------------------------- history --------------------------------------
    with st.expander(i18n.t("library.history", lang), expanded=False):
        hist = materials.get_history(m.id)
        if hist:
            hdf = pd.DataFrame(hist)[["created_at", "action", "detail",
                                      "quantity_before", "quantity_after"]]
            st.dataframe(hdf, width="stretch", hide_index=True)
        else:
            st.caption("—")
