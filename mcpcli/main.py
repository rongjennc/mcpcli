import typer
from mcpcli import config, ollama_client, duckduckgo_client
import json

app = typer.Typer()

@app.command()
def version():
    """
    Prints the version of mcpcli.
    """
    print("mcpcli 0.1.0")

@app.command()
def chat(
    prompt: str = typer.Argument(..., help="The prompt to start the chat with."),
    model: str = typer.Option("llama2", help="The Ollama model to use."),
    max_loops: int = typer.Option(5, help="The maximum number of tool-use loops to prevent infinite cycles.")
):
    """
    Starts a chat session with the LLM, allowing it to use configured tools.
    """
    conf = config.load_config()
    ollama_endpoint = conf.get("ollama", {}).get("endpoint")
    if not ollama_endpoint:
        print("Ollama endpoint not configured. Please check your config file.")
        raise typer.Exit(code=1)

    current_prompt = f"You are a helpful assistant. You can use tools to answer questions. To use a tool, output 'MCP:' followed by a JSON object with 'tool' and 'query' keys. For example: MCP:{{\"tool\": \"duckduckgo\", \"query\": \"who is the president of the united states?\"}}\n\nUser: {prompt}"

    print(f"Starting chat with model '{model}'...\n")

    for i in range(max_loops):
        print("Thinking...", end="", flush=True)
        full_response = ""
        for chunk in ollama_client.generate(ollama_endpoint, model, current_prompt):
            full_response += chunk

        print("\r" + " " * 11 + "\r", end="") # Clear "Thinking..."

        if "MCP:" in full_response:
            try:
                mcp_command_str = full_response.split("MCP:")[1].strip()
                mcp_command = json.loads(mcp_command_str)

                tool = mcp_command.get("tool")
                query = mcp_command.get("query")

                if tool == "duckduckgo":
                    print(f"LLM is using DuckDuckGo to search for: '{query}'")
                    ddg_endpoint = conf.get("mcp_servers", {}).get("duckduckgo", {}).get("endpoint")
                    if not ddg_endpoint:
                        print("DuckDuckGo MCP server not configured.")
                        tool_result = "Error: DuckDuckGo MCP server not configured."
                    else:
                        tool_result = duckduckgo_client.search(ddg_endpoint, query)

                    current_prompt += f"\nTool Response: {tool_result}"
                else:
                    print(f"Unknown tool: {tool}")
                    current_prompt += f"\nError: Unknown tool '{tool}'"

            except (json.JSONDecodeError, IndexError) as e:
                print(f"Could not parse MCP command: {e}")
                print("Final Answer (due to parsing error):")
                print(full_response)
                break
        else:
            print("Final Answer:")
            print(full_response)
            break
    else:
        print("\nMaximum tool-use loops reached. Exiting.")


if __name__ == "__main__":
    app()
