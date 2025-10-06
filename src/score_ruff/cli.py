"""Command-line interface for score-ruff."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import NoReturn

from score_ruff import __version__, config


def run_ruff(argv: list[str]) -> NoReturn:
    sys.argv = ["ruff"] + argv
    # replace current process with ruff
    os.execvp("ruff", sys.argv)  # type: ignore[attr-defined]


def main():
    """Main entry point for score-ruff."""
    argv = sys.argv[1:]
    p = argparse.ArgumentParser(
        description="score-ruff: A wrapper around ruff with score-specific defaults",
        epilog="All other arguments are passed to ruff",
        add_help=False,
    )
    _ = p.add_argument(
        "-h", "--help", action="store_true", help="Show this help message and exit"
    )
    _ = p.add_argument(
        "-v", "--version", action="store_true", help="Show version information and exit"
    )
    _ = p.add_argument(
        "--config",
        type=str,
        help="Path to pyproject.toml or ruff.toml",
    )
    _ = p.add_argument(
        "--score-config",
        action="store_true",
        help="Print the score default configuration and exit",
    )
    _ = p.add_argument(
        "--print-config",
        action="store_true",
        help="Print the resolved configuration and exit",
    )

    parsed, rest = p.parse_known_args(argv)

    if parsed.help:  # pyright: ignore[reportAny]
        print(p.format_help())
        print("--- ruff help ---\n")
        run_ruff(argv)
    
    if parsed.version:  # pyright: ignore[reportAny]
        print(f"score-ruff version {__version__}")
        run_ruff(["--version"])

    usr_cfg = Path(parsed.config) if parsed.config else None  # pyright: ignore[reportAny]

    if parsed.score_config:  # pyright: ignore[reportAny]
        print("score-ruff default configuration:")
        cfg = config.get_default_config()
        print(json.dumps(cfg, indent=2))
        return 0
    elif parsed.print_config:  # pyright: ignore[reportAny]
        print(f"score-ruff resolved configuration (using {usr_cfg}):")
        cfg = config.get_final_config(user_config_path=usr_cfg)
        print(json.dumps(cfg, indent=2))
        return 0

    cfg_file = config.write_config_to_tempfile(user_config=usr_cfg)

    return run_ruff(["--config", str(cfg_file)] + rest)


if __name__ == "__main__":
    sys.exit(main())
