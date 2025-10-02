"""Tests for the Perplexity API client."""

from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from perplexity_cli.core.client import PerplexityClient
from perplexity_cli.core.config import Config

@pytest.fixture
def config() -> Config:
    """Returns a mock Config object."""
    return Config(api_key="test-key")

@pytest.fixture
def runner() -> CliRunner:
    """Returns a click CliRunner."""
    return CliRunner()

@patch('perplexity_cli.core.client.Perplexity')
def test_generate_response_success(mock_perplexity, config: Config):
    """Tests successful response generation."""
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = 'Hello, world!'
    mock_perplexity.return_value.chat.completions.create.return_value = mock_completion

    client = PerplexityClient(config)
    response = client.generate_response("Hello")

    assert response is not None
    assert response.choices[0].message.content == 'Hello, world!'

@patch('perplexity_cli.core.client.Perplexity')
def test_generate_response_api_error(mock_perplexity, config: Config):
    """Tests handling of API errors."""
    mock_perplexity.return_value.chat.completions.create.side_effect = Exception("API Error")

    client = PerplexityClient(config)
    response = client.generate_response("Hello")

    assert response is None

def test_print_response(config: Config, runner: CliRunner):
    """Tests the print_response method."""
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = 'Hello'
    client = PerplexityClient(config)

    with runner.isolation() as (stdout, _):
        client.print_response(mock_completion)
        output = stdout.getvalue().decode('utf-8')
        assert "Hello" in output

def test_print_response_none(config: Config, runner: CliRunner):
    """Tests the print_response method with None response."""
    client = PerplexityClient(config)
    with runner.isolation() as (stdout, _):
        client.print_response(None)
        output = stdout.getvalue().decode('utf-8')
        assert "Failed to generate a response." in output
