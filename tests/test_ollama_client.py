import pytest
import json
from unittest.mock import patch, AsyncMock
from mcpcli.ollama_client import generate


@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_generate_success(mock_client_class):
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.aiter_lines.return_value = [
        'data: {"response": "Hello", "done": false}',
        'data: {"response": " world", "done": true}'
    ]
    mock_response.raise_for_status = AsyncMock()
    mock_client.stream.return_value.__aenter__.return_value = mock_response
    mock_client_class.return_value = mock_client

    chunks = []
    async for chunk in generate("http://localhost:11434", "llama2", "Test prompt"):
        chunks.append(chunk)

    assert chunks == ["Hello", " world"]


@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_generate_request_error(mock_client_class):
    mock_client = AsyncMock()
    mock_client.stream.side_effect = Exception("Connection error")
    mock_client_class.return_value = mock_client

    chunks = []
    async for chunk in generate("http://localhost:11434", "llama2", "Test prompt"):
        chunks.append(chunk)

    assert "An unexpected error occurred" in chunks[0]