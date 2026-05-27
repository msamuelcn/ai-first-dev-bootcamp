"""Analyze command registration and placeholder handler."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from mcp.client import MCPConnectionError, MCPOperationError
from mcp.filesystem import create_local_filesystem_client


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the analyze command."""
    parser = subparsers.add_parser(
        "analyze",
        help="Analyze a project path and summarize structure.",
    )
    parser.add_argument("path", help="Path to the project directory to analyze.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Analyze a directory with MCP and print a concise project summary."""
    try:
        client = create_local_filesystem_client()
        with client:
            listing = client.list_directory(args.path)
            summary = _analyze_listing(client, listing)
        print(_format_summary(summary))
    except ValueError:
        print(
            f"Error: Invalid path format: {args.path}. Please provide a valid path and try again."
        )
    except FileNotFoundError:
        print(
            f"Error: Path not found: {args.path}. Please check the path and try again."
        )
    except NotADirectoryError:
        print(
            f"Error: Path not found: {args.path}. Please provide a directory path and try again."
        )
    except PermissionError:
        print(
            f"Error: Permission denied when accessing: {args.path}. Please check your permissions and try again."
        )
    except MCPConnectionError:
        print(
            "Error: Unable to connect to MCP server. Please ensure the server is running and try again."
        )
    except MCPOperationError:
        print(
            "Error: MCP operation failed: unable to analyze project. Please check your MCP connection and try again."
        )
    except Exception:
        print(
            "Error: Unable to analyze project right now. Please verify the path and MCP setup, then try again."
        )


def _analyze_listing(client: Any, listing: Any) -> dict[str, Any]:
    """Collect file statistics and project signals from an MCP listing payload."""
    files = _collect_files(listing)
    total_files = len(files)

    extension_counts: Counter[str] = Counter()
    for file_entry in files:
        extension_counts[_normalized_extension(file_entry)] += 1

    project_type = _detect_project_type(client, files)

    return {
        "root": _root_label(listing),
        "total_files": total_files,
        "extension_counts": extension_counts,
        "project_type": project_type,
    }


def _collect_files(node: Any) -> list[dict[str, Any]]:
    """Recursively flatten files from MCP list_directory response."""
    files: list[dict[str, Any]] = []

    if isinstance(node, list):
        for item in node:
            files.extend(_collect_files(item))
        return files

    if not isinstance(node, dict):
        return files

    node_type = str(node.get("type", "")).lower()
    if node_type == "file":
        files.append(node)
        return files

    for key in ("entries", "children"):
        children = node.get(key)
        if isinstance(children, list):
            for child in children:
                files.extend(_collect_files(child))

    return files


def _normalized_extension(file_entry: dict[str, Any]) -> str:
    """Return a normalized extension bucket for file counting."""
    name = str(file_entry.get("name") or file_entry.get("path") or "")
    suffix = Path(name).suffix.lower()
    return suffix if suffix else "[no-ext]"


def _detect_project_type(client: Any, files: list[dict[str, Any]]) -> str:
    """Infer project type based on file names, extensions, and MCP-read hints."""
    names = {str(file_entry.get("name", "")).lower() for file_entry in files}
    extension_counts = Counter(_normalized_extension(entry) for entry in files)

    if "package.json" in names:
        if _contains_token(client, files, {"package.json"}, "fastapi"):
            return "Node.js project"
        return "Node.js project"

    python_like = extension_counts[".py"] > 0 or "requirements.txt" in names
    if python_like and _contains_fastapi_signal(client, files):
        return "FastAPI project"

    if python_like:
        return "generic Python project"

    return "unknown project type"


def _contains_fastapi_signal(client: Any, files: list[dict[str, Any]]) -> bool:
    """Check common files for FastAPI dependency/import hints via MCP read_file."""
    if _contains_token(
        client, files, {"requirements.txt", "pyproject.toml"}, "fastapi"
    ):
        return True

    py_files = [
        entry for entry in files if str(entry.get("name", "")).lower().endswith(".py")
    ][:12]

    for entry in py_files:
        path = entry.get("path")
        if not isinstance(path, str):
            continue

        try:
            payload = client.read_file(path)
        except Exception:
            continue

        if payload.get("is_binary"):
            continue

        text = str(payload.get("content", "")).lower()
        if "from fastapi" in text or "import fastapi" in text or "fastapi(" in text:
            return True

    return False


def _contains_token(
    client: Any, files: list[dict[str, Any]], target_names: set[str], token: str
) -> bool:
    """Read selected files through MCP and look for a token."""
    lowered_token = token.lower()

    for entry in files:
        name = str(entry.get("name", "")).lower()
        if name not in target_names:
            continue

        path = entry.get("path")
        if not isinstance(path, str):
            continue

        try:
            payload = client.read_file(path)
        except Exception:
            continue

        if payload.get("is_binary"):
            continue

        text = str(payload.get("content", "")).lower()
        if lowered_token in text:
            return True

    return False


def _root_label(listing: Any) -> str:
    """Return top-level path label from MCP listing payload."""
    if isinstance(listing, dict):
        raw_path = listing.get("path")
        if isinstance(raw_path, str) and raw_path.strip():
            return str(Path(raw_path))
    return "."


def _format_summary(summary: dict[str, Any]) -> str:
    """Format the final analyze command output."""
    counts: Counter[str] = summary["extension_counts"]
    top_types = counts.most_common(6)
    if top_types:
        type_line = ", ".join(f"{ext}:{count}" for ext, count in top_types)
    else:
        type_line = "none"

    return "\n".join(
        [
            f"FILE ANALYSIS SUMMARY",
            f"Project: {summary['root']}",
            f"Total files: {summary['total_files']}",
            f"File types: {type_line}",
            f"Detected type: {summary['project_type']}",
        ]
    )
