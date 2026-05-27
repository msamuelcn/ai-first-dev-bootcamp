"""Summarize command registration and placeholder handler."""

from __future__ import annotations

import argparse
from pathlib import Path

from mcp.client import MCPConnectionError, MCPOperationError
from mcp.filesystem import create_local_filesystem_client


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the summarize command."""
    parser = subparsers.add_parser(
        "summarize",
        help="Summarize a file.",
    )
    parser.add_argument("file", help="Path to the file to summarize.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Summarize a text file using MCP read_file."""
    try:
        client = create_local_filesystem_client()
        with client:
            payload = client.read_file(args.file)

        if payload.get("is_binary"):
            print(_unsupported_type_error(args.file))
            return

        content = str(payload.get("content", ""))
        if not content.strip():
            print(
                f"Error: File is empty and cannot be summarized: {args.file}. Please provide a valid file for analysis."
            )
            return

        print(_build_summary(args.file, content))
    except ValueError:
        print(
            f"Error: Invalid path format: {args.file}. Please provide a valid path and try again."
        )
    except FileNotFoundError:
        print(
            f"Error: Path not found: {args.file}. Please check the path and try again."
        )
    except IsADirectoryError:
        print(
            f"Error: Invalid path format: {args.file}. Please provide a file path and try again."
        )
    except PermissionError:
        print(
            f"Error: Permission denied when accessing: {args.file}. Please check your permissions and try again."
        )
    except MCPConnectionError:
        print(
            "Error: Unable to connect to MCP server. Please ensure the server is running and try again."
        )
    except MCPOperationError:
        print(
            "Error: MCP operation failed: unable to summarize file. Please check your MCP connection and try again."
        )
    except Exception:
        print(
            "Error: Unable to summarize file right now. Please verify the file path and MCP setup, then try again."
        )


def _build_summary(file_path: str, content: str) -> str:
    """Create a concise, human-readable summary for text content."""
    normalized_lines = [line.strip() for line in content.splitlines() if line.strip()]
    preview = normalized_lines[0] if normalized_lines else "No notable section found"
    if len(preview) > 100:
        preview = f"{preview[:97]}..."

    line_count = content.count("\n") + 1
    word_count = len(content.split())

    return "\n".join(
        [
            f"Summary: {Path(file_path).name}",
            f"Stats: {line_count} lines, {word_count} words",
            f"Purpose: {_infer_purpose(file_path, content)}",
            f"Highlight: {preview}",
        ]
    )


def _infer_purpose(file_path: str, content: str) -> str:
    """Infer a short purpose statement from extension and simple patterns."""
    suffix = Path(file_path).suffix.lower()

    if suffix == ".py":
        if "argparse" in content:
            return "Python CLI or script logic"
        return "Python source code"

    if suffix in {".md", ".rst"}:
        return "Documentation or notes"

    if suffix in {".log"}:
        return "Application/runtime log output"

    if suffix in {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"}:
        return "Configuration or structured data"

    return "Text content for quick review"


def _unsupported_type_error(file_path: str) -> str:
    """Return spec-compliant unsupported file type error."""
    return (
        f"Error: Unsupported file type for analysis: {file_path}. "
        "Supported types are .py, .js, .log, etc."
    )
