# Perplexity AI CLI

A command-line interface for interacting with the Perplexity AI API.

## Features

*   Interactive chat session.
*   Powered by Perplexity AI.
*   Configurable via a YAML file and environment variables.
*   Modern CLI built with `click`.
*   High test coverage with `pytest`.

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/addhe/perplexity-chatgpt-cli.git
    cd perplexity-chatgpt-cli
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Install the application in editable mode:
    ```bash
    pip install -e .
    ```

## Usage

To start the interactive chat session, run the following command:

```bash
perplexity-cli
```

### Options

*   `--api-key`: Your Perplexity AI API key.
*   `--model`: The model to use for completions (e.g., `sonar-pro`).

## Configuration

The application can be configured via a YAML file and environment variables.

### Configuration File

A configuration file named `config.yaml` can be created in the `~/.perplexity-cli/` directory.

Here is an example of the configuration file:

```yaml
api:
  base_url: https://api.perplexity.ai
  timeout: 30
cli:
  char_delay: 0.0
model: sonar-pro
```

### Environment Variables

You can also configure the application using environment variables:

*   `PERPLEXITY_API_KEY`: Your Perplexity AI API key.
*   `PERPLEXITY_MODEL`: The model to use for completions.
*   `CHAR_DELAY`: The character delay for the typewriter effect.

## Development

### Setting up the Development Environment

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Tests

To run the tests, use the following command:

```bash
pytest
```

To get a coverage report, use the following command:

```bash
pytest --cov=perplexity_cli
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
