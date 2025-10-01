"""Configuration management for Perplexity CLI."""

import os
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class APIConfig:
    """API configuration settings."""
    base_url: str = "https://api.perplexity.ai"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

@dataclass
class CLIConfig:
    """CLI behavior configuration."""
    char_delay: float = 0.0
    max_history: int = 100
    theme: str = "default"

@dataclass
class Config:
    """Main configuration container."""
    api: APIConfig = field(default_factory=APIConfig)
    cli: CLIConfig = field(default_factory=CLIConfig)
    api_key: Optional[str] = None
    model: str = "llama-3.1-sonar-small-128k-online"

    def __post_init__(self):
        """Load configuration from environment variables."""
        self._load_from_environment()

    def _load_from_environment(self):
        """Load configuration from environment variables."""
        if env_api_key := os.getenv('PERPLEXITY_API_KEY'):
            self.api_key = env_api_key

        if env_model := os.getenv('PERPLEXITY_MODEL'):
            self.model = env_model

        if env_char_delay := os.getenv('CHAR_DELAY'):
            try:
                self.cli.char_delay = float(env_char_delay)
            except ValueError:
                pass

class ConfigManager:
    """Manages configuration loading and saving."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize config manager."""
        self.config_dir = config_dir or self._get_default_config_dir()
        self.config_path = self.config_dir / "config.yaml"

    def _get_default_config_dir(self) -> Path:
        """Get default configuration directory."""
        return Path.home() / ".perplexity-cli"

    def load_config(self) -> Config:
        """Load configuration."""
        config = Config()
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            if 'api' in data:
                config.api = APIConfig(**data['api'])
            if 'cli' in data:
                config.cli = CLIConfig(**data['cli'])
            if 'api_key' in data:
                config.api_key = data['api_key']
            if 'model' in data:
                config.model = data['model']
        
        config._load_from_environment()
        return config

    def save_config(self, config: Config) -> None:
        """Save configuration."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        data = {
            'api': {
                'base_url': config.api.base_url,
                'timeout': config.api.timeout,
                'max_retries': config.api.max_retries,
                'retry_delay': config.api.retry_delay,
            },
            'cli': {
                'char_delay': config.cli.char_delay,
                'max_history': config.cli.max_history,
                'theme': config.cli.theme,
            },
            'model': config.model,
        }
        if config.api_key and not os.getenv("PERPLEXITY_API_KEY"):
            data['api_key'] = config.api_key

        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False, indent=2)
