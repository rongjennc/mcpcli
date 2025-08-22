# MCPCLI

A terminal-based client for interacting with local Large Language Models (LLMs) like Ollama and tool providers that adhere to the Model Context Protocol (MCP).

## Features

*   Connect to a local Ollama instance.
*   Integrate with tool providers (MCP servers) like a local DuckDuckGo search server.
*   Orchestrate communication between the LLM and its tools.

## How it Works

`mcpcli` acts as an orchestrator between a Large Language Model (like Ollama) and various tools (called MCP servers). The communication follows a simple "Model Context Protocol" (MCP).

When the LLM needs to use a tool, it outputs a special JSON object on a single line, prefixed with `MCP:`. For example:
```
MCP:{"tool": "duckduckgo", "query": "What is the capital of France?"}
```
`mcpcli` intercepts this output, calls the appropriate MCP server, and feeds the result back to the LLM.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd mcpcli
    ```

2.  **Install dependencies using Poetry:**
    Make sure you have [Poetry](https://python-poetry.org/) installed.
    ```bash
    poetry install
    ```

## Setup

### 1. Ollama

Ensure you have [Ollama](https://ollama.ai/) installed and running. `mcpcli` will connect to it at its default address (`http://localhost:11434`).

### 2. DuckDuckGo MCP Server

`mcpcli` is designed to work with a local DuckDuckGo search server. You will need to set this up separately.

**(Note: The DuckDuckGo MCP server is a separate project that you need to create. Here is a conceptual example of what a simple Flask-based server might look like.)**

**Example `ddg_server.py`:**
```python
from flask import Flask, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Query not provided"}), 400

    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(port=8000)
```

You would need to install `flask` and `duckduckgo-search`, then run this server in a separate terminal: `python ddg_server.py`.

## Usage

(Instructions to be added)
