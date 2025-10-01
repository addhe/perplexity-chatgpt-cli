"""Tests for the Perplexity API client."""

from unittest.mock import patch, MagicMock

import pytest
import requests
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

@patch('requests.post')
def test_generate_response_success(mock_post, config: Config):
    """Tests successful response generation."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'choices': [{'message': {'content': 'Hello, world!'}}]}
    mock_post.return_value = mock_response

    client = PerplexityClient(config)
    response = client.generate_response("Hello")

    assert response is not None
    assert response['choices'][0]['message']['content'] == 'Hello, world!'

@patch('requests.post')
def test_generate_response_api_error(mock_post, config: Config):
    """Tests handling of API errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
    mock_post.return_value = mock_response

    client = PerplexityClient(config)
    response = client.generate_response("Hello")

    assert response is None

@patch('requests.post', side_effect=requests.exceptions.RequestException("Test error"))
def test_generate_response_network_error(mock_post, config: Config):
    """Tests handling of network errors."""
    client = PerplexityClient(config)
    response = client.generate_response("Hello")

    assert response is None

def test_print_response(config: Config, runner: CliRunner):
    """Tests the print_response method."""
    response_data = {'choices': [{'message': {'content': 'Hello'}}]}
    client = PerplexityClient(config)

    with runner.isolation() as (stdout, _):
        client.print_response(response_data)
        output = stdout.getvalue().decode('utf-8')
        assert "Hello" in output

def test_print_response_none(config: Config, runner: CliRunner):
    """Tests the print_response method with None response."""
    client = PerplexityClient(config)
    with runner.isolation() as (stdout, _):
        client.print_response(None)
        output = stdout.getvalue().decode('utf-8')
        assert "Failed to generate a response." in output