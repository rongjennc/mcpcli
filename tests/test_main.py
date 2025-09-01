import pytest
from unittest.mock import patch
from typer.testing import CliRunner
from mcpcli.main import app, __version__


runner = CliRunner()


def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


@patch('mcpcli.main.config.load_config')
@patch('mcpcli.main.ollama_client.generate')
@patch('mcpcli.main.mcp_client.run_tool')
def test_chat_command_no_tool(mock_run_tool, mock_generate, mock_load_config):
    mock_load_config.return_value.ollama.endpoint = "http://localhost:11434"
    mock_generate.return_value = ["Final answer"]

    result = runner.invoke(app, ["chat", "--prompt", "Hello"])
    assert result.exit_code == 0
    assert "Final answer" in result.output


@patch('mcpcli.main.config.load_config')
def test_chat_command_no_endpoint(mock_load_config):
    mock_load_config.return_value.ollama.endpoint = ""

    result = runner.invoke(app, ["chat", "--prompt", "Hello"])
    assert result.exit_code == 1
    assert "Ollama endpoint not configured" in result.output