from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codeinsight.mcp.filesystem import create_local_filesystem_client


def test_mcp_connection():
    client = create_local_filesystem_client()

    assert client is not None
    assert client.is_connected is False
