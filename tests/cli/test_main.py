"""Tests for the main CLI."""

from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from perplexity_cli.cli.main import cli

@pytest.fixture
def runner() -> CliRunner:
    """Returns a click CliRunner."""
    return CliRunner()

@patch('perplexity_cli.cli.main.PerplexityClient')
@patch('perplexity_cli.cli.main.ConfigManager')
def test_chat_command(mock_config_manager, mock_client, runner: CliRunner):
    """Tests the chat command with a mocked API client."""
    mock_config = MagicMock()
    mock_config.api_key = "test-key"
    mock_config_manager.return_value.load_config.return_value = mock_config

    mock_client_instance = MagicMock()
    mock_client_instance.generate_response.return_value = {'choices': [{'message': {'content': 'Hello'}}]}
    mock_client.return_value = mock_client_instance

    result = runner.invoke(cli, ['chat'], input='Hello\nexit()\n')

    assert result.exit_code == 0
    assert "Hello" in result.output

@patch('perplexity_cli.cli.main.ConfigManager')
def test_chat_command_no_api_key(mock_config_manager, runner: CliRunner):
    """Tests the chat command with no API key configured."""
    mock_config = MagicMock()
    mock_config.api_key = None
    mock_config_manager.return_value.load_config.return_value = mock_config

    result = runner.invoke(cli, ['chat'])

    assert result.exit_code == 1
    assert "API key not configured" in result.output

@patch('perplexity_cli.cli.main.ConfigManager')
def test_chat_command_exit(mock_config_manager, runner: CliRunner):
    """Tests exiting the chat command."""
    mock_config = MagicMock()
    mock_config.api_key = "test-key"
    mock_config_manager.return_value.load_config.return_value = mock_config

    result = runner.invoke(cli, ['chat'], input='exit()\n')

    assert result.exit_code == 0

@patch('perplexity_cli.cli.main.ConfigManager')
def test_cli_options(mock_config_manager, runner: CliRunner):
    """Tests passing options to the CLI."""
    mock_config = MagicMock()
    mock_config.api_key = "test-key"
    mock_config_manager.return_value.load_config.return_value = mock_config

    runner.invoke(cli, ['--api-key', 'new-key', '--model', 'new-model', 'chat'], input='exit()\n')

    assert mock_config.api_key == 'new-key'
    assert mock_config.model == 'new-model'
