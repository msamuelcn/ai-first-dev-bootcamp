"""Find-errors command registration and placeholder handler."""

from __future__ import annotations

import argparse


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the find-errors command."""
    parser = subparsers.add_parser(
        "find-errors",
        help="Scan files/logs for potential error patterns.",
    )
    parser.add_argument("path", help="Path to the project or log file to scan.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Placeholder find-errors handler."""
    print(f"[TODO] find-errors is not implemented yet (path={args.path}).")
