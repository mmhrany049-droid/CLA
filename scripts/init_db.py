#!/usr/bin/env python3
"""CLA / سیلا — initialize (and pre-load) the starting-materials database.

Usage:
    python scripts/init_db.py

Idempotent: safe to run repeatedly; existing user data is never modified.
The Streamlit app also does this automatically on first launch.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import config, db  # noqa: E402
from backend.seed import loader  # noqa: E402


def main() -> int:
    config.ensure_data_dirs()
    path = db.init_db()
    inserted = loader.seed_if_empty()
    stats = db.db_stats()
    print(f"Database : {path}")
    print(f"Inserted : {inserted} default material(s) this run")
    print(f"Total    : {stats['materials']} material(s) "
          f"(active {stats['active']}, low {stats['low_stock']}, "
          f"out {stats['out_of_stock']}, inactive {stats['inactive']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
