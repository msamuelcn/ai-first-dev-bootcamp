"""Entrypoint for the Code Insight CLI."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codeinsight.cli import run


def main() -> int:
    """Run the CLI application."""
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
