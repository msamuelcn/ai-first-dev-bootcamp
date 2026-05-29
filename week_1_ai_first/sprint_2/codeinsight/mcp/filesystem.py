"""Filesystem-oriented MCP helpers built on top of MCPClient."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .client import MCPClient, MCPConnectionSettings


class LocalFilesystemTransport:
    """Simple local transport used to adapt filesystem access through MCP client APIs."""

    _BINARY_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".bmp",
        ".ico",
        ".pdf",
        ".zip",
        ".gz",
        ".tar",
        ".7z",
        ".exe",
        ".dll",
        ".so",
        ".bin",
        ".dat",
        ".mp3",
        ".wav",
        ".mp4",
        ".mov",
        ".avi",
        ".pyc",
    }

    def open(self, settings: MCPConnectionSettings) -> None:
        """Open the transport connection."""

    def close(self) -> None:
        """Close the transport connection."""

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute a filesystem tool request."""
        if tool_name == "list_directory":
            return self._list_directory(arguments["path"])

        if tool_name == "read_file":
            return self._read_file(arguments["path"])

        raise ValueError(f"Unsupported tool: {tool_name}")

    def _list_directory(self, path: str) -> dict[str, Any]:
        """Return a recursive directory listing for a path."""
        if not isinstance(path, str) or not path.strip():
            raise ValueError("Invalid path format")

        try:
            directory = Path(path).expanduser()
        except (TypeError, ValueError) as exc:
            raise ValueError("Invalid path format") from exc

        if not directory.exists():
            raise FileNotFoundError(path)

        if not directory.is_dir():
            raise NotADirectoryError(path)

        return {
            "path": str(directory),
            "type": "directory",
            "entries": self._build_entries(directory),
        }

    def _build_entries(self, directory: Path) -> list[dict[str, Any]]:
        """Build nested entries for a directory."""
        entries: list[dict[str, Any]] = []

        children = sorted(
            directory.iterdir(), key=lambda item: (item.is_file(), item.name.lower())
        )

        for child in children:
            entry: dict[str, Any] = {
                "name": child.name,
                "path": str(child),
                "type": "directory" if child.is_dir() else "file",
            }

            if child.is_dir() and not child.is_symlink():
                entry["entries"] = self._build_entries(child)

            entries.append(entry)

        return entries

    def _read_file(self, path: str) -> dict[str, Any]:
        """Return a file payload for summarize/explain style commands."""
        if not isinstance(path, str) or not path.strip():
            raise ValueError("Invalid path format")

        try:
            file_path = Path(path).expanduser()
        except (TypeError, ValueError) as exc:
            raise ValueError("Invalid path format") from exc

        if not file_path.exists():
            raise FileNotFoundError(path)

        if file_path.is_dir():
            raise IsADirectoryError(path)

        raw = file_path.read_bytes()
        extension = file_path.suffix.lower()

        if extension in self._BINARY_EXTENSIONS or self._looks_binary(raw):
            return {
                "path": str(file_path),
                "content": "",
                "extension": extension,
                "is_binary": True,
                "size_bytes": len(raw),
                "line_count": 0,
            }

        content = raw.decode("utf-8")

        return {
            "path": str(file_path),
            "content": content,
            "extension": extension,
            "is_binary": False,
            "size_bytes": len(raw),
            "line_count": content.count("\n") + (1 if content else 0),
        }

    @staticmethod
    def _looks_binary(raw: bytes) -> bool:
        """Heuristic binary detector for unknown file extensions."""
        if not raw:
            return False

        if b"\x00" in raw:
            return True

        try:
            raw.decode("utf-8")
            return False
        except UnicodeDecodeError:
            return True


