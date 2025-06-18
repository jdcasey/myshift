# Copyright 2025 John Casey
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration management for the myshift tool.

This module handles:
- Configuration file discovery and loading
- Configuration validation
- Sample configuration generation

The configuration can be stored in multiple locations:
- Linux: $XDG_CONFIG_HOME/myshift.yaml or ~/.config/myshift.yaml
- macOS: ~/Library/Application Support/myshift.yaml
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union

import yaml


class ConfigDict(TypedDict, total=False):
    """Type definition for configuration dictionary."""

    token: str
    schedule_id: str
    my_user: str


def get_config_paths() -> List[Path]:
    """Get the list of possible configuration file paths in order of precedence.

    The paths are checked in the following order:
    1. $XDG_CONFIG_HOME/myshift.yaml (Linux)
    2. ~/.config/myshift.yaml (Linux)
    3. ~/Library/Application Support/myshift.yaml (macOS)

    Returns:
        List of Path objects representing possible config file locations
    """
    paths = []

    # Add XDG config path for Linux
    if "XDG_CONFIG_HOME" in os.environ:
        paths.append(Path(os.environ["XDG_CONFIG_HOME"]) / "myshift.yaml")
    else:
        paths.append(Path.home() / ".config" / "myshift.yaml")

    # Add macOS path
    paths.append(Path.home() / "Library" / "Application Support" / "myshift.yaml")

    return paths


def load_config() -> ConfigDict:
    """Load configuration from the first available config file.

    The configuration file should be a YAML file containing:
    - pagerduty_token: Required API token for PagerDuty
    - my_user: Optional user ID or email for the current user
    - schedule_id: Optional default schedule ID

    Returns:
        Configuration dictionary

    Raises:
        SystemExit: If no config file is found or if there's an error loading the file
    """
    for path in get_config_paths():
        if path.exists():
            try:
                with open(path) as f:
                    config = yaml.safe_load(f)
                    if not isinstance(config, dict):
                        raise ValueError("Configuration must be a dictionary")
                    return config
            except Exception as e:
                print(
                    f"Error loading config from {path}: {e}",
                    file=sys.stderr,
                )
                sys.exit(1)

    print(
        "No configuration file found. Please create one using " "'myshift config --print'",
        file=sys.stderr,
    )
    sys.exit(1)


def print_sample_config() -> None:
    """Print a sample configuration file."""
    print(
        """# MyShift Configuration
# This file should be placed in one of the following locations:
# - Linux: ~/.config/myshift.yaml
# - macOS: ~/Library/Application Support/myshift.yaml

# PagerDuty API token
token: \"your-pagerduty-token\"

# Default schedule ID (optional)
# schedule_id: \"your-default-schedule-id\"

# Your PagerDuty user ID or email (optional)
# This will be used when no --user-id or --user-email is provided
# my_user: \"your-email@example.com\"  # or \"your-user-id\"
"""
    )


def validate_config(config: ConfigDict) -> None:
    """Validate the configuration parameters.

    Checks for:
    - Presence of required pagerduty_token
    - Valid format of my_user (if present)
    - Valid format of schedule_id (if present)

    Args:
        config: Configuration dictionary to validate

    Raises:
        SystemExit: If any validation fails
    """
    if not config.get("token"):
        print("Error: 'token' is required in configuration", file=sys.stderr)
        sys.exit(1)

    # Validate my_user if present
    my_user = config.get("my_user")
    if my_user and not isinstance(my_user, str):
        print(
            "Error: 'my_user' must be a string (email or user ID)",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate schedule_id if present
    schedule_id = config.get("schedule_id")
    if schedule_id and not isinstance(schedule_id, str):
        print("Error: 'schedule_id' must be a string", file=sys.stderr)
        sys.exit(1)


def config_main(args: Optional[List[str]] = None) -> None:
    """Handle the config sub-command.

    Args:
        args: Optional list of command line arguments

    Raises:
        SystemExit: If configuration validation fails
    """
    parser = argparse.ArgumentParser(description="Manage MyShift configuration.")
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print a sample configuration file",
    )
    parsed_args = parser.parse_args(args)

    if parsed_args.print:
        print_sample_config()
        return

    # If no options provided, validate the configuration
    try:
        config = load_config()
        validate_config(config)
        print("Configuration is valid.")
    except Exception as e:
        print(f"Error validating configuration: {e}", file=sys.stderr)
        sys.exit(1)
