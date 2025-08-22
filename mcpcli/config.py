import toml
from pathlib import Path
from typing import Any, Dict

# Define the config path
CONFIG_DIR = Path.home() / ".config" / "mcpcli"
CONFIG_FILE = CONFIG_DIR / "config.toml"

# Default config structure
DEFAULT_CONFIG: Dict[str, Dict[str, Any]] = {
    "accounts": {},
    "llms": {}
}

def ensure_config_dir_exists():
    """Ensures the config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Loads the configuration from the TOML file."""
    ensure_config_dir_exists()
    if not CONFIG_FILE.is_file():
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, 'r') as f:
            return toml.load(f)
    except toml.TomlDecodeError:
        return DEFAULT_CONFIG

def save_config(config_data: Dict[str, Any]):
    """Saves the configuration data to the TOML file."""
    ensure_config_dir_exists()
    with open(CONFIG_FILE, 'w') as f:
        toml.dump(config_data, f)

def add_account(name: str, jid: str, password: str):
    """Adds a new account to the config."""
    config = load_config()
    if "accounts" not in config:
        config["accounts"] = {}
    config["accounts"][name] = {"jid": jid, "password": password}
    save_config(config)

def add_llm(name: str, account: str, room_jid: str, nickname: str):
    """Adds a new LLM profile to the config."""
    config = load_config()
    if "llms" not in config:
        config["llms"] = {}
    config["llms"][name] = {
        "account": account,
        "room_jid": room_jid,
        "nickname": nickname
    }
    save_config(config)
