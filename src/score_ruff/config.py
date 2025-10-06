"""Command-line interface for score-pyright."""

import json
import logging
import tempfile
import tomllib
from pathlib import Path
from typing import Any, NoReturn, cast

logger = logging.getLogger(__name__)

def get_default_config() -> dict[str, str]:
    """Get the default score-specific configuration for basedpyright."""
    default_config_path = Path(__file__).parent / "pyproject.toml"
    return load_user_config(default_config_path)


def merge_configs(base_config: dict[str, str], user_config: dict[str, str]) -> dict[str, str]:
    """
    Merge user config with base config, user config takes precedence.
    """
    merged = base_config.copy()
    for key, value in user_config.items():
        if key in merged:
            logger.debug(f"Merging config key {key}: replacing {merged[key]} with {value}")
        merged[key] = value
    return merged


def find_config_file() -> Path | None:
    """
    Find existing pyrightconfig.json or pyproject.toml in current directory or parents.
    Stops at first potential match.
    """
    current = Path.cwd()
    
    # Check for pyrightconfig.json
    for parent in [current] + list(current.parents):
        pyright_config = parent / "pyrightconfig.json"
        if pyright_config.exists():
            return pyright_config
        
        pyproject_config = parent / "pyproject.toml"
        if pyproject_config.exists():
            try:
                content = pyproject_config.read_text(encoding="utf-8")
                if "[tool.pyright]" in content or "[tool.basedpyright]" in content:
                    return pyproject_config
            except Exception:
                logger.warning(f"Failed to read {pyproject_config}, skipping")
    
    return None


def load_user_config(config_path: Path) -> dict[str, str]:
    """Load user configuration from file."""
    content = config_path.read_text(encoding="utf-8")

    if config_path.name == "pyrightconfig.json":
        json_data = cast(dict[str, str], json.loads(content))
        return json_data
    elif config_path.name == "pyproject.toml":
        toml_data: dict[str, object] = tomllib.loads(content)
        if "tool" not in toml_data:
            raise RuntimeError("Default config is missing [tool] section")
        if len(toml_data) != 1:
            raise RuntimeError("Default config has unexpected sections outside [tool]")
        tool_config = toml_data["tool"]
        assert isinstance(tool_config, dict)
        if "basedpyright" not in tool_config:
            raise RuntimeError("Default config is missing [tool.basedpyright] section")

        return cast(dict[str, str], tool_config["basedpyright"])
    else:
        raise RuntimeError(f"Unsupported config file: {config_path}")

def get_final_config(user_config_path: Path | None) -> dict[str, str]:
    """Get the final configuration by merging defaults with user config if present."""
    default_config = get_default_config()
    if not user_config_path:
        user_config_path= find_config_file()
    
    if user_config_path:
        user_config = load_user_config(user_config_path)
        final_config = merge_configs(default_config, user_config)
    else:
        final_config = default_config
    
    return final_config

# TODO: when there is no user config, there is no need to write to some temp path!
# just pass the config directly from the bundled config.
def write_config_to_tempfile(user_config: Path | None) -> Path:
    """Write the final configuration to a temporary JSON file and return its path."""
    config = get_final_config(user_config)
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        prefix="score-pyright-config-",
        delete=False,
        encoding="utf-8"
    ) as temp_config:
        # json.dump(config, temp_config, indent=2)
        return Path(temp_config.name)
