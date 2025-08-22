import toml
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path.home() / ".config" / "mcpcli"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {"ollama": {"endpoint": "http://localhost:11434"}}

def load_config() -> Dict[str, Any]:
    """
    Loads the configuration from the TOML file.
    If the file doesn't exist, it creates it with default values.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.is_file():
        with open(CONFIG_FILE, 'w') as f:
            toml.dump(DEFAULT_CONFIG, f)
        return DEFAULT_CONFIG

    # In case the file is empty or malformed
    try:
        return toml.load(CONFIG_FILE)
    except toml.TomlDecodeError:
        return DEFAULT_CONFIG
