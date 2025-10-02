# score-pyright Features

## Core Features

### ✅ Modern Python Package Structure
- Uses the recommended `src` layout
- Built with `hatchling` for modern Python packaging
- Follows PEP 517/518 standards

### ✅ Multiple Installation Methods
- `pip install score-pyright` - Standard pip installation
- `uv pip install score-pyright` - Fast installation with uv
- `pipx install score-pyright` - Isolated installation
- `uvx score-pyright` - Run without installation
- `pip install -e .` - Development installation
- `PYTHONPATH=src python -m score_pyright` - Run from source

### ✅ Smart Configuration Management
- Provides sensible defaults for score projects
- Automatically discovers user configuration files
- Merges user config with defaults (user settings take precedence)
- Supports both `pyrightconfig.json` and `pyproject.toml`
- Works with `[tool.basedpyright]` and `[tool.pyright]` sections

### ✅ Seamless basedpyright Integration
- Wraps basedpyright as a dependency (no manual copying needed)
- Passes through all basedpyright command-line options
- Supports all basedpyright features (watch mode, JSON output, etc.)
- Returns the same exit codes as basedpyright

### ✅ Python 3.9+ Support
- Compatible with Python 3.9, 3.10, 3.11, and 3.12
- Uses `tomllib` (Python 3.11+) or `tomli` (Python <3.11) for TOML parsing
- Proper type hints throughout the codebase

## Default Configuration

The following checks are enabled by default:

| Setting | Value | Description |
|---------|-------|-------------|
| `typeCheckingMode` | `"standard"` | Standard type checking mode |
| `reportMissingImports` | `true` | Report when imports cannot be resolved |
| `reportMissingTypeStubs` | `false` | Don't require type stubs for all packages |
| `reportUnusedImport` | `true` | Report unused imports |
| `reportUnusedClass` | `true` | Report unused classes |
| `reportUnusedFunction` | `true` | Report unused functions |
| `reportUnusedVariable` | `true` | Report unused variables |
| `reportDuplicateImport` | `true` | Report duplicate imports |
| `pythonVersion` | `"3.9"` | Target Python 3.9+ |
| `pythonPlatform` | `"All"` | Cross-platform analysis |

## Command-Line Interface

All basedpyright options are supported:

```bash
score-pyright [options] files...
```

### Common Options
- `-h, --help` - Show help message
- `--version` - Show version information
- `-w, --watch` - Watch mode (continuous type checking)
- `-p, --project <FILE>` - Use specific configuration file
- `--outputjson` - Output results in JSON format
- `--verbose` - Emit verbose diagnostics
- And many more!

## Usage Examples

### Basic Type Checking
```bash
# Check a single file
score-pyright myfile.py

# Check multiple files
score-pyright file1.py file2.py

# Check entire directory
score-pyright .
```

### Watch Mode
```bash
# Continuous type checking
score-pyright --watch
```

### JSON Output
```bash
# Get results in JSON format
score-pyright --outputjson myfile.py
```

### With Custom Configuration
```bash
# Use specific config file
score-pyright --project myconfig.json

# Or let it auto-discover your pyrightconfig.json or pyproject.toml
score-pyright
```

## Configuration Examples

### Override Type Checking Mode
```json
// pyrightconfig.json
{
  "typeCheckingMode": "strict"
}
```

### Set Python Version
```toml
# pyproject.toml
[tool.basedpyright]
pythonVersion = "3.11"
typeCheckingMode = "basic"
```

### Disable Specific Checks
```json
// pyrightconfig.json
{
  "reportUnusedVariable": false,
  "reportMissingTypeStubs": true
}
```

## File Structure

```
score-pyright/
├── src/score_pyright/
│   ├── __init__.py          # Package version and metadata
│   ├── __main__.py          # Module entry point
│   └── cli.py               # Main CLI logic
├── pyproject.toml           # Package configuration
├── README.md                # User documentation
├── IMPLEMENTATION.md        # Implementation details
├── FEATURES.md              # This file
├── LICENSE                  # MIT License
└── example.py               # Example Python file
```

## Dependencies

- **basedpyright** (>=1.0.0): The underlying type checker
- **tomli** (>=2.0.0, Python <3.11): TOML parser for older Python versions
- **nodejs-wheel-binaries**: Automatically installed by basedpyright

## License

MIT License - See [LICENSE](LICENSE) file for details.
