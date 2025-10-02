"""Perplexity API client implementation."""

from perplexity import Perplexity
import time
from typing import Optional, Any

import click

from perplexity_cli.core.config import Config

class PerplexityClient:
    """Client for interacting with the Perplexity AI API."""

    def __init__(self, config: Config) -> None:
        """Initialize client with configuration."""
        self.config = config
        self.client = Perplexity(api_key=self.config.api_key)

    def generate_response(self, prompt: str) -> Optional[Any]:
        """Generates a response using the Perplexity API."""
        messages = [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ]

        try:
            completion = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
            )
            return completion
        except Exception as e:
            click.echo(f"Error communicating with Perplexity API: {e}", err=True)
            return None

    def print_response(self, response: Optional[Any]) -> None:
        """Prints the AI's response with a typewriter effect."""
        if response is None:
            click.echo("Failed to generate a response.", err=True)
            return

        message: str = response.choices[0].message.content

        for char in message:
            click.echo(char, nl=False)
            time.sleep(self.config.cli.char_delay)
        click.echo()

