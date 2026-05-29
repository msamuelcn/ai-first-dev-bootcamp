from argparse import Namespace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codeinsight.commands import summarize
from codeinsight.mcp.client import MCPConnectionError


def test_summarize_requires_mcp_connection(monkeypatch, capsys):
    def raise_connection_error():
        raise MCPConnectionError("server unavailable")

    monkeypatch.setattr(summarize, "create_filesystem_client", raise_connection_error)

    summarize.handle(Namespace(file="codeinsight/main.py"))

    captured = capsys.readouterr()

    assert "Unable to connect to MCP server" in captured.out
    assert "server unavailable" not in captured.out.lower()
