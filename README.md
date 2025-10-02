# score-pyright

A wrapper around [basedpyright](https://github.com/DetachHead/basedpyright) with score-specific default configuration.

## Overview

`score-pyright` is a Python package that wraps basedpyright with sensible defaults for the score project. It can be installed via pip/uv or run directly with pipx/uvx.

## Installation

### Using pip

```bash
pip install score-pyright
```

### Using uv

```bash
uv pip install score-pyright
```

### Using pipx (for isolated execution)

```bash
pipx install score-pyright
```

### Using uvx (run without installation)

```bash
uvx score-pyright
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

## Development

To install for development:

```bash
pip install -e .
```

## License

MIT
