import requests
import json
from typing import Iterator, Dict, Any

def generate(endpoint: str, model: str, prompt: str) -> Iterator[str]:
    """
    Sends a prompt to the Ollama API and yields the streaming response.
    """
    try:
        response = requests.post(
            f"{endpoint.rstrip('/')}/api/generate",
            json={"model": model, "prompt": prompt},
            stream=True
        )
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if chunk.get("done"):
                        break
                    yield chunk.get("response", "")
                except json.JSONDecodeError:
                    # Handle potential non-JSON lines, if any
                    continue
    except requests.exceptions.RequestException as e:
        yield f"\nError connecting to Ollama at {endpoint}: {e}\n"
    except Exception as e:
        yield f"\nAn unexpected error occurred: {e}\n"
