import pytest
import tempfile
import toml
from pathlib import Path
from unittest.mock import patch
from mcpcli.config import load_config, Config, CONFIG_DIR, CONFIG_FILE


@pytest.fixture
def temp_config_dir(tmp_path):
    return tmp_path / "config" / "mcpcli"


@pytest.fixture
def mock_config_dir(temp_config_dir):
    with patch('mcpcli.config.CONFIG_DIR', temp_config_dir), \
         patch('mcpcli.config.CONFIG_FILE', temp_config_dir / "config.toml"):
        yield


def test_load_config_creates_default_when_missing(mock_config_dir):
    config = load_config()
    assert isinstance(config, Config)
    assert config.ollama.endpoint == "http://localhost:11434"
    assert (CONFIG_DIR / "config.toml").exists()


def test_load_config_loads_existing_file(mock_config_dir, temp_config_dir):
    config_data = {"ollama": {"endpoint": "http://custom:1234"}}
    config_file = temp_config_dir / "config.toml"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w') as f:
        toml.dump(config_data, f)

    config = load_config()
    assert config.ollama.endpoint == "http://custom:1234"


def test_load_config_handles_malformed_file(mock_config_dir, temp_config_dir):
    config_file = temp_config_dir / "config.toml"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w') as f:
        f.write("invalid toml content")

    config = load_config()
    assert isinstance(config, Config)
    assert config.ollama.endpoint == "http://localhost:11434"  # defaults