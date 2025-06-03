# MCP Perplexity Server

## Overview

The MCP Perplexity Server is a lightweight Python-based microservice designed to provide simple echo functionality. It receives messages and returns them back to the client, serving as a basic diagnostic and testing tool within the MCP framework.

## Project Details

- **Version**: 0.1.0
- **Python Compatibility**: Python 3.11+

## Features

- **Message Echo**: Returns any message sent to the server
- **Comprehensive Validation**: Robust input validation using Pydantic models
- **Async Server Architecture**: Built with asyncio for efficient performance
- **Flexible Configuration**: Configurable through environment variables and config files

## Dependencies

Core dependencies:
- mcp (>=1.6.0)
- pydantic (>=2.11.2)
- PyYAML (>=6.0.2)

Development dependencies:
- pytest (>=8.3.5)

## Installation

### Prerequisites

- Python 3.11 or higher
- pip
- (Optional) Virtual environment recommended

### Install from PyPI

```bash
pip install chuk-mcp-perplexity
```

### Install from Source

1. Clone the repository:
```bash
git clone <repository-url>
cd chuk-mcp-perplexity
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the package:
```bash
pip install .  # Installs the package in editable mode
```

### Development Installation

To set up for development:
```bash
pip install .[dev]  # Installs package with development dependencies
```

## Running the Server

### Command-Line Interface

```bash
chuk-mcp-perplexity
```

### Programmatic Usage

```python
from chuk_mcp_perplexity.main import main

if __name__ == "__main__":
    main()
```

## Environment Variables

- `NO_BOOTSTRAP`: Set to disable component bootstrapping
- Other configuration options can be set in the configuration files

## Available Tools

### Echo

**Input**:
- `message`: The string message to echo back

**Example**:
```python
echo("Hello, world!")
```

**Returns**:
- The original message in an EchoResult object

## Development

### Code Formatting

- Black is used for code formatting
- isort is used for import sorting
- Line length is set to 88 characters

### Running Tests

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Ensure code passes formatting and testing
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

[MIT License](LICENSE)