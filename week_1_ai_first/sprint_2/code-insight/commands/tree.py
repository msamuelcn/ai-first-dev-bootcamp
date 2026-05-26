"""Tree command registration and placeholder handler."""

from __future__ import annotations

import argparse


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the tree command."""
    parser = subparsers.add_parser(
        "tree",
        help="Display a directory tree.",
    )
    parser.add_argument("path", help="Path to the directory to display as a tree.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Placeholder tree handler."""
    print(f"[TODO] tree is not implemented yet (path={args.path}).")
