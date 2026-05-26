"""Explain command registration and placeholder handler."""

from __future__ import annotations

import argparse


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the explain command."""
    parser = subparsers.add_parser(
        "explain",
        help="Explain a source file in plain language.",
    )
    parser.add_argument("file", help="Path to the source file to explain.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Placeholder explain handler."""
    print(f"[TODO] explain is not implemented yet (file={args.file}).")
