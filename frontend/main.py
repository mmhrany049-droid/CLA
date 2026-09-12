"""CLA / سیلا — Streamlit app shell: sidebar navigation + language switch."""

from __future__ import annotations

import streamlit as st

from backend import config, db, i18n, settings
from backend.chemistry import HAS_RDKIT, rdkit_status_message
from backend.seed import loader
from frontend import ui_utils
from frontend.pages import add_edit, library, search, settings_page, transfer


def _bootstrap() -> str:
    """First-run: create data dirs, DB schema, seed defaults. Returns language."""
    config.ensure_data_dirs()
    db.init_db()
    with db.get_conn() as conn:
        count = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    if count == 0:
        loader.seed_if_empty()
    s = settings.load_settings()
    lang = s.get("language", "fa")
    if lang not in settings.LANGUAGES:
        lang = "fa"
    if "lang" not in st.session_state:
        st.session_state["lang"] = lang
    return st.session_state["lang"]


def main() -> None:
    st.set_page_config(
        page_title="CLA / سیلا",
        page_icon="⚗️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    lang = _bootstrap()
    ui_utils.inject_css(lang)

    # ---- sidebar: language switch + navigation + status -------------------
    with st.sidebar:
        st.markdown(f"## ⚗️ {i18n.t('app.title', lang)}")
        st.caption(i18n.t("app.subtitle", lang))

        new_lang = st.radio(
            i18n.t("sidebar.language", lang),
            options=["fa", "en"],
            format_func=lambda x: "فارسی 🇮🇷" if x == "fa" else "English 🇬🇧",
            index=0 if lang == "fa" else 1,
            horizontal=True,
            key="lang_radio",
            label_visibility="collapsed",
        )
        if new_lang != st.session_state.get("lang"):
            st.session_state["lang"] = new_lang
            settings.set_language(new_lang)
            st.rerun()
        lang = new_lang

        st.divider()
        page = st.radio(
            "NAV",
            options=["library", "add_edit", "search", "transfer", "settings"],
            format_func=lambda p: i18n.t(f"nav.{p}", lang),
            key="nav_page",
            label_visibility="collapsed",
        )
        st.divider()
        st.caption(f"🌍 {i18n.t('sidebar.offline', lang)}")
        stats = db.db_stats()
        st.caption(
            f"{i18n.t('sidebar.db', lang)}: {stats['materials']} "
            f"{i18n.t('library.count', lang)}"
        )
        st.caption(f"🧪 {rdkit_status_message()}")
        st.caption(f"{i18n.t('sidebar.version', lang)}: {config.APP_VERSION}")

    # ---- page routing ------------------------------------------------------
    if page == "library":
        library.render(lang)
    elif page == "add_edit":
        add_edit.render(lang)
    elif page == "search":
        search.render(lang)
    elif page == "transfer":
        transfer.render(lang)
    else:
        settings_page.render(lang)
