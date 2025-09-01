import toml
import logging
from pathlib import Path
from typing import Any, Dict
from pydantic import BaseModel, ValidationError

class OllamaConfig(BaseModel):
    endpoint: str = "http://localhost:11434"

class Config(BaseModel):
    ollama: OllamaConfig = OllamaConfig()

CONFIG_DIR = Path.home() / ".config" / "mcpcli"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {"ollama": {"endpoint": "http://localhost:11434"}}

def load_config() -> Config:
    """
    Loads the configuration from the TOML file.
    If the file doesn't exist, it creates it with default values.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.is_file():
        logging.info(f"Creating default config file at {CONFIG_FILE}")
        with open(CONFIG_FILE, 'w') as f:
            toml.dump(DEFAULT_CONFIG, f)
        return Config(**DEFAULT_CONFIG)

    # In case the file is empty or malformed
    try:
        config_dict = toml.load(CONFIG_FILE)
        config = Config(**config_dict)
        logging.info("Config loaded and validated successfully")
        return config
    except (toml.TomlDecodeError, ValidationError) as e:
        logging.warning(f"Config file malformed or invalid, using defaults: {e}")
        return Config(**DEFAULT_CONFIG)
