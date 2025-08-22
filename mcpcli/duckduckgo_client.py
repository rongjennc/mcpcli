import requests
from typing import Dict, Any

def search(endpoint: str, query: str) -> str:
    """
    Sends a search query to the DuckDuckGo MCP server.
    """
    try:
        response = requests.post(
            f"{endpoint.rstrip('/')}/search",
            json={"query": query}
        )
        response.raise_for_status()
        return response.json().get("results", "No results found.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to DuckDuckGo MCP server at {endpoint}: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
