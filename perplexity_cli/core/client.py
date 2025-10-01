"""Perplexity API client implementation."""

import requests
import time
from typing import Optional, Any

import click

from perplexity_cli.core.config import Config

class PerplexityClient:
    """Client for interacting with the Perplexity AI API."""

    def __init__(self, config: Config) -> None:
        """Initialize client with configuration."""
        self.config = config

    def generate_response(self, prompt: str) -> Optional[Any]:
        """Generates a response using the Perplexity API."""
        messages = [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ]

        payload = {
            "model": self.config.model,
            "messages": messages,
        }

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                f"{self.config.api.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.config.api.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            click.echo(f"Error communicating with Perplexity API: {e}", err=True)
            return None
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}", err=True)
            return None

    def print_response(self, response: Optional[Any]) -> None:
        """Prints the AI's response with a typewriter effect."""
        if response is None:
            click.echo("Failed to generate a response.", err=True)
            return

        message: str = response.get('choices', [{}])[0].get(
            'message', {}).get('content', '')

        for char in message:
            click.echo(char, nl=False)
            time.sleep(self.config.cli.char_delay)
        click.echo()
