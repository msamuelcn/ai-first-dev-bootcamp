"""Tree command registration and placeholder handler."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from mcp.client import MCPConnectionError, MCPOperationError
from mcp.filesystem import create_local_filesystem_client


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the tree command."""
    parser = subparsers.add_parser(
        "tree",
        help="Display a directory tree.",
    )
    parser.add_argument("path", help="Path to the directory to display as a tree.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Render a directory tree using the filesystem MCP client."""
    try:
        client = create_local_filesystem_client()
        with client:
            listing = client.list_directory(args.path)
        print(_render_tree(listing))
    except Exception as exc:
        print(_format_tree_error(args.path, exc))


def _format_tree_error(path: str, error: Exception) -> str:
    """Convert internal failures into user-friendly tree command errors."""
    if isinstance(error, ValueError):
        return (
            f"Error: Invalid path format: {path}. Please provide a valid path and try again. "
            "Examples: . , ./src , C:/projects/codeinsight"
        )

    if isinstance(error, FileNotFoundError):
        return f"Error: Path not found: {path}. Please check the path and try again."

    if isinstance(error, NotADirectoryError):
        return f"Error: Path not found: {path}. Please provide a directory path and try again."

    if isinstance(error, PermissionError):
        return (
            f"Error: Permission denied when accessing: {path}. "
            "Please check your permissions and try again."
        )

    if isinstance(error, MCPConnectionError):
        return (
            "Error: Unable to connect to MCP server. "
            "Please ensure the server is running and try again."
        )

    if isinstance(error, MCPOperationError):
        return (
            "Error: MCP operation failed: unable to display directory tree. "
            "Please check your MCP connection and try again."
        )

    return (
        "Error: Unable to display directory tree right now. "
        "Please verify the path and MCP setup, then try again."
    )


def _render_tree(listing: Any) -> str:
    """Render a recursive tree from MCP directory listing data."""
    root_label = _normalize_root_label(listing)
    entries = _extract_entries(listing)

    lines = [root_label]
    lines.extend(_render_entries(entries, prefix=""))
    return "\n".join(lines)


def _normalize_root_label(listing: Any) -> str:
    """Create the top-level label for the rendered tree."""
    if isinstance(listing, dict):
        root_path = listing.get("path")
        if isinstance(root_path, str) and root_path.strip():
            return str(Path(root_path))

    return "."


def _extract_entries(listing: Any) -> list[dict[str, Any]]:
    """Extract entry dictionaries from common MCP listing shapes."""
    if isinstance(listing, dict):
        if isinstance(listing.get("entries"), list):
            return [entry for entry in listing["entries"] if isinstance(entry, dict)]
        if isinstance(listing.get("children"), list):
            return [entry for entry in listing["children"] if isinstance(entry, dict)]

    if isinstance(listing, list):
        return [entry for entry in listing if isinstance(entry, dict)]

    return []


def _render_entries(entries: list[dict[str, Any]], prefix: str) -> list[str]:
    """Render tree branches for a list of entries."""
    lines: list[str] = []
    total = len(entries)

    for index, entry in enumerate(entries):
        is_last = index == total - 1
        branch = "`-- " if is_last else "|-- "
        name = str(entry.get("name") or entry.get("path") or "<unknown>")
        entry_type = entry.get("type")
        label = f"{name}/" if entry_type == "directory" else name
        lines.append(f"{prefix}{branch}{label}")

        child_entries = _extract_entries(entry)
        if child_entries:
            child_prefix = f"{prefix}    " if is_last else f"{prefix}|   "
            lines.extend(_render_entries(child_entries, child_prefix))

    return lines
