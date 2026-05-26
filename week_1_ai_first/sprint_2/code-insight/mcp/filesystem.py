"""Filesystem-oriented MCP helpers built on top of MCPClient."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .client import MCPClient, MCPConnectionSettings


class LocalFilesystemTransport:
    """Simple local transport used to adapt filesystem access through MCP client APIs."""

    def open(self, settings: MCPConnectionSettings) -> None:
        """Open the transport connection."""

    def close(self) -> None:
        """Close the transport connection."""

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute a filesystem tool request."""
        if tool_name != "list_directory":
            raise ValueError(f"Unsupported tool: {tool_name}")

        return self._list_directory(arguments["path"])

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
