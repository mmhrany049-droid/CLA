"""CLA / سیلا — application entry point.

Run with:
    streamlit run app.py

Phase 1: Starting Materials Manager (see CLA_Prompts/07_Development_Roadmap_and_Priorities.md).
Fully offline — the app never contacts the internet at runtime.
"""

from __future__ import annotations

import os
import sys

# Make the project root importable regardless of how Streamlit was launched.
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from frontend.main import main  # noqa: E402

main()
