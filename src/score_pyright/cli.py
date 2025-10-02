"""Command-line interface for score-pyright."""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import NoReturn


def get_default_config() -> dict:
    """Get the default score-specific configuration for basedpyright."""
    return {
        "typeCheckingMode": "standard",
        "reportMissingImports": True,
        "reportMissingTypeStubs": False,
        "reportUnusedImport": True,
        "reportUnusedClass": True,
        "reportUnusedFunction": True,
        "reportUnusedVariable": True,
        "reportDuplicateImport": True,
        "pythonVersion": "3.9",
        "pythonPlatform": "All",
    }


def merge_configs(base_config: dict, user_config: dict) -> dict:
    """Merge user config with base config, user config takes precedence."""
    merged = base_config.copy()
    merged.update(user_config)
    return merged


def find_config_file() -> Path | None:
    """Find existing pyrightconfig.json or pyproject.toml in current directory or parents."""
    current = Path.cwd()
    
    # Check for pyrightconfig.json
    for parent in [current] + list(current.parents):
        pyright_config = parent / "pyrightconfig.json"
        if pyright_config.exists():
            return pyright_config
        
        pyproject_config = parent / "pyproject.toml"
        if pyproject_config.exists():
            # Check if it has pyright config
            try:
                with open(pyproject_config, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "[tool.pyright]" in content or "[tool.basedpyright]" in content:
                        return pyproject_config
            except Exception:
                pass
    
    return None


def load_user_config(config_path: Path) -> dict:
    """Load user configuration from file."""
    if config_path.name == "pyrightconfig.json":
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    elif config_path.name == "pyproject.toml":
        try:
            # Basic TOML parsing for pyright config
            if sys.version_info >= (3, 11):
                import tomllib
                with open(config_path, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("tool", {}).get("basedpyright", data.get("tool", {}).get("pyright", {}))
            else:
                # Fallback: try importing tomli
                try:
                    import tomli
                    with open(config_path, "rb") as f:
                        data = tomli.load(f)
                        return data.get("tool", {}).get("basedpyright", data.get("tool", {}).get("pyright", {}))
                except ImportError:
                    print("Warning: tomli not available, skipping pyproject.toml config", file=sys.stderr)
                    return {}
        except Exception as e:
            print(f"Warning: Failed to parse config from {config_path}: {e}", file=sys.stderr)
            return {}
    
    return {}


def main() -> int:
    """Main entry point for score-pyright."""
    # Get default config
    default_config = get_default_config()
    
    # Check if user has their own config
    user_config_path = find_config_file()
    
    # If user has config, merge it with defaults (user config takes precedence)
    if user_config_path:
        user_config = load_user_config(user_config_path)
        final_config = merge_configs(default_config, user_config)
    else:
        final_config = default_config
    
    # Create temporary config file with merged configuration
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        prefix="score-pyright-config-",
        delete=False,
        encoding="utf-8"
    ) as temp_config:
        json.dump(final_config, temp_config, indent=2)
        temp_config_path = temp_config.name
    
    try:
        # Import and run basedpyright
        try:
            # Try to import basedpyright's main module
            from basedpyright import main as basedpyright_main
            
            # Set environment variable to use our config
            original_args = sys.argv[1:]
            
            # If no explicit config is specified, use our temporary config
            has_config_arg = any(
                arg.startswith("--project") or arg.startswith("-p")
                for arg in original_args
            )
            
            if not has_config_arg:
                sys.argv = ["basedpyright", "--project", temp_config_path] + original_args
            else:
                sys.argv = ["basedpyright"] + original_args
            
            # Run basedpyright
            return basedpyright_main()
            
        except ImportError:
            print("Error: basedpyright is not installed.", file=sys.stderr)
            print("Please install it with: pip install basedpyright", file=sys.stderr)
            return 1
    finally:
        # Clean up temporary config file
        try:
            os.unlink(temp_config_path)
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
