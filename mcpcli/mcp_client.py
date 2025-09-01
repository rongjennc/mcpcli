import httpx
import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, AsyncGenerator, List

@asynccontextmanager
async def streamablehttp_client(url: str) -> AsyncGenerator[httpx.AsyncClient, None]:
    """A context manager for an httpx.AsyncClient."""
    async with httpx.AsyncClient(base_url=url) as client:
        yield client

class ClientSession:
    """A session for interacting with an MCP server."""
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def initialize(self):
        """
        In a real scenario, this might ping a /health or /initialize endpoint.
        For now, we'll just assume the server is ready.
        """
        pass

    async def list_tools(self) -> List[str]:
        """
        Lists available tools from mcp.json.
        """
        try:
            with open("mcp.json", 'r') as f:
                mcp_config = json.load(f)
            tools = [server["name"] for server in mcp_config.get("servers", [])]
            logging.info(f"Available tools: {tools}")
            return tools
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load tools from mcp.json: {e}")
            return []

    async def invoke(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Invokes a tool on the MCP server."""
        try:
            with open("mcp.json", 'r') as f:
                mcp_config = json.load(f)
            server_info = next((s for s in mcp_config.get("servers", []) if s["name"] == tool_name), None)
            if not server_info:
                return f"Error: Tool '{tool_name}' not found in mcp.json"
            path = server_info.get("path", "/invoke")
            response = await self.client.post(
                path,
                json=parameters,
                timeout=30.0
            )
            response.raise_for_status()
            return json.dumps(response.json())
        except httpx.RequestError as e:
            return f"Error invoking tool '{tool_name}': {e}"

async def run_tool(tool_name: str, query: str) -> str:
    """
    Connects to an MCP server and runs a tool using the custom client.
    """
    logging.info(f"Running tool '{tool_name}' with query: '{query}'")
    try:
        with open("mcp.json", 'r') as f:
            mcp_config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load mcp.json: {e}")
        return "Error: mcp.json not found or is invalid."

    server_info = next((s for s in mcp_config.get("servers", []) if s["name"] == tool_name), None)

    if not server_info:
        return f"Error: MCP server for tool '{tool_name}' not found in mcp.json"

    url = server_info["url"]

    try:
        async with streamablehttp_client(url) as client:
            session = ClientSession(client)
            await session.initialize()

            tools = await session.list_tools()
            if tool_name not in tools:
                return f"Error: Tool '{tool_name}' not found on server {url}"

            result = await session.invoke(tool_name, {"query": query})
            return result
    except Exception as e:
        return f"An unexpected error occurred while running tool '{tool_name}': {e}"
