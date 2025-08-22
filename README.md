# MCPCLI

A terminal-based client that orchestrates communication between a local Large Language Model (Ollama) and tool providers using the Model Context Protocol (MCP).

## How It Works

`mcpcli` facilitates a conversation between an LLM and various tools. The LLM can request a tool action by outputting a special JSON command, which `mcpcli` then executes by making HTTP requests to the appropriate MCP server.

## Setup

### 1. Install Dependencies
This project uses Poetry for dependency management.
```bash
poetry install
```

### 2. Run the DuckDuckGo MCP Server
This tool requires a local DuckDuckGo MCP server. You can install and run it in a separate terminal:
```bash
uv pip install duckduckgo-mcp-server
uvx duckduckgo-mcp-server
```
The server will run on `http://127.0.0.1:8000`.

### 3. Ollama
Ensure you have [Ollama](https://ollama.ai/) installed and running.

## Usage

```bash
poetry run mcpcli chat --prompt "Your prompt for the LLM"
```
