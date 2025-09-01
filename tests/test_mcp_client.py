import pytest
import json
from unittest.mock import patch, mock_open, AsyncMock
from mcpcli.mcp_client import run_tool, ClientSession


@pytest.fixture
def mock_mcp_json():
    return {
        "servers": [
            {
                "name": "duckduckgo",
                "url": "http://127.0.0.1:8000/mcp",
                "path": "/search"
            }
        ]
    }


@patch('builtins.open', new_callable=mock_open)
@patch('mcpcli.mcp_client.streamablehttp_client')
@pytest.mark.asyncio
async def test_run_tool_success(mock_client, mock_file, mock_mcp_json):
    mock_file.return_value.read.return_value = json.dumps(mock_mcp_json)
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    mock_session.list_tools = AsyncMock(return_value=["duckduckgo"])
    mock_session.invoke = AsyncMock(return_value="search result")
    mock_client.return_value.__aenter__.return_value = mock_session

    result = await run_tool("duckduckgo", "test query")
    assert "search result" in result


@patch('builtins.open', new_callable=mock_open)
@pytest.mark.asyncio
async def test_run_tool_missing_mcp_json(mock_file):
    mock_file.side_effect = FileNotFoundError
    result = await run_tool("duckduckgo", "query")
    assert "mcp.json not found" in result


@patch('builtins.open', new_callable=mock_open)
@patch('mcpcli.mcp_client.streamablehttp_client')
@pytest.mark.asyncio
async def test_run_tool_unknown_tool(mock_client, mock_file, mock_mcp_json):
    mock_mcp_json["servers"][0]["name"] = "othertool"
    mock_file.return_value.read.return_value = json.dumps(mock_mcp_json)
    mock_session = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_session

    result = await run_tool("duckduckgo", "query")
    assert "not found in mcp.json" in result