"""Command-line parser and command registration for Code Insight CLI."""

from __future__ import annotations

import argparse
from typing import Sequence

from commands import analyze, explain, find_errors, summarize, tree


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level CLI parser."""
    parser = argparse.ArgumentParser(
        prog="code-insight",
        description="Inspect projects and files through MCP-backed commands.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze.register(subparsers)
    summarize.register(subparsers)
    explain.register(subparsers)
    tree.register(subparsers)
    find_errors.register(subparsers)

    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Parse args and dispatch to a selected command handler."""
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)

    if handler is None:
        parser.print_help()
        return 1

    handler(args)
    return 0
