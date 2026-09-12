"""CLA / سیلا — Settings page (spec 06 §4) + database info + About."""

from __future__ import annotations

import streamlit as st

from backend import config, db, i18n, settings
from backend.seed import loader


def render(lang: str) -> None:
    st.title(i18n.t("settings.title", lang))
    current = settings.load_settings()

    # ---------------------------- language ---------------------------------
    new_lang = st.selectbox(
        i18n.t("settings.language", lang),
        options=["fa", "en"],
        index=0 if lang == "fa" else 1,
        format_func=lambda x: "فارسی 🇮🇷" if x == "fa" else "English 🇬🇧",
        key="settings_language",
    )
    if new_lang != lang:
        settings.set_language(new_lang)
        st.session_state["lang"] = new_lang
        st.rerun()

    # ---------------------------- future-phase defaults ---------------------
    with st.expander(i18n.t("settings.future", lang), expanded=False):
        c1, c2, c3 = st.columns(3)
        depth = c1.number_input("default_search_depth",
                                value=int(current.get("default_search_depth", 4)),
                                min_value=1, max_value=50,
                                help="Phase 2 — AiZynthFinder")
        mct = c2.number_input("max_computation_time_s",
                              value=int(current.get("max_computation_time_s", 600)),
                              min_value=10, max_value=86400, step=60,
                              help="Phase 2")
        model = c3.text_input("preferred_local_ai_model",
                              value=str(current.get("preferred_local_ai_model", "")),
                              help="Phase 3 — Ollama (e.g. phi3, qwen2.5:7b)")
        if st.button("💾", key="save_future_settings"):
            settings.save_settings({
                "default_search_depth": depth,
                "max_computation_time_s": mct,
                "preferred_local_ai_model": model.strip(),
            })
            st.rerun()

    # ---------------------------- database info ------------------------------
    st.subheader(i18n.t("settings.db_info", lang))
    stats = db.db_stats()
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric(i18n.t("library.count", lang), stats["materials"])
    m2.metric(i18n.t("status.Active", lang), stats["active"])
    m3.metric(i18n.t("status.LowStock", lang), stats["low_stock"])
    m4.metric(i18n.t("status.OutOfStock", lang), stats["out_of_stock"])
    m5.metric(i18n.t("status.Inactive", lang), stats["inactive"])
    st.caption(f"{i18n.t('settings.db_path', lang)}: `{stats['path']}`  ·  "
               f"{i18n.t('settings.db_size', lang)}: {stats['size_bytes']/1024:.1f} KiB")

    if st.button(i18n.t("settings.reseed", lang), key="reseed_btn"):
        added = loader.seed_if_empty(force_missing=True)
        if added:
            st.success(i18n.t("settings.reseed_done", lang, n=added))
        else:
            st.info(i18n.t("settings.reseed_none", lang))

    # ---------------------------- about --------------------------------------
    st.subheader(i18n.t("settings.about", lang))
    st.info(i18n.t("settings.about_text", lang))
    st.caption(f"{config.APP_NAME_EN} / {config.APP_NAME_FA} — {config.APP_VERSION}")
