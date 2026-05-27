def test_mcp_connection():
    from codeinsight.mcp.client import MCPClient

    client = MCPClient()

    assert client is not None
