"""CLA / سیلا — project path configuration.

All paths are resolved RELATIVE to the project root (spec 06: "Always use
relative paths inside the project", "Never hard-code absolute paths").
The whole ``data/`` folder is designed to be copied to another machine and
work offline.
"""

from __future__ import annotations

from pathlib import Path

# Project root = parent of the backend package directory
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

DATA_DIR: Path = PROJECT_ROOT / "data"
STARTING_MATERIALS_DIR: Path = DATA_DIR / "starting_materials"
ROUTES_DIR: Path = DATA_DIR / "routes"
MODELS_DIR: Path = DATA_DIR / "models"
STOCKS_DIR: Path = DATA_DIR / "stocks"
CACHE_DIR: Path = DATA_DIR / "cache"
USER_SETTINGS_DIR: Path = DATA_DIR / "user_settings"

# Spec 06: SQLite location for the starting-materials database
DB_PATH: Path = STARTING_MATERIALS_DIR / "compounds.db"

# Spec 06: user settings JSON
SETTINGS_PATH: Path = USER_SETTINGS_DIR / "settings.json"

APP_NAME_EN = "CLA — Chemistry Lab Assistant"
APP_NAME_FA = "سیلا — دستیار آزمایشگاه شیمی"
APP_VERSION = "0.1.0 (Phase 1)"


def ensure_data_dirs() -> None:
    """Create the runtime data folders if they do not exist yet."""
    for d in (
        DATA_DIR,
        STARTING_MATERIALS_DIR,
        ROUTES_DIR,
        MODELS_DIR,
        STOCKS_DIR,
        CACHE_DIR,
        USER_SETTINGS_DIR,
    ):
        d.mkdir(parents=True, exist_ok=True)
