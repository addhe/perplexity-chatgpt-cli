
"""Main CLI entry point for Perplexity CLI."""

import click
import sys
from typing import Optional

from perplexity_cli.core.config import ConfigManager, Config
from perplexity_cli.core.client import PerplexityClient

def get_welcoming_text(config: Config) -> str:
    """Returns the welcoming text."""
    return (
        f"\nWelcome to {config.model} Text Generator made by (Awan)\n"
        f"Happy chat and talk with your {config.model} AI Generative Model\n"
        "Addhe Warman Putra - (Awan)\n"
        "Type 'exit()' to exit from program\n"
    )

@click.group(invoke_without_command=True)
@click.option('--api-key', help='Perplexity API key')
@click.option('--model', help='Model to use for completions')
@click.pass_context
def cli(ctx: click.Context, api_key: Optional[str], model: Optional[str]) -> None:
    """Perplexity CLI - AI-powered command-line interface."""
    ctx.ensure_object(dict)

    config_manager = ConfigManager()
    config = config_manager.load_config()

    if api_key:
        config.api_key = api_key
    if model:
        config.model = model

    ctx.obj['config'] = config

    if ctx.invoked_subcommand is None:
        ctx.invoke(chat)

@cli.command()
@click.pass_context
def chat(ctx: click.Context) -> None:
    """Starts an interactive chat session."""
    config: Config = ctx.obj['config']

    if not config.api_key:
        click.echo("API key not configured. Please set the PERPLEXITY_API_KEY environment variable or use the --api-key option.", err=True)
        sys.exit(1)

    client = PerplexityClient(config)
    click.echo(get_welcoming_text(config))

    try:
        while True:
            user_input: str = click.prompt(">")
            if user_input.lower() == "exit()":
                break

            response = client.generate_response(user_input)
            if response:
                client.print_response(response)
            else:
                click.echo("Failed to generate a response. Please try again.", err=True)

    except (KeyboardInterrupt, EOFError):
        click.echo("\nProgram interrupted by user. Exiting...")

if __name__ == '__main__':
    cli()
