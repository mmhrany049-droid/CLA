"""CLA / سیلا — shared UI helpers: RTL layout for Persian, badges, formats."""

from __future__ import annotations

import streamlit as st

from backend import i18n
from backend.materials import Material

# Base CSS + Persian (RTL) layout. Latin technical content (SMILES, InChIKey,
# numbers) keeps LTR direction via Unicode bidi isolation.
_CSS_COMMON = """
<style>
.block-container { padding-top: 2.2rem; }
div[data-testid="stMetricValue"] { font-size: 1.35rem; }
.code-ltr, [data-testid="stDataFrame"] { unicode-bidi: isolate; }
span.ghs-badge {
  display:inline-block; margin:2px 4px 2px 0; padding:2px 8px;
  border-radius:10px; background:#fdecea; color:#b3261e;
  border:1px solid #f5c6c0; font-size:0.82em; font-family:monospace;
}
span.ghs-none {
  display:inline-block; margin:2px 4px 2px 0; padding:2px 8px;
  border-radius:10px; background:#e8f5e9; color:#1b5e20;
  border:1px solid #c8e6c9; font-size:0.82em;
}
</style>
"""

_CSS_RTL = """
<style>
html, body, [class*="css"] { direction: rtl; }
div[data-testid="stSidebar"] { direction: rtl; }
/* keep code-ish content LTR inside an RTL page */
code, pre, [data-testid="stDataFrame"], textarea, span.code-ltr {
  direction: ltr !important; text-align: left; unicode-bidi: isolate;
}
h1, h2, h3, label, p, li { text-align: right; }
div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"] { text-align: right; }
</style>
"""


def inject_css(lang: str) -> None:
    st.markdown(_CSS_COMMON, unsafe_allow_html=True)
    if lang == "fa":
        st.markdown(_CSS_RTL, unsafe_allow_html=True)


def status_badge(m: Material, lang: str) -> str:
    return i18n.t(f"status.{m.effective_status}", lang)


def ghs_html(m: Material, lang: str) -> str:
    """Render GHS codes as badges with localized statements (title tooltip)."""
    if not m.ghs_hazards:
        label = "بدون کلاس خطر ثبت‌شده" if lang == "fa" else "No hazards on record"
        return f'<span class="ghs-none">{label}</span>'
    out = []
    for code in m.ghs_hazards:
        label = i18n.ghs_label(code, lang)
        out.append(f'<span class="ghs-badge" title="{label}">{code}</span>')
    return "".join(out)


def ghs_lines(m: Material, lang: str) -> list[str]:
    if not m.ghs_hazards:
        label = "بدون کلاس خطر ثبت‌شده" if lang == "fa" else "No hazards on record"
        return [label]
    return [i18n.ghs_label(c, lang) for c in m.ghs_hazards]


def fmt_qty(m: Material) -> str:
    q = m.quantity or 0
    qs = f"{q:g}"
    return f"{qs} {m.unit}"


def fmt_num(v, digits=3) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):.{digits}f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)
    except (TypeError, ValueError):
        return str(v)


def localized_name(m: Material, lang: str) -> str:
    """Name in the active language, falling back to the other one."""
    primary = m.name_fa if lang == "fa" else m.name_en
    return primary or m.name_en or m.name_fa or "?"


def material_row_for_table(m: Material, lang: str) -> dict:
    """One table row, localized."""
    return {
        i18n.t("col.name", lang): localized_name(m, lang),
        i18n.t("col.cas", lang): m.cas or "—",
        i18n.t("col.formula", lang): m.formula or "—",
        i18n.t("col.mw", lang): fmt_num(m.molecular_weight),
        i18n.t("col.quantity", lang): fmt_qty(m),
        i18n.t("col.status", lang): i18n.t(f"status.{m.effective_status}", lang),
        "id": m.id,
    }


def toast(msg: str) -> None:
    st.toast(msg, icon="⚗️")
