"""Filesystem-oriented MCP helpers built on top of MCPClient."""

from __future__ import annotations

from typing import Any

from .client import MCPClient


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
