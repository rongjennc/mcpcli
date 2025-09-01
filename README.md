# MCPCLI

A terminal-based client that orchestrates communication between a local Large Language Model (Ollama) and tool providers using the Model Context Protocol (MCP).

## What It Does

MCPCLI enables interactive conversations with a local LLM (via Ollama) that can dynamically use external tools. The LLM can request tool execution by outputting a specific JSON command (e.g., `MCP:{"tool": "duckduckgo", "query": "search term"}`), which MCPCLI parses, executes via HTTP requests to configured MCP servers, and feeds the results back to the LLM for continued conversation. This allows the LLM to access real-time data or perform actions beyond its training, such as web searches.

Currently supports DuckDuckGo search, but is extensible to other MCP-compatible tools.

## Features

- **Asynchronous Communication**: Uses async HTTP for efficient tool calls and LLM streaming.
- **Configurable Tools**: Easily add new tools via `mcp.json` configuration.
- **Logging**: Comprehensive logging for debugging and monitoring.
- **Config Validation**: Uses Pydantic for robust configuration validation.
- **CLI Interface**: Built with Typer for intuitive command-line usage.
- **Extensible**: Modular design for adding new clients or tools.

## Setup

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- [Ollama](https://ollama.ai/) installed and running locally
- A compatible MCP server (e.g., DuckDuckGo MCP server)

### 1. Install Dependencies

```bash
poetry install
```

### 2. Configure Ollama

Ensure Ollama is running. The default endpoint is `http://localhost:11434`. You can customize this in `~/.config/mcpcli/config.toml`:

```toml
[ollama]
endpoint = "http://localhost:11434"
```

### 3. Set Up MCP Servers

Configure tools in `mcp.json` at the project root:

```json
{
  "servers": [
    {
      "name": "duckduckgo",
      "url": "http://127.0.0.1:8000/mcp",
      "path": "/search"
    }
  ]
}
```

To run the DuckDuckGo MCP server:

```bash
uv pip install duckduckgo-mcp-server
uvx duckduckgo-mcp-server
```

The server runs on `http://127.0.0.1:8000` by default.

## Usage

### Start a Chat

```bash
poetry run mcpcli chat --prompt "What is the weather today?" --model llama2 --max-loops 5
```

- `--prompt`: Initial prompt for the LLM
- `--model`: Ollama model to use (default: llama2)
- `--max-loops`: Maximum tool-use loops to prevent infinite cycles (default: 5)

### Other Commands

- `poetry run mcpcli version`: Display the app version

### Example Interaction

```
$ poetry run mcpcli chat --prompt "Search for the latest news on AI"

Starting chat with model 'llama2'...

Thinking...
LLM is using tool 'duckduckgo' with query: 'latest news on AI'
[Tool results displayed]
Final Answer: Based on the search results...
```

## Configuration

- **Config File**: `~/.config/mcpcli/config.toml` (auto-created with defaults)
- **MCP Tools**: `mcp.json` in the project root
- **Logging**: Output to console with timestamps; configurable via Python logging

## Adding New Tools

1. Ensure an MCP server is running for the tool.
2. Add an entry to `mcp.json`:

```json
{
  "name": "newtool",
  "url": "http://example.com/mcp",
  "path": "/endpoint"
}
```

3. The LLM can now request it with `MCP:{"tool": "newtool", "query": "..."}`

## Development

- **Linting**: Run `poetry run flake8` or similar
- **Testing**: Add tests in a `tests/` directory
- **Contributing**: Fork, make changes, submit PR

## License

[Add license if applicable, e.g., MIT]

## Version

0.1.0
