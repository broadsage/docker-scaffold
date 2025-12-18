#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Configuration Merger - Merges defaults.yaml + project.yaml with feature activation.

Architecture:
    This module follows a clean, layered architecture:

    1. Dependencies Layer: Imports and dependency checks
    2. Core Logic Layer: Pure functions for merging, validation, feature activation
    3. I/O Layer: File loading/saving operations
    4. CLI Layer: User-facing interface and main entry point

    Each layer has a single responsibility and can be tested independently.
"""

import sys
import copy
from pathlib import Path
from typing import Dict, Any, List

try:
    import yaml
except ImportError:
    print("❌ Error: PyYAML is not installed")
    print("   Install with: pip install pyyaml")
    sys.exit(1)


# CORE LOGIC LAYER - Pure functions for business logic
def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries.

    Args:
        base: Base dictionary (defaults)
        override: Override dictionary (project-specific)

    Returns:
        Merged dictionary where override values win on conflicts
    """
    result = copy.deepcopy(base)

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)  # type: ignore
        else:
            result[key] = copy.deepcopy(value)

    return result


def get_feature_bundles(defaults: Dict[str, Any]) -> List[str]:
    """Dynamically detect feature bundles from defaults.

    Feature bundles are sections in defaults that aren't core sections.
    This makes the script auto-discover new features without code changes.

    Args:
        defaults: The defaults configuration

    Returns:
        List of feature bundle names (e.g., ['github', 'security', 'registry'])
    """
    core_sections = {"organization", "metadata", "build", "image", "documentation"}
    features = [
        key for key in defaults.keys() if key not in core_sections
    ]  # type: ignore
    return sorted(features)


def make_safe_default(value: Any) -> Any:
    """Convert a value to a safe default (false/empty for disabled features).

    Args:
        value: Any value from config

    Returns:
        Safe default: False for booleans, [] for lists, {} for dicts, None otherwise
    """
    if isinstance(value, dict):
        return {k: make_safe_default(v) for k, v in value.items()}  # type: ignore
    if isinstance(value, list):
        return []
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return 0
    if isinstance(value, str):
        return value
    return None


