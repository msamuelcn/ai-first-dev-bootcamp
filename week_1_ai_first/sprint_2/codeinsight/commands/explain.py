"""Explain command registration and placeholder handler."""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

from mcp.client import MCPConnectionError, MCPOperationError
from mcp.filesystem import create_filesystem_client

_SUPPORTED_CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".rb",
    ".php",
    ".swift",
    ".kt",
    ".m",
    ".scala",
    ".sh",
    ".ps1",
    ".sql",
}


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the explain command."""
    parser = subparsers.add_parser(
        "explain",
        help="Explain a source file in plain language.",
    )
    parser.add_argument("file", help="Path to the source file to explain.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Explain code structure and flow for a source file read via MCP."""
    try:
        client = create_filesystem_client()
        with client:
            payload = client.read_file(args.file)

        if payload.get("is_binary"):
            print(_unsupported_type_error(args.file))
            return

        extension = str(payload.get("extension", "")).lower()
        if extension not in _SUPPORTED_CODE_EXTENSIONS:
            print(_unsupported_type_error(args.file))
            return

        content = str(payload.get("content", ""))
        if not content.strip():
            print(
                f"Error: File is empty and cannot be explained: {args.file}. Please provide a valid file for analysis."
            )
            return

        print(_build_explanation(args.file, extension, content))
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
            "Error: MCP operation failed: unable to explain file. Please check your MCP connection and try again."
        )
    except Exception:
        print(
            "Error: Unable to explain file right now. Please verify the file path and MCP setup, then try again."
        )


def _build_explanation(file_path: str, extension: str, content: str) -> str:
    """Build concise explanation output for a source file."""
    purpose = _infer_purpose(file_path, extension, content)
    functions, classes = _extract_symbols(extension, content)
    flow = _build_flow_summary(extension, content, functions, classes)

    return "\n".join(
        [
            f"File: {Path(file_path).name}",
            f"Purpose: {purpose}",
            f"Main functions/classes: {_format_symbols(functions, classes)}",
            f"Flow summary: {flow}",
        ]
    )


def _infer_purpose(file_path: str, extension: str, content: str) -> str:
    """Infer high-level purpose of the file from extension and token hints."""
    lower_content = content.lower()
    file_name = Path(file_path).name.lower()

    if extension == ".py":
        if "argparse" in lower_content:
            return "Defines a command-line interface and command execution flow"
        if "fastapi" in lower_content:
            return "Implements API endpoints and request handling"
        return "Implements Python application logic"

    if extension in {".js", ".ts", ".jsx", ".tsx"}:
        if "express(" in lower_content or "from 'express'" in lower_content:
            return "Implements a Node.js web/server module"
        return "Implements JavaScript/TypeScript application logic"

    if file_name.startswith("test_") or file_name.endswith(".test.js"):
        return "Contains automated tests"

    return "Contains source code logic for part of the application"


def _extract_symbols(extension: str, content: str) -> tuple[list[str], list[str]]:
    """Extract main function and class names without dumping file content."""
    if extension == ".py":
        return _extract_python_symbols(content)

    class_matches = re.findall(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)", content)
    function_matches = re.findall(
        r"\b(?:function\s+([A-Za-z_][A-Za-z0-9_]*)|([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\([^)]*\)\s*=>)",
        content,
    )

    functions = []
    for one, two in function_matches:
        name = one or two
        if name:
            functions.append(name)

    return _unique_limited(functions), _unique_limited(class_matches)


def _extract_python_symbols(content: str) -> tuple[list[str], list[str]]:
    """Extract top-level Python symbols via AST."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return [], []

    functions: list[str] = []
    classes: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.AsyncFunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return _unique_limited(functions), _unique_limited(classes)


def _build_flow_summary(
    extension: str, content: str, functions: list[str], classes: list[str]
) -> str:
    """Generate a short execution-flow summary from detected structure."""
    lower_content = content.lower()

    if extension == ".py":
        has_main_guard = 'if __name__ == "__main__"' in content
        if has_main_guard and functions:
            return f"Defines reusable units, then enters execution through the main guard, likely invoking {functions[0]}."
        if classes and functions:
            return "Defines classes and helper functions, then orchestrates behavior through function calls."
        if functions:
            return "Defines functions and executes logic by calling them in sequence."
        return "Runs module-level logic with minimal explicit function structure."

    if (
        "router" in lower_content
        or "route" in lower_content
        or "endpoint" in lower_content
    ):
        return "Declares handlers/routes and processes inputs through those handlers."

    if functions or classes:
        return "Defines code units that are composed to perform the module's main behavior."

    return "Contains mostly inline logic with a straightforward top-to-bottom flow."


def _format_symbols(functions: list[str], classes: list[str]) -> str:
    """Format symbol list for concise output."""
    parts: list[str] = []
    if classes:
        parts.append(f"classes: {', '.join(classes)}")
    if functions:
        parts.append(f"functions: {', '.join(functions)}")

    if not parts:
        return "no major functions or classes detected"

    return " | ".join(parts)


def _unique_limited(items: list[str], limit: int = 6) -> list[str]:
    """Return unique items preserving order with a max limit."""
    seen: set[str] = set()
    result: list[str] = []

    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
        if len(result) >= limit:
            break

    return result


def _unsupported_type_error(file_path: str) -> str:
    """Return spec-compliant unsupported file type error."""
    return (
        f"Error: Unsupported file type for analysis: {file_path}. "
        "Supported types are .py, .js, .log, etc."
    )
