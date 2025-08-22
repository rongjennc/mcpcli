import httpx
import json
from typing import AsyncIterator

async def generate(endpoint: str, model: str, prompt: str) -> AsyncIterator[str]:
    """
    Sends a prompt to the Ollama API and yields the streaming response asynchronously.
    """
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{endpoint.rstrip('/')}/api/generate",
                json={"model": model, "prompt": prompt},
                timeout=None
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            if chunk.get("done"):
                                break
                            yield chunk.get("response", "")
                        except json.JSONDecodeError:
                            continue
    except httpx.RequestError as e:
        yield f"\nError connecting to Ollama at {endpoint}: {e}\n"
    except Exception as e:
        yield f"\nAn unexpected error occurred: {e}\n"
