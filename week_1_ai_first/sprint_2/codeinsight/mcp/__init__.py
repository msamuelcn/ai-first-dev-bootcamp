"""MCP integration layer for Code Insight CLI."""

from .client import (
    MCPClient,
    MCPClientError,
    MCPConnectionError,
    MCPConnectionSettings,
    MCPOperationError,
    MCPTransport,
)
from .filesystem import (
    FilesystemMCPClient,
    LocalFilesystemTransport,
    StdioFilesystemTransport,
    create_filesystem_client,
    create_local_filesystem_client,
)

__all__ = [
    "MCPClient",
    "MCPClientError",
    "MCPConnectionError",
    "MCPConnectionSettings",
    "MCPOperationError",
    "MCPTransport",
    "FilesystemMCPClient",
    "LocalFilesystemTransport",
    "StdioFilesystemTransport",
    "create_filesystem_client",
    "create_local_filesystem_client",
]
