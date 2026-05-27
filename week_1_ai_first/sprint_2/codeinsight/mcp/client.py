"""Reusable MCP client primitives for server communication."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


class MCPClientError(RuntimeError):
    """Base class for MCP client errors."""


class MCPConnectionError(MCPClientError):
    """Raised when connecting to or disconnecting from MCP fails."""


class MCPOperationError(MCPClientError):
    """Raised when an MCP operation fails."""


@dataclass(frozen=True)
class MCPConnectionSettings:
    """Configuration used to connect to an MCP server."""

    server_command: list[str]
    env: dict[str, str] | None = None
    cwd: str | None = None
    timeout_seconds: float = 10.0


class MCPTransport(Protocol):
    """Low-level transport contract used by MCPClient."""

    def open(self, settings: MCPConnectionSettings) -> None:
        """Open a connection to the MCP server."""

    def close(self) -> None:
        """Close the existing server connection."""

    def call_tool(self, tool_name: str, arguments: Mapping[str, Any]) -> Any:
        """Call a tool on the MCP server and return raw response data."""


class MCPClient:
    """Connection lifecycle and operation wrapper for MCP transports."""

    def __init__(
        self, settings: MCPConnectionSettings, transport: MCPTransport
    ) -> None:
        self._settings = settings
        self._transport = transport
        self._connected = False

    @property
    def is_connected(self) -> bool:
        """Return whether the client currently has an active connection."""
        return self._connected

    def connect(self) -> None:
        """Connect to the MCP server using the configured transport."""
        if self._connected:
            return

        try:
            self._transport.open(self._settings)
            self._connected = True
        except (OSError, TimeoutError, ValueError) as exc:
            raise MCPConnectionError(f"Unable to connect to MCP server: {exc}") from exc
        except Exception as exc:  # pragma: no cover - defensive wrapper
            raise MCPConnectionError(
                f"Unexpected MCP connection failure: {exc}"
            ) from exc

    def disconnect(self) -> None:
        """Disconnect from the MCP server if connected."""
        if not self._connected:
            return

        try:
            self._transport.close()
        except Exception as exc:  # pragma: no cover - defensive wrapper
            raise MCPConnectionError(
                f"Unable to close MCP connection cleanly: {exc}"
            ) from exc
        finally:
            self._connected = False

    def call_tool(self, tool_name: str, arguments: Mapping[str, Any]) -> Any:
        """Call an MCP tool with standardized error handling."""
        if not self._connected:
            raise MCPConnectionError("MCP client is not connected.")

        try:
            return self._transport.call_tool(tool_name=tool_name, arguments=arguments)
        except MCPClientError:
            raise
        except (FileNotFoundError, NotADirectoryError, PermissionError, ValueError):
            raise
        except Exception as exc:  # pragma: no cover - defensive wrapper
            raise MCPOperationError(f"MCP operation failed: {exc}") from exc

    def __enter__(self) -> "MCPClient":
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.disconnect()