class StdioFilesystemTransport:
    """MCP stdio transport that launches an external filesystem server process."""

    _TRACE_ENV_VAR = "CODEINSIGHT_MCP_TRACE"
    _NOT_FOUND_HINTS = ("not found", "no such file", "enoent")
    _NOT_DIRECTORY_HINTS = ("not a directory", "directory expected")
    _IS_DIRECTORY_HINTS = ("is a directory", "expected file")
    _PERMISSION_HINTS = ("permission denied", "eacces", "operation not permitted")

    def __init__(self) -> None:
        self._settings: MCPConnectionSettings | None = None

    def open(self, settings: MCPConnectionSettings) -> None:
        """Store connection settings; the server is launched on tool execution."""
        if not settings.server_command:
            raise ValueError("MCP server command is required.")
        self._settings = settings

    def close(self) -> None:
        """Clear connection settings for this transport."""
        self._settings = None

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call a filesystem tool through the stdio MCP server."""
        if self._settings is None:
            raise RuntimeError("MCP stdio transport is not configured.")

        command = self._build_helper_command()
        payload = {
            "server_command": self._settings.server_command,
            "server_env": self._settings.env or {},
            "tool_name": tool_name,
            "arguments": arguments,
            "timeout_seconds": self._settings.timeout_seconds,
        }

        helper_env = dict(os.environ)
        if self._settings.env:
            helper_env.update(self._settings.env)

        helper_cwd = str(Path(__file__).resolve().parents[2])
        trace_enabled = self._trace_enabled()

        if trace_enabled:
            self._emit_trace("request", payload)

        try:
            process = subprocess.run(
                command,
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                cwd=helper_cwd,
                env=helper_env,
                timeout=max(2.0, self._settings.timeout_seconds + 2.0),
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError(
                f"Timed out waiting for MCP response for tool '{tool_name}'."
            ) from exc
        except OSError as exc:
            raise OSError(f"Unable to start helper process: {exc}") from exc

        output = process.stdout.strip()
        if not output:
            message = process.stderr.strip() or "MCP helper produced no output."
            self._raise_mapped_error(RuntimeError(message), arguments)

        try:
            response = json.loads(output)
        except json.JSONDecodeError as exc:
            message = process.stderr.strip() or output[:200]
            raise RuntimeError(f"Invalid MCP helper response: {message}") from exc

        if trace_enabled:
            self._emit_trace("response", response)

        if not response.get("ok", False):
            error_message = str(response.get("error", "Unknown MCP helper error"))
            self._raise_mapped_error(RuntimeError(error_message), arguments)

        result_payload = response.get("result")
        if tool_name in {"read_file", "list_directory"}:
            self._raise_mapped_error_from_result(tool_name, result_payload, arguments)

        return self._normalize_mcp_result(result_payload)

    def _trace_enabled(self) -> bool:
        """Return whether trace output should be emitted for MCP requests."""
        if self._settings and self._settings.env:
            value = self._settings.env.get(self._TRACE_ENV_VAR)
            if isinstance(value, str) and value.strip().lower() not in {
                "",
                "0",
                "false",
                "no",
            }:
                return True

        value = os.getenv(self._TRACE_ENV_VAR, "")
        return value.strip().lower() not in {"", "0", "false", "no"}

    @staticmethod
    def _emit_trace(kind: str, payload: Any) -> None:
        """Emit a compact JSON trace line to stderr for debugging and review evidence."""
        print(
            f"[codeinsight-mcp] {kind}: {json.dumps(payload, ensure_ascii=True, default=str)}",
            file=sys.stderr,
        )

    @staticmethod
    def _build_helper_command() -> list[str]:
        """Build the Python command that runs an isolated MCP SDK tool call."""
        helper_script = "\n".join(
            [
                "import asyncio",
                "import json",
                "import os",
                "import sys",
                "",
                "async def _run() -> int:",
                "    payload = json.loads(sys.stdin.read())",
                "    try:",
                "        from mcp import ClientSession, StdioServerParameters",
                "        from mcp.client.stdio import stdio_client",
                "    except Exception as exc:",
                "        print(json.dumps({'ok': False, 'error': f'MCP SDK import failed: {exc}'}))",
                "        return 1",
                "",
                "    env = dict(os.environ)",
                "    env.update(payload.get('server_env') or {})",
                "",
                "    params = StdioServerParameters(",
                "        command=payload['server_command'][0],",
                "        args=payload['server_command'][1:],",
                "        env=env,",
                "    )",
                "",
                "    timeout_seconds = float(payload.get('timeout_seconds', 10.0))",
                "",
                "    try:",
                "        async with stdio_client(params) as (read_stream, write_stream):",
                "            async with ClientSession(read_stream, write_stream) as session:",
                "                await asyncio.wait_for(session.initialize(), timeout=timeout_seconds)",
                "                result = await asyncio.wait_for(",
                "                    session.call_tool(payload['tool_name'], payload.get('arguments') or {}),",
                "                    timeout=timeout_seconds,",
                "                )",
                "",
                "                structured = getattr(result, 'structuredContent', None)",
                "                if structured is not None:",
                "                    print(json.dumps({'ok': True, 'result': structured}))",
                "                    return 0",
                "",
                "                content = getattr(result, 'content', None)",
                "                if isinstance(content, list):",
                "                    parts = []",
                "                    for item in content:",
                "                        if isinstance(item, dict):",
                "                            text = item.get('text')",
                "                        else:",
                "                            text = getattr(item, 'text', None)",
                "                        if isinstance(text, str):",
                "                            parts.append(text)",
                "                    if len(parts) == 1:",
                "                        print(json.dumps({'ok': True, 'result': parts[0]}))",
                "                        return 0",
                "                    if parts:",
                "                        print(json.dumps({'ok': True, 'result': '\\n'.join(parts)}))",
                "                        return 0",
                "",
                "                print(json.dumps({'ok': True, 'result': str(result)}))",
                "                return 0",
                "    except Exception as exc:",
                "        print(json.dumps({'ok': False, 'error': str(exc)}))",
                "        return 1",
                "",
                "raise SystemExit(asyncio.run(_run()))",
            ]
        )

        return [sys.executable, "-c", helper_script]

    def _raise_mapped_error(self, exc: Exception, arguments: dict[str, Any]) -> None:
        """Map common MCP server/tool failures into user-facing path exceptions."""
        message = str(exc)
        lowered = message.lower()
        raw_path = arguments.get("path")
        path = str(raw_path) if isinstance(raw_path, str) else ""

        if any(hint in lowered for hint in self._NOT_FOUND_HINTS):
            raise FileNotFoundError(path or message) from exc
        if any(hint in lowered for hint in self._NOT_DIRECTORY_HINTS):
            raise NotADirectoryError(path or message) from exc
        if any(hint in lowered for hint in self._IS_DIRECTORY_HINTS):
            raise IsADirectoryError(path or message) from exc
        if any(hint in lowered for hint in self._PERMISSION_HINTS):
            raise PermissionError(path or message) from exc
        if "invalid" in lowered and "path" in lowered:
            raise ValueError("Invalid path format") from exc

        raise RuntimeError(message) from exc

    def _raise_mapped_error_from_result(
        self, tool_name: str, result: Any, arguments: dict[str, Any]
    ) -> None:
        """Convert server-returned error text into the expected file/path exceptions."""
        if isinstance(result, str):
            lowered = result.lower()
            if any(hint in lowered for hint in self._NOT_FOUND_HINTS):
                raise FileNotFoundError(str(arguments.get("path", "")))
            if any(hint in lowered for hint in self._NOT_DIRECTORY_HINTS):
                raise NotADirectoryError(str(arguments.get("path", "")))
            if any(hint in lowered for hint in self._IS_DIRECTORY_HINTS):
                raise IsADirectoryError(str(arguments.get("path", "")))
            if any(hint in lowered for hint in self._PERMISSION_HINTS):
                raise PermissionError(str(arguments.get("path", "")))

        if isinstance(result, dict):
            error_message = str(result.get("error", "")).lower()
            if error_message:
                if any(hint in error_message for hint in self._NOT_FOUND_HINTS):
                    raise FileNotFoundError(str(arguments.get("path", "")))
                if any(hint in error_message for hint in self._NOT_DIRECTORY_HINTS):
                    raise NotADirectoryError(str(arguments.get("path", "")))
                if any(hint in error_message for hint in self._IS_DIRECTORY_HINTS):
                    raise IsADirectoryError(str(arguments.get("path", "")))
                if any(hint in error_message for hint in self._PERMISSION_HINTS):
                    raise PermissionError(str(arguments.get("path", "")))

    @staticmethod
    def _normalize_mcp_result(result: Any) -> Any:
        """Extract a useful payload from MCP SDK result shapes."""
        structured = getattr(result, "structuredContent", None)
        if structured is not None:
            return structured

        content = getattr(result, "content", None)
        if isinstance(content, list):
            text_parts: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        text_parts.append(text)
                else:
                    text = getattr(item, "text", None)
                    if isinstance(text, str):
                        text_parts.append(text)

            if len(text_parts) == 1:
                return text_parts[0]
            if text_parts:
                return "\n".join(text_parts)

        return result


class FilesystemMCPClient(MCPClient):
    """High-level helper methods for a filesystem MCP server."""

    def list_directory(self, path: str) -> Any:
        """Return recursive directory entries for the provided path."""
        root_path = str(Path(path).expanduser().resolve(strict=False))
        entries = self._collect_directory_entries(root_path, depth=0)
        return {
            "path": root_path,
            "type": "directory",
            "entries": entries,
        }

    def read_file(self, path: str) -> Any:
        """Return file contents for the provided path."""
        resolved_path = str(Path(path).expanduser().resolve(strict=False))
        raw = self.call_tool("read_file", {"path": resolved_path})

        if isinstance(raw, dict) and "content" in raw:
            content = str(raw.get("content", ""))
            extension = str(raw.get("extension") or Path(path).suffix.lower())
            is_binary = bool(raw.get("is_binary", False))
            size_bytes = int(raw.get("size_bytes", len(content.encode("utf-8"))))
            line_count = int(
                raw.get("line_count", content.count("\n") + (1 if content else 0))
            )
            return {
                "path": str(raw.get("path") or resolved_path),
                "content": content,
                "extension": extension,
                "is_binary": is_binary,
                "size_bytes": size_bytes,
                "line_count": line_count,
            }

        content = str(raw)
        extension = Path(resolved_path).suffix.lower()
        return {
            "path": resolved_path,
            "content": content,
            "extension": extension,
            "is_binary": False,
            "size_bytes": len(content.encode("utf-8")),
            "line_count": content.count("\n") + (1 if content else 0),
        }

    def analyze_project(self, path: str) -> Any:
        """Return high-level project analysis for the provided path."""
        return self.call_tool("analyze_project", {"path": path})

    def get_file_metadata(self, path: str) -> Any:
        """Return metadata for the provided file path."""
        return self.call_tool("get_file_metadata", {"path": path})

    def _collect_directory_entries(
        self, path: str, depth: int, max_depth: int = 8
    ) -> list[dict[str, Any]]:
        """Recursively call list_directory and normalize MCP filesystem output."""
        if depth > max_depth:
            return []

        raw = self.call_tool("list_directory", {"path": path})
        entries = self._normalize_directory_entries(path, raw)

        for entry in entries:
            if entry.get("type") != "directory":
                continue

            child_path = str(Path(path) / str(entry.get("name", "")))
            try:
                entry["entries"] = self._collect_directory_entries(
                    child_path, depth + 1, max_depth=max_depth
                )
            except (FileNotFoundError, NotADirectoryError, PermissionError, ValueError):
                entry["entries"] = []

        return entries

    def _normalize_directory_entries(
        self, base_path: str, payload: Any
    ) -> list[dict[str, Any]]:
        """Normalize different MCP list_directory result formats into entry dictionaries."""
        if isinstance(payload, dict):
            for key in ("entries", "children"):
                children = payload.get(key)
                if isinstance(children, list):
                    return self._normalize_entry_list(base_path, children)

        if isinstance(payload, list):
            return self._normalize_entry_list(base_path, payload)

        if isinstance(payload, str):
            return self._parse_directory_text(base_path, payload)

        text = getattr(payload, "text", None)
        if isinstance(text, str):
            return self._parse_directory_text(base_path, text)

        return []

    def _normalize_entry_list(
        self, base_path: str, payload: list[Any]
    ) -> list[dict[str, Any]]:
        """Normalize dictionary-based entry payloads from MCP responses."""
        entries: list[dict[str, Any]] = []

        for item in payload:
            if not isinstance(item, dict):
                continue

            name = str(item.get("name") or item.get("path") or "").strip()
            if not name:
                continue

            entry_type = str(item.get("type") or "file").lower()
            if entry_type not in {"file", "directory"}:
                entry_type = "directory" if name.endswith("/") else "file"

            clean_name = name.rstrip("/")
            entries.append(
                {
                    "name": clean_name,
                    "path": str(item.get("path") or Path(base_path) / clean_name),
                    "type": entry_type,
                }
            )

        return self._sort_entries(entries)

    def _parse_directory_text(self, base_path: str, text: str) -> list[dict[str, Any]]:
        """Parse plain-text directory listings into structured entries."""
        entries: list[dict[str, Any]] = []

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            match = re.match(r"^\[(DIR|FILE)\]\s+(.+)$", line, flags=re.IGNORECASE)
            if match:
                entry_type = "directory" if match.group(1).upper() == "DIR" else "file"
                name = match.group(2).strip().rstrip("/")
            else:
                cleaned = line.lstrip("-* ").strip()
                if not cleaned:
                    continue
                entry_type = "directory" if cleaned.endswith("/") else "file"
                name = cleaned.rstrip("/")

            if not name or name in {".", ".."}:
                continue

            entries.append(
                {
                    "name": name,
                    "path": str(Path(base_path) / name),
                    "type": entry_type,
                }
            )

        return self._sort_entries(entries)

    @staticmethod
    def _sort_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Sort entries so directories appear before files."""
        return sorted(
            entries,
            key=lambda entry: (
                entry.get("type") != "directory",
                str(entry.get("name", "")).lower(),
            ),
        )


def create_filesystem_client(root_path: str | None = None) -> FilesystemMCPClient:
    """Create a filesystem client backed by the external stdio MCP server."""
    resolved_root = Path(
        root_path or os.getenv("CODEINSIGHT_MCP_ROOT") or Path.cwd()
    ).resolve()
    settings = MCPConnectionSettings(
        server_command=[
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(resolved_root),
        ],
        cwd=str(resolved_root),
        timeout_seconds=12.0,
    )
    return FilesystemMCPClient(settings, StdioFilesystemTransport())


def create_local_filesystem_client() -> FilesystemMCPClient:
    """Create a filesystem client backed by the local filesystem transport."""
    settings = MCPConnectionSettings(server_command=["filesystem-local"])
    return FilesystemMCPClient(settings, LocalFilesystemTransport())
