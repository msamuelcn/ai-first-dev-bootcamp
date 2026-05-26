"""Summarize command registration and placeholder handler."""

from __future__ import annotations

import argparse


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the summarize command."""
    parser = subparsers.add_parser(
        "summarize",
        help="Summarize a file.",
    )
    parser.add_argument("file", help="Path to the file to summarize.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Placeholder summarize handler."""
    print(f"[TODO] summarize is not implemented yet (file={args.file}).")
