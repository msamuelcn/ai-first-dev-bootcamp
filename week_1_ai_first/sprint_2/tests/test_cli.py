from argparse import Namespace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codeinsight.commands import summarize
from codeinsight.mcp.client import MCPConnectionError, MCPOperationError


def test_summarize_requires_mcp_connection(monkeypatch, capsys):
    def raise_connection_error():
        raise MCPConnectionError("server unavailable")

    monkeypatch.setattr(summarize, "create_filesystem_client", raise_connection_error)

    summarize.handle(Namespace(file="codeinsight/main.py"))

    captured = capsys.readouterr()

    assert "Unable to connect to MCP server" in captured.out
    assert "server unavailable" not in captured.out.lower()


def test_summarize_reports_operation_failure(monkeypatch, capsys):
    def raise_operation_error():
        raise MCPOperationError("read_file tool failed")

    monkeypatch.setattr(summarize, "create_filesystem_client", raise_operation_error)

    summarize.handle(Namespace(file="codeinsight/main.py"))

    captured = capsys.readouterr()

    assert "MCP operation failed: unable to summarize file" in captured.out


def test_summarize_reports_invalid_input(monkeypatch, capsys):
    def raise_invalid_input():
        raise ValueError("invalid path")

    monkeypatch.setattr(summarize, "create_filesystem_client", raise_invalid_input)

    summarize.handle(Namespace(file=""))

    captured = capsys.readouterr()

    assert "Invalid path format" in captured.out
