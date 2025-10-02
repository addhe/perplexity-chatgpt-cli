"""Tests for the configuration management."""

import os
import yaml
from pathlib import Path
from unittest.mock import patch

import pytest
from perplexity_cli.core.config import ConfigManager, Config, APIConfig, CLIConfig

@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """Creates a temporary config directory."""
    return tmp_path

def test_load_default_config(temp_config_dir: Path):
    """Tests loading the default configuration."""
    config_manager = ConfigManager(config_dir=temp_config_dir)
    config = config_manager.load_config()

    assert isinstance(config, Config)
    assert isinstance(config.api, APIConfig)
    assert isinstance(config.cli, CLIConfig)
    assert config.api_key is None
    assert config.model == "sonar-pro"

def test_load_config_from_file(temp_config_dir: Path):
    """Tests loading the configuration from a YAML file."""
    config_data = {
        'api': {
            'base_url': 'https://custom.api.com',
            'timeout': 60,
        },
        'cli': {
            'char_delay': 0.1,
        },
        'model': 'custom-model',
        'api_key': 'file-api-key',
    }
    config_path = temp_config_dir / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)

    config_manager = ConfigManager(config_dir=temp_config_dir)
    config = config_manager.load_config()

    assert config.api.base_url == 'https://custom.api.com'
    assert config.api.timeout == 60
    assert config.cli.char_delay == 0.1
    assert config.model == 'custom-model'
    assert config.api_key == 'file-api-key'

@patch.dict(os.environ, {
    'PERPLEXITY_API_KEY': 'env-api-key',
    'PERPLEXITY_MODEL': 'env-model',
    'CHAR_DELAY': '0.2',
})
def test_load_config_from_env(temp_config_dir: Path):
    """Tests loading the configuration from environment variables."""
    config_manager = ConfigManager(config_dir=temp_config_dir)
    config = config_manager.load_config()

    assert config.api_key == 'env-api-key'
    assert config.model == 'env-model'
    assert config.cli.char_delay == 0.2

@patch.dict(os.environ, {
    'PERPLEXITY_API_KEY': 'env-api-key',
    'PERPLEXITY_MODEL': 'env-model',
})
def test_config_precedence(temp_config_dir: Path):
    """Tests the precedence of configuration sources (env > file > default)."""
    config_data = {
        'model': 'file-model',
        'api_key': 'file-api-key',
    }
    config_path = temp_config_dir / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)

    config_manager = ConfigManager(config_dir=temp_config_dir)
    config = config_manager.load_config()

    assert config.api_key == 'env-api-key'  # Env should override file
    assert config.model == 'env-model'  # Env should override file

def test_save_config(temp_config_dir: Path):
    """Tests saving the configuration to a file."""
    config_manager = ConfigManager(config_dir=temp_config_dir)
    config = config_manager.load_config()
    config.model = 'new-model'
    config.api_key = 'new-api-key'

    config_manager.save_config(config)

    with open(config_manager.config_path, 'r') as f:
        saved_data = yaml.safe_load(f)

    assert saved_data['model'] == 'new-model'
    assert saved_data['api_key'] == 'new-api-key'
