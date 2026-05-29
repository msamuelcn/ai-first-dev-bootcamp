import os
from types import SimpleNamespace
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codeinsight.mcp.filesystem import (
    FilesystemMCPClient,
    MCPConnectionSettings,
    StdioFilesystemTransport,
    create_filesystem_client,
    create_local_filesystem_client,
)


def test_local_mcp_connection_object():
    client = create_local_filesystem_client()

    assert client is not None
    assert client.is_connected is False


def test_external_mcp_client_uses_real_server_command():
    client = create_filesystem_client()

    assert client is not None
    assert client.is_connected is False
    assert client._settings.server_command[0] == "npx"
    assert "@modelcontextprotocol/server-filesystem" in client._settings.server_command


def test_stdio_transport_emits_trace_for_request_and_response(monkeypatch, capsys):
    transport = StdioFilesystemTransport()
    settings = MCPConnectionSettings(
        server_command=["npx", "-y", "@modelcontextprotocol/server-filesystem", "."],
        env={"CODEINSIGHT_MCP_TRACE": "1"},
    )
    client = FilesystemMCPClient(settings, transport)

    def fake_run(*args, **kwargs):
        return SimpleNamespace(
            stdout='{"ok": true, "result": {"path": ".", "type": "directory", "entries": []}}',
            stderr="",
        )

    monkeypatch.setattr(
        "codeinsight.mcp.filesystem.subprocess.run",
        fake_run,
    )

    with client:
        payload = client.list_directory(".")

    captured = capsys.readouterr()

    assert payload["type"] == "directory"
    assert "[codeinsight-mcp] request:" in captured.err
    assert "[codeinsight-mcp] response:" in captured.err
    assert '"tool_name": "list_directory"' in captured.err
    assert '"ok": true' in captured.err


@pytest.mark.integration
def test_external_mcp_list_directory_integration():
    if os.getenv("RUN_MCP_INTEGRATION") != "1":
        pytest.skip("Set RUN_MCP_INTEGRATION=1 to run live MCP integration tests.")

    root = Path(__file__).resolve().parents[1]
    client = create_filesystem_client(root_path=str(root))

    with client:
        payload = client.list_directory(str(root))

    assert isinstance(payload, dict)
    assert payload.get("type") == "directory"
    assert isinstance(payload.get("entries"), list)
