"""Filesystem-oriented MCP helpers built on top of MCPClient."""

from __future__ import annotations

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


class FilesystemMCPClient(MCPClient):
    """High-level helper methods for a filesystem MCP server."""

    def list_directory(self, path: str) -> Any:
        """Return directory entries for the provided path."""
        return self.call_tool("list_directory", {"path": path})

    def read_file(self, path: str) -> Any:
        """Return file contents for the provided path."""
        return self.call_tool("read_file", {"path": path})

    def analyze_project(self, path: str) -> Any:
        """Return high-level project analysis for the provided path."""
        return self.call_tool("analyze_project", {"path": path})

    def get_file_metadata(self, path: str) -> Any:
        """Return metadata for the provided file path."""
        return self.call_tool("get_file_metadata", {"path": path})


def create_local_filesystem_client() -> FilesystemMCPClient:
    """Create a filesystem client backed by the local filesystem transport."""
    settings = MCPConnectionSettings(server_command=["filesystem-local"])
    return FilesystemMCPClient(settings, LocalFilesystemTransport())
