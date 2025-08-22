import toml
from pathlib import Path
from typing import Any, Dict

# Define the config path
CONFIG_DIR = Path.home() / ".config" / "mcpcli"
CONFIG_FILE = CONFIG_DIR / "config.toml"

# Default config structure
DEFAULT_CONFIG: Dict[str, Any] = {
    "ollama": {"endpoint": "http://localhost:11434"},
    "mcp_servers": {
        "duckduckgo": {"endpoint": "http://localhost:8000"} # Example
    }
}

def ensure_config_dir_exists():
    """Ensures the config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Loads the configuration from the TOML file."""
    ensure_config_dir_exists()
    if not CONFIG_FILE.is_file():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    config_data = {}
    try:
        with open(CONFIG_FILE, 'r') as f:
            config_data = toml.load(f)
    except (toml.TomlDecodeError, FileNotFoundError):
        pass # Will be handled by the merge below

    # Merge with defaults to ensure all keys are present
    needs_update = False
    if "ollama" not in config_data:
        config_data["ollama"] = DEFAULT_CONFIG["ollama"]
        needs_update = True

    if "mcp_servers" not in config_data:
        config_data["mcp_servers"] = DEFAULT_CONFIG["mcp_servers"]
        needs_update = True

    if needs_update:
        save_config(config_data)

    return config_data

def save_config(config_data: Dict[str, Any]):
    """Saves the configuration data to the TOML file."""
    ensure_config_dir_exists()
    with open(CONFIG_FILE, 'w') as f:
        toml.dump(config_data, f)
