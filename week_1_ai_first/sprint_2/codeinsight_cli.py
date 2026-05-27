"""Console entrypoint for the Code Insight CLI command."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    """Delegate execution to the existing CLI main module."""
    cli_dir = Path(__file__).resolve().parent / "codeinsight"
    sys.path.insert(0, str(cli_dir))

    from main import main as run_main

    return run_main()
