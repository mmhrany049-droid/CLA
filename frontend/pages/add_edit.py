"""CLA / سیلا — Add / Edit material page (spec 01 §2, §3, §5).

Input methods (spec 01 §3): by SMILES, by name/CAS (resolved LOCALLY —
offline-first), or by structure drawing (JSME editor via streamlit-jsme,
which bundles its JavaScript assets locally — no CDN, no internet).
"""

from __future__ import annotations

import streamlit as st

from backend import chemistry, i18n, materials
from frontend import ui_utils

try:
    from streamlit_jsme import st_jsme
    HAS_JSME = True
except ImportError:  # graceful degradation (spec 03)
    HAS_JSME = False


def _jsme_or_none(molecule: str, height: int, key: str):
    """Render the JSME editor; degrade gracefully in runtimes that do not
    support custom components (e.g. Streamlit's AppTest). Returns the drawn
    molecule string or None."""
    if not HAS_JSME:
        return None
    try:
        return st_jsme(molecule=molecule, height=height, key=key)
    except Exception:
        return None


def render(lang: str) -> None:
    edit_id = st.session_state.get("edit_material_id")
    existing = materials.get_material(edit_id) if edit_id else None

    if existing is not None:
        st.title(i18n.t("addedit.title_edit", lang,
                        name=ui_utils.localized_name(existing, lang)))
        if st.button(i18n.t("addedit.cancel_edit", lang)):
            st.session_state.pop("edit_material_id", None)
            st.rerun()
    else:
        st.title(i18n.t("addedit.title_new", lang))

    if not chemistry.HAS_RDKIT:
        st.warning(i18n.t("addedit.no_rdkit", lang))

    uid = f"edit{existing.id}" if existing else "new"

    # ------------------------------------------------------------------
    # Structure input (only when adding new or when editing structure)
    # ------------------------------------------------------------------
    st.subheader(i18n.t("addedit.input_method", lang))
    # SMILES is the default: the JSME editor (~1 MB of JS) is only loaded when
    # the user explicitly asks to draw — friendlier on weak hardware (spec 03).
    method = st.radio(
        "method", horizontal=True, label_visibility="collapsed",
        options=(["smiles", "draw", "lookup"] if HAS_JSME else ["smiles", "lookup"]),
        format_func=lambda x: i18n.t(f"addedit.method_{x}", lang),
        key=f"method_{uid}",
    )

    if method == "draw" and HAS_JSME:
        st.caption(i18n.t("addedit.jsme_hint", lang))
        initial = existing.smiles if existing else st.session_state.get("smiles_input", "")
        drawn = _jsme_or_none(initial or "", 430, f"jsme_{uid}")
        if drawn is None:
            st.info(i18n.t("addedit.editor_unavailable", lang))
        elif drawn != st.session_state.get(f"last_drawn_{uid}"):
            st.session_state[f"last_drawn_{uid}"] = drawn
            st.session_state["smiles_input"] = drawn
            st.rerun()

    elif method == "lookup":
        st.caption(i18n.t("addedit.lookup_hint", lang))
        q = st.text_input(i18n.t("search.query", lang), key=f"lookup_q_{uid}",
                          placeholder="ethanol / اتانول / 64-17-5")
        if q and q.strip():
            hits = materials.text_search(q)[:10]
            if not hits:
                st.info(i18n.t("addedit.lookup_none", lang))
            for h in hits:
                cc1, cc2 = st.columns([5, 1])
                label = f"{h.name_en}" + (f" — {h.name_fa}" if h.name_fa else "")
                label += f"  |  CAS {h.cas}" if h.cas else ""
                if h.smiles:
                    label += f"  |  {h.smiles}"
                cc1.markdown(f"<span class='code-ltr'>{label}</span>",
                             unsafe_allow_html=True)
                if cc2.button(i18n.t("addedit.lookup_use", lang), key=f"use_{h.id}_{uid}"):
                    _prefill_from(h, uid)
                    st.rerun()

    # ------------------------------------------------------------------
    # SMILES + validation
    # ------------------------------------------------------------------
    smiles_key = "smiles_input"
    smiles = st.text_input(
        i18n.t("addedit.smiles_label", lang), key=smiles_key,
        placeholder="CCO",
    )
    if smiles and st.button(i18n.t("addedit.validate", lang), key=f"val_{uid}"):
        ok, msg = chemistry.validate_smiles(smiles)
        if ok:
            st.success(i18n.t("addedit.valid", lang) if msg == "valid"
                       else f"{i18n.t('addedit.valid', lang)} ({msg})")
            ident = chemistry.compute_identifiers(smiles)
            with st.expander(i18n.t("addedit.computed", lang), expanded=True):
                st.json({k: v for k, v in ident.items() if v is not None})
                png = chemistry.render_png(smiles)
                if png:
                    st.image(png, width=300)
            if ident.get("inchikey"):
                dup = materials.find_by_inchikey(ident["inchikey"])
                if dup and (existing is None or dup.id != existing.id):
                    st.warning(i18n.t(
                        "addedit.duplicate_warn", lang,
                        id=dup.id,
                        name=ui_utils.localized_name(dup, lang)))
        else:
            st.error(i18n.t("addedit.invalid", lang))

    # ------------------------------------------------------------------
    # Fields form
    # ------------------------------------------------------------------
    st.divider()
    pre = st.session_state.pop("prefill", {}) if not existing else {}

    def val(field: str, default=None):
        if existing is not None:
            return getattr(existing, field, default)
        return pre.get(field, default)

    with st.form(f"material_form_{uid}"):
        st.markdown(f"**{i18n.t('addedit.section_identity', lang)}**")
        c1, c2, c3 = st.columns(3)
        name_en = c1.text_input(i18n.t("col.name_en", lang) + " *",
                                value=val("name_en", "") or "")
        name_fa = c2.text_input(i18n.t("col.name_fa", lang),
                                value=val("name_fa", "") or "")
        cas = c3.text_input(i18n.t("col.cas", lang), value=val("cas", "") or "")
        synonyms = st.text_input(
            i18n.t("col.synonyms", lang),
            value=", ".join(val("synonyms", []) or []) if not isinstance(val("synonyms", []), str) else val("synonyms", ""))

        st.markdown(f"**{i18n.t('addedit.section_stock', lang)}**")
        s1, s2, s3, s4 = st.columns([1.2, 1, 1.2, 1.4])
        quantity = s1.number_input(i18n.t("col.quantity", lang),
                                   value=float(val("quantity", 0) or 0),
                                   min_value=0.0, step=1.0, format="%.4g")
        unit = s2.selectbox(i18n.t("col.unit", lang), materials.UNITS,
                            index=materials.UNITS.index(val("unit", "g"))
                            if val("unit", "g") in materials.UNITS else 0)
        min_stock = s3.number_input(i18n.t("col.min_stock", lang),
                                    value=float(val("min_stock", 0) or 0),
                                    min_value=0.0, step=1.0, format="%.4g")
        status = s4.selectbox(
            i18n.t("col.status", lang),
            options=[materials.STATUS_ACTIVE, materials.STATUS_INACTIVE],
            format_func=lambda s: i18n.t(f"status.{s}", lang),
            index=0 if val("status", "Active") != materials.STATUS_INACTIVE else 1)

        st.markdown(f"**{i18n.t('addedit.section_safety', lang)}**")
        current_ghs = val("ghs_hazards", []) or []
        g1, g2 = st.columns([2, 1])
        ghs_sel = g1.multiselect(
            i18n.t("addedit.ghs_select", lang),
            options=i18n.known_ghs_codes(),
            default=[c for c in current_ghs if c in i18n.known_ghs_codes()],
            format_func=lambda c: i18n.ghs_label(c, lang))
        ghs_extra = g2.text_input(
            i18n.t("addedit.ghs_custom", lang),
            value=", ".join(c for c in current_ghs if c not in i18n.known_ghs_codes()))

        st.markdown(f"**{i18n.t('addedit.section_props', lang)}**")
        p1, p2, p3 = st.columns(3)
        # value=None keeps "not specified" distinct from a real 0 (e.g. water mp = 0 °C)
        mp = p1.number_input(i18n.t("addedit.mp", lang),
                             value=val("melting_point_c", None), format="%.6g")
        bp = p2.number_input(i18n.t("addedit.bp", lang),
                             value=val("boiling_point_c", None), format="%.6g")
        dens = p3.number_input(i18n.t("addedit.density", lang),
                               value=val("density_g_ml", None), format="%.6g")
        p4, p5 = st.columns(2)
        appearance = p4.text_input(i18n.t("addedit.appearance", lang),
                                   value=val("appearance", "") or "")
        solubility = p5.text_input(i18n.t("addedit.solubility", lang),
                                   value=val("solubility", "") or "")

        notes = st.text_area(i18n.t("library.notes", lang),
                             value=val("notes", "") or "", height=90)

        submitted = st.form_submit_button(i18n.t("addedit.save", lang),
                                          type="primary", width="stretch")

    if submitted:
        if not name_en.strip():
            st.error(i18n.t("addedit.name_required", lang))
            return
        ghs_all = list(ghs_sel) + [c.strip().upper() for c in
                                   ghs_extra.replace(";", ",").split(",") if c.strip()]
        data = {
            "name_en": name_en.strip(),
            "name_fa": name_fa.strip(),
            "smiles": (smiles or "").strip(),
            "cas": cas.strip(),
            "synonyms": materials._as_list(synonyms),
            "quantity": quantity, "unit": unit, "min_stock": min_stock,
            "status": status,
            "ghs_hazards": ghs_all,
            "notes": notes.strip(),
            "melting_point_c": mp,
            "boiling_point_c": bp,
            "density_g_ml": dens,
            "appearance": appearance.strip(),
            "solubility": solubility.strip(),
        }
        if existing is not None:
            m = materials.update_material(existing.id, data)
            ui_utils.toast(i18n.t("addedit.saved_edit", lang, name=m.name_en))
            st.session_state.pop("edit_material_id", None)
        else:
            m = materials.add_material(data)
            ui_utils.toast(i18n.t("addedit.saved_new", lang, name=m.name_en))
            # reset the form for the next entry
            for k in ("smiles_input", f"method_{uid}", f"jsme_{uid}",
                      f"last_drawn_{uid}"):
                st.session_state.pop(k, None)
        st.rerun()


def _prefill_from(m, uid: str) -> None:
    """Copy an existing (library) material's data into the new-material form."""
    st.session_state["smiles_input"] = m.smiles or ""
    st.session_state["prefill"] = {
        "name_en": "", "name_fa": "",           # user re-names the new entry
        "cas": m.cas, "synonyms": m.synonyms,
        "ghs_hazards": m.ghs_hazards,
        "melting_point_c": m.melting_point_c,
        "boiling_point_c": m.boiling_point_c,
        "density_g_ml": m.density_g_ml,
        "appearance": m.appearance,
        "solubility": m.solubility,
        "notes": "",
        "unit": m.unit,
    }
    st.session_state[f"method_{uid}"] = "smiles"
