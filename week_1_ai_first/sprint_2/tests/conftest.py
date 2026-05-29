"""Pytest configuration: load .env from the sprint root before tests run."""

from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv(env_file: Path) -> None:
    """Parse a simple KEY=value .env file and inject into os.environ."""
    if not env_file.is_file():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, _, raw_value = line.partition("=")
        key = key.strip()
        value = raw_value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv(Path(__file__).resolve().parents[1] / ".env")
