"""CLA / سیلا — user settings (spec 06 §4).

Stored at ``data/user_settings/settings.json``. Keys follow the spec:
language, default search depth, max computation time, preferred local AI
model, theme, safety display level. Phase-1 UI exposes language; the rest
are persisted defaults for later phases (they are part of the spec schema).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend import config

DEFAULTS: dict[str, Any] = {
    "language": "fa",                 # 'fa' | 'en'
    "theme": "light",                 # 'light' | 'dark' (visual theme; Streamlit-managed)
    "default_search_depth": 4,        # Phase 2 (AiZynthFinder iterations)
    "max_computation_time_s": 600,    # Phase 2 (route-search budget)
    "preferred_local_ai_model": "",   # Phase 3 (Ollama model name)
    "safety_display_level": "full",   # Phase 2 ('full' | 'summary')
}

LANGUAGES = ("fa", "en")


def _path(db_path: Path | None = None) -> Path:
    return config.SETTINGS_PATH


def load_settings() -> dict:
    config.ensure_data_dirs()
    data = dict(DEFAULTS)
    p = _path()
    if p.exists():
        try:
            stored = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(stored, dict):
                data.update(stored)
        except (json.JSONDecodeError, OSError):
            pass  # corrupt settings -> fall back to defaults (never crash)
    return data


def save_settings(updates: dict) -> dict:
    """Merge ``updates`` into the settings file and return the full settings."""
    current = load_settings()
    current.update({k: v for k, v in updates.items() if k in DEFAULTS})
    config.ensure_data_dirs()
    _path().write_text(
        json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return current


def get_language() -> str:
    lang = str(load_settings().get("language", "fa"))
    return lang if lang in LANGUAGES else "fa"


def set_language(lang: str) -> str:
    if lang not in LANGUAGES:
        raise ValueError(f"unsupported language: {lang}")
    save_settings({"language": lang})
    return lang