def activate_feature_bundles(
    defaults: Dict[str, Any], project: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge configs and activate feature bundles based on feature flags.

    Logic:
        1. Always include core sections (organization, metadata, etc.)
        2. For enabled features: load bundle from defaults
        3. Apply project-specific overrides
        4. For disabled features: use safe defaults (prevent undefined vars in Ansible)

    Args:
        defaults: Configuration with feature bundles
        project: Project-specific configuration with feature toggles

    Returns:
        Merged configuration with all features (enabled or safe defaults)
    """
    merged: Dict[str, Any] = {}
    core_sections = {
        "organization",
        "metadata",
        "build",
        "image",
        "documentation",
        "template",
    }
    features = project.get("features", {})
    bundles = get_feature_bundles(defaults)

    # Always include core sections from defaults
    for section in core_sections:
        if section in defaults:
            merged[section] = copy.deepcopy(defaults[section])

    # Activate enabled bundles from defaults
    for bundle in bundles:
        enabled = features.get(bundle, False)
        if enabled and bundle in defaults:
            merged[bundle] = copy.deepcopy(defaults[bundle])  # type: ignore
        else:
            # Create safe defaults for disabled features
            if bundle in defaults:
                merged[bundle] = make_safe_default(defaults[bundle])

    # Apply project-specific overrides (merge all sections from project)
    merged = deep_merge(merged, project)

    return merged


def validate_config(config: Dict[str, Any]) -> List[str]:
    """Validate configuration for required fields and correct types.

    Args:
        config: Configuration to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors: List[str] = []

    # Validate image name if image section exists
    if "image" in config:
        image_name = config["image"].get("name")
        if not image_name or not isinstance(image_name, str):
            errors.append("image.name must be a non-empty string")

    # Validate metadata.license (MANDATORY)
    if "metadata" in config:
        license_value = config["metadata"].get("license")
        if not license_value or not isinstance(license_value, str):
            errors.append("metadata.license must be a non-empty string")
    else:
        errors.append("metadata section is required with license field")

    # Validate build.platforms if present
    if "build" in config and "platforms" in config["build"]:
        platforms = config["build"]["platforms"]
        if not isinstance(platforms, list) or not platforms:
            errors.append("build.platforms must be a non-empty list")

    return errors


# I/O LAYER - File loading and saving
def _handle_io_error(operation: str, file_path: Path, error: Exception) -> None:
    """Handle I/O errors consistently (DRY)."""
    icon = "❌"
    print(f"{icon} Error {operation} {file_path}: {error}")
    sys.exit(1)


def load_yaml(file_path: Path) -> Dict[str, Any]:
    """Load and parse a YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Parsed YAML as dictionary, empty dict if file doesn't exist

    Raises:
        SystemExit: If file parsing fails
    """
    if not file_path.exists():
        return {}

    try:
        with open(file_path, encoding="utf-8") as f:
            content = yaml.safe_load(f)
            data: Dict[str, Any] = content if content else {}
        return data
    except yaml.YAMLError as e:
        _handle_io_error("parsing", file_path, e)
        return {}  # Never reached, but satisfies type checker


def save_yaml(file_path: Path, data: Dict[str, Any]) -> None:
    """Save data to a YAML file.

    Args:
        file_path: Path where to save YAML file
        data: Dictionary to save

    Raises:
        SystemExit: If file write fails
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)
    except Exception as e:
        _handle_io_error("writing", file_path, e)


# CLI LAYER - User interface and main entry point
def print_header(title: str) -> None:
    """Print a formatted header."""
    line = "=" * 70
    print(f"{line}\n{title}\n{line}")


def print_status(message: str, success: bool = True) -> None:
    """Print a status message with icon."""
    prefix = "✓" if success else "❌"
    print(f"{prefix} {message}")


def print_features(config: Dict[str, Any]) -> None:
    """Print activated features in a readable format."""
    features = config.get("features", {})
    if not features:
        return

    print("\nActivated features:")
    for name, enabled in features.items():
        status = "✓" if enabled else "○"
        print(f"  {status} {name}: {enabled}")


def print_validation_errors(errors: List[str]) -> None:
    """Print validation errors in a consistent format (DRY)."""
    for error in errors:
        print(f"  • {error}")


def main() -> None:
    """Main entry point - orchestrates the merge process."""
    # Configuration file paths
    defaults_file = Path("vars/defaults.yaml")
    project_file = Path("/tmp/project.yaml")
    output_file = Path("/tmp/merged_config.yaml")

    # Header
    print_header("Docker Scaffold Configuration Merger")

    # Validate input
    if not project_file.exists():
        print_status(f"Project file not found: {project_file}", success=False)
        print("   Please mount your project.yaml to /tmp/project.yaml")
        sys.exit(1)

    # Load configurations
    print("\nLoading configurations...")
    defaults = load_yaml(defaults_file)
    if defaults_file.exists():
        print_status(f"Loaded defaults from {defaults_file}")
    else:
        print_status("Defaults file not found, using project config only", success=True)

    project = load_yaml(project_file)
    print_status(f"Loaded project from {project_file}")

    # Merge with feature activation
    print("\nMerging configurations with feature bundles...")
    merged = activate_feature_bundles(defaults, project)
    print_status("Configuration merged")

    # Show activated features
    print_features(merged)

    # Validate
    print("\nValidating configuration...")
    errors = validate_config(merged)

    if errors:
        print_status("Validation failed", success=False)
        print_validation_errors(errors)
        sys.exit(1)

    image_name = merged.get("image", {}).get("name", "unknown")
    print_status(f"Validation passed for image: {image_name}")

    # Save
    print("\nGenerating output...")
    save_yaml(output_file, merged)
    print_status(f"Configuration saved to {output_file}")

    # Summary
    print_header(f"🎉 Configuration ready for: {image_name}")
    print(f"\nNext: Ansible will use {output_file} to generate scaffold")
    print(f"Note: {output_file} will be automatically cleaned up after generation")


if __name__ == "__main__":
    sys.exit(main())
