"""Analyze command registration and placeholder handler."""

from __future__ import annotations

import argparse


def register(subparsers: argparse._SubParsersAction) -> None:
	"""Register the analyze command."""
	parser = subparsers.add_parser(
		"analyze",
		help="Analyze a project path and summarize structure.",
	)
	parser.add_argument("path", help="Path to the project directory to analyze.")
	parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
	"""Placeholder analyze handler."""
	print(f"[TODO] analyze is not implemented yet (path={args.path}).")
