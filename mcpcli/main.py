import typer
import asyncio
import json
from mcpcli import config, ollama_client, mcp_client

app = typer.Typer()

@app.command()
def version():
    """
    Prints the version of mcpcli.
    """
    print("mcpcli 0.1.0")

@app.command()
def chat(
    prompt: str = typer.Option(..., "--prompt", "-p", help="The prompt to start the chat with."),
    model: str = typer.Option("llama2", help="The Ollama model to use."),
    max_loops: int = typer.Option(5, help="The maximum number of tool-use loops to prevent infinite cycles.")
):
    """
    Starts a chat session with the LLM, allowing it to use configured tools.
    """
    try:
        asyncio.run(amain(prompt, model, max_loops))
    except KeyboardInterrupt:
        print("\nChat interrupted by user.")

async def amain(prompt: str, model: str, max_loops: int):
    conf = config.load_config()
    ollama_endpoint = conf.get("ollama", {}).get("endpoint")
    if not ollama_endpoint:
        print("Ollama endpoint not configured. Please check your config.toml.")
        raise typer.Exit(code=1)

    # Initial prompt includes instructions for the LLM on how to use tools.
    current_prompt = (
        "You are a helpful assistant. You have access to tools. "
        "To use a tool, you MUST output a single line containing only 'MCP:' followed by a valid JSON object. "
        "The JSON object must have a 'tool' key and a 'query' key. "
        "For example: MCP:{\"tool\": \"duckduckgo\", \"query\": \"who is the president of the united states?\"}\n\n"
        f"User: {prompt}"
    )

    print(f"Starting chat with model '{model}'...\n")

    for i in range(max_loops):
        print("Thinking...", end="", flush=True)

        full_response = ""
        async for chunk in ollama_client.generate(ollama_endpoint, model, current_prompt):
            full_response += chunk

        print("\r" + " " * 11 + "\r", end="")

        if "MCP:" in full_response:
            lines = full_response.splitlines()
            mcp_line = next((line for line in lines if line.startswith("MCP:")), None)

            if not mcp_line:
                print("Final Answer (MCP command not found on a single line):")
                print(full_response)
                break

            try:
                mcp_command_str = mcp_line.split("MCP:", 1)[1].strip()
                mcp_command = json.loads(mcp_command_str)

                tool = mcp_command.get("tool")
                query = mcp_command.get("query")

                if not tool or not query:
                    raise ValueError("MCP command must have 'tool' and 'query' keys.")

                print(f"LLM is using tool '{tool}' with query: '{query}'")
                tool_result = await mcp_client.run_tool(tool, query)

                # Append the tool result to the prompt for the next iteration
                current_prompt += f"\n\nTool Response for '{query}':\n{tool_result}"

            except (json.JSONDecodeError, IndexError, ValueError) as e:
                print(f"\nCould not parse or execute MCP command: {e}")
                print("Final Answer (due to error):")
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
