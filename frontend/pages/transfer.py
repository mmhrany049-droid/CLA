"""CLA / سیلا — Import / Export page (spec 01 §1: CSV, SDF, JSON;
spec 06: "Make backup and export easy")."""

from __future__ import annotations

import streamlit as st

from backend import chemistry, i18n, io_formats, materials
from frontend import ui_utils


def render(lang: str) -> None:
    st.title(i18n.t("transfer.title", lang))
    st.caption(i18n.t("transfer.backup_note", lang))

    export_col, import_col = st.columns(2, gap="large")

    # ------------------------------ export ---------------------------------
    with export_col:
        st.subheader(i18n.t("transfer.export_all", lang))
        n = len(materials.list_materials())
        st.caption(f"{n} {i18n.t('library.count', lang)}")

        st.download_button(
            i18n.t("transfer.export_csv", lang),
            data=io_formats.export_csv().encode("utf-8-sig"),
            file_name="cla_materials.csv", mime="text/csv",
            width="stretch")
        st.download_button(
            i18n.t("transfer.export_json", lang),
            data=io_formats.export_json().encode("utf-8"),
            file_name="cla_materials.json", mime="application/json",
            width="stretch")
        if chemistry.HAS_RDKIT:
            sdf = io_formats.export_sdf()
            st.download_button(
                i18n.t("transfer.export_sdf", lang),
                data=sdf.encode("utf-8"),
                file_name="cla_materials.sdf", mime="chemical/x-mdl-sdfile",
                width="stretch",
                disabled=not sdf.strip())
        else:
            st.warning(i18n.t("transfer.sdf_needs_rdkit", lang))

    # ------------------------------ import ---------------------------------
    with import_col:
        st.subheader(i18n.t("transfer.import", lang))
        st.caption(i18n.t("transfer.import_hint", lang))
        up = st.file_uploader(i18n.t("transfer.upload", lang),
                              type=["csv", "json", "sdf"], key="import_file")
        if up is None:
            return

        name = up.name.lower()
        try:
            text = up.getvalue().decode("utf-8", errors="replace")
            if name.endswith(".csv"):
                rows = io_formats.parse_csv(text)
            elif name.endswith(".json"):
                rows = io_formats.parse_json(text)
            else:
                if not chemistry.HAS_RDKIT:
                    st.error(i18n.t("transfer.sdf_needs_rdkit", lang))
                    return
                rows = io_formats.parse_sdf(text)
        except Exception as exc:  # noqa: BLE001 — user-facing parse errors
            st.error(i18n.t("error.generic", lang, msg=str(exc)))
            return

        if not rows:
            st.info("0 " + i18n.t("search.results", lang))
            return

        st.markdown(f"**{i18n.t('transfer.preview', lang)}** ({len(rows)})")
        preview = [
            {
                i18n.t("col.name_en", lang): r.get("name_en", ""),
                i18n.t("col.smiles", lang): r.get("smiles", ""),
                i18n.t("col.cas", lang): r.get("cas", ""),
                i18n.t("col.quantity", lang): f"{r.get('quantity', 0):g} {r.get('unit', 'g')}",
            }
            for r in rows[:50]
        ]
        st.dataframe(preview, width="stretch", hide_index=True)

        if st.button(i18n.t("transfer.confirm", lang), type="primary",
                     key="confirm_import"):
            summary = io_formats.import_rows(rows)
            st.success(i18n.t(
                "transfer.imported", lang,
                n=summary["imported"], s=summary["skipped"], e=summary["errors"]))
            ui_utils.toast(i18n.t("transfer.confirm", lang))
