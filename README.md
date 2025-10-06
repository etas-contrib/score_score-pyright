# score-pyright

A wrapper around [basedpyright](https://github.com/DetachHead/basedpyright) with score-specific default configuration.

## Overview

`score-pyright` is a Python package that wraps basedpyright with sensible defaults for the score project. It can be installed via pip/uv or run directly with pipx/uvx.

## Installation

Use pip, pipx or uv:

```bash
pip install score-pyright
pipx install score-pyright
uv pip install score-pyright
```

### Using uvx (run without installation)

```bash
uvx score-pyright
```

### From source

You can also run directly from the source without installation:

```bash
# Clone the repository
git clone https://github.com/etas-contrib/score_score-pyright.git
cd score_score-pyright

# Run using Python module syntax
PYTHONPATH=src python -m score_pyright <files>
```

## Usage

Once installed, you can run `score-pyright` just like you would run `basedpyright`:

```bash
# Check the current directory
score-pyright

# Check a specific file
score-pyright myfile.py

# Check with additional options
score-pyright --watch

# Display help
score-pyright --help

# Display version
score-pyright --version
```

## Default Configuration

`score-pyright` comes with the following default configuration:

- `typeCheckingMode`: `"standard"`
- `reportMissingImports`: `true`
- `reportMissingTypeStubs`: `false`
- `reportUnusedImport`: `true`
- `reportUnusedClass`: `true`
- `reportUnusedFunction`: `true`
- `reportUnusedVariable`: `true`
- `reportDuplicateImport`: `true`
- `pythonVersion`: `"3.9"`
- `pythonPlatform`: `"All"`

## Custom Configuration

You can override the default configuration by creating a `pyrightconfig.json` or adding a `[tool.basedpyright]` section to your `pyproject.toml`. Your configuration will be merged with the defaults, with your settings taking precedence.

### Example: pyrightconfig.json

```json
{
  "typeCheckingMode": "strict",
  "pythonVersion": "3.11"
}
```

### Example: pyproject.toml

```toml
[tool.basedpyright]
typeCheckingMode = "strict"
pythonVersion = "3.11"
```

## How It Works

When you run `score-pyright`, it:

1. Loads the default score-specific configuration
2. Searches for your project's configuration (`pyrightconfig.json` or `pyproject.toml`)
3. Merges your configuration with the defaults (your settings take precedence)
4. Passes the merged configuration to basedpyright
5. Runs basedpyright with all the original command-line arguments you provided

## Development

To install for development:

```bash
git clone https://github.com/etas-contrib/score_score-pyright.git
cd score_score-pyright
pip install -e .
```

## Requirements

- Python 3.9 or higher
- basedpyright 1.0.0 or higher

## License

MIT
