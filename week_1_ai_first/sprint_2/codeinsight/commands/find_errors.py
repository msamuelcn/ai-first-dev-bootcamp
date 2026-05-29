"""Find-errors command registration and placeholder handler."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from codeinsight.mcp.client import MCPConnectionError, MCPOperationError
from codeinsight.mcp.filesystem import create_filesystem_client

_ERROR_RE = re.compile(r"\berror\b", re.IGNORECASE)
_WARNING_RE = re.compile(r"\bwarning\b", re.IGNORECASE)
_EXCEPTION_RE = re.compile(r"\bexception\b", re.IGNORECASE)
_TRACEBACK_RE = re.compile(r"\btraceback\b", re.IGNORECASE)


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the find-errors command."""
    parser = subparsers.add_parser(
        "find-errors",
        help="Scan files/logs for potential error patterns.",
    )
    parser.add_argument("path", help="Path to the project or log file to scan.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Scan a log file for common error patterns using MCP read_file."""
    try:
        client = create_filesystem_client()
        with client:
            payload = client.read_file(args.path)

        if payload.get("is_binary"):
            print(_unsupported_type_error(args.path))
            return

        extension = str(payload.get("extension", "")).lower()
        if extension not in {".log", ".txt", ".out", ".err"}:
            print(_unsupported_type_error(args.path))
            return

        content = str(payload.get("content", ""))
        if not content.strip():
            print(
                f"Error: File is empty and cannot be summarized: {args.path}. Please provide a valid file for analysis."
            )
            return

        report = _scan_log_content(content)
        print(_format_report(args.path, report))
    except ValueError:
        print(
            f"Error: Invalid path format: {args.path}. Please provide a valid path and try again."
        )
    except FileNotFoundError:
        print(
            f"Error: Path not found: {args.path}. Please check the path and try again."
        )
    except IsADirectoryError:
        print(
            f"Error: Invalid path format: {args.path}. Please provide a valid file path and try again."
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
            "Error: MCP operation failed: unable to scan log file. Please check your MCP connection and try again."
        )
    except Exception:
        print(
            "Error: Unable to scan log file right now. Please verify the file path and MCP setup, then try again."
        )


def _scan_log_content(content: str) -> dict[str, object]:
    """Parse log content and collect grouped error counts with issue frequencies."""
    counts = {
        "ERROR": 0,
        "WARNING": 0,
        "EXCEPTION": 0,
        "TRACEBACK": 0,
    }
    issues: Counter[str] = Counter()

    lines = content.splitlines()
    for line in lines:
        # Be defensive: malformed log lines should never abort scanning.
        try:
            has_error = bool(_ERROR_RE.search(line))
            has_warning = bool(_WARNING_RE.search(line))
            has_exception = bool(_EXCEPTION_RE.search(line))
            has_traceback = bool(_TRACEBACK_RE.search(line))

            if has_error:
                counts["ERROR"] += 1
            if has_warning:
                counts["WARNING"] += 1
            if has_exception:
                counts["EXCEPTION"] += 1
            if has_traceback:
                counts["TRACEBACK"] += 1

            if has_error or has_warning or has_exception or has_traceback:
                normalized = _normalize_issue_line(line)
                if normalized:
                    issues[normalized] += 1
        except Exception:
            continue

    return {
        "counts": counts,
        "top_issues": issues.most_common(3),
        "matched_total": sum(counts.values()),
        "line_total": len(lines),
    }


def _normalize_issue_line(line: str) -> str:
    """Sanitize an issue line to keep output readable and avoid stack trace dumps."""
    cleaned = line.strip()
    cleaned = re.sub(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:,\d+)?", "", cleaned)
    cleaned = re.sub(r"\bline\s+\d+\b", "line <n>", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b0x[0-9a-fA-F]+\b", "<addr>", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -|:")

    if not cleaned:
        return "Unspecified issue"

    if cleaned.lower().startswith("traceback"):
        return "Traceback detected"

    if len(cleaned) > 140:
        cleaned = f"{cleaned[:137]}..."

    return cleaned


def _format_report(path: str, report: dict[str, object]) -> str:
    """Render grouped summary and top frequent issue list."""
    counts = report["counts"]
    assert isinstance(counts, dict)
    top_issues = report["top_issues"]
    assert isinstance(top_issues, list)

    lines = [
        f"Log scan: {Path(path).name}",
        "Counts:",
        f"- ERROR: {counts['ERROR']}",
        f"- WARNING: {counts['WARNING']}",
        f"- EXCEPTION: {counts['EXCEPTION']}",
        f"- TRACEBACK: {counts['TRACEBACK']}",
    ]

    if top_issues:
        lines.append("Top issues:")
        for rank, (issue, count) in enumerate(top_issues, start=1):
            lines.append(f"{rank}. {issue} ({count})")
    else:
        lines.append("Top issues: none detected")

    return "\n".join(lines)


def _unsupported_type_error(path: str) -> str:
    """Return spec-compliant unsupported file type error."""
    return (
        f"Error: Unsupported file type for analysis: {path}. "
        "Supported types are .py, .js, .log, etc."
    )
