#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Configuration merger for docker-scaffold.

Merges defaults.yml + project.yml with feature bundle activation.
Outputs a single merged_config.yml for Ansible consumption.

Architecture:
  defaults.yml (feature bundles) + project.yml (toggles + overrides)
    → Python merger (this script)
    → merged_config.yml (flat config for Ansible)

Logic:
  1. features.github: true → Load all github.* from defaults.yml
  2. github.* in project.yml → Override specific settings
  3. features.github: false → Exclude all github.*

Example:
  defaults.yml:
    github:
      workflows: true
      issues: true

  project.yml:
    features:
      github: true
    github:
      issues: false

  Result:
    github:
      workflows: true  (from defaults)
      issues: false    (overridden)
"""

import sys
import copy
from pathlib import Path
from typing import Dict, Any, List, Set  # noqa: F401

try:
    import yaml
except ImportError:
    print("❌ Error: PyYAML is not installed")
    print("   Install with: pip install pyyaml")
    sys.exit(1)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries, override values win on conflicts.
    Uses deep copy to avoid reference issues.

    Args:
        base: Base dictionary (defaults)
        override: Override dictionary (project-specific)

    Returns:
        Merged dictionary with overrides applied
    """
    # Deep copy to avoid modifying original
    result = copy.deepcopy(base)

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dicts
            result[key] = deep_merge(result[key], value)  # type: ignore
        else:
            # Override wins - use deep copy to avoid reference issues
            result[key] = copy.deepcopy(value)

    return result


def _extract_safe_defaults(defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dynamically extract safe defaults from defaults.yml.

    For each feature bundle (github, security, registry, etc.),
    creates a safe default version where all boolean/list/dict values
    become false/[]/empty equivalents. This approach makes the script
    automatically adapt to new features without code changes.

    Args:
        defaults: The defaults.yml configuration

    Returns:
        Dictionary of safe default values for disabled features
    """
    safe_defaults: Dict[str, Any] = {}
    feature_bundles = _get_feature_bundles(defaults)

    for bundle_name in feature_bundles:
        if bundle_name in defaults:
            safe_defaults[bundle_name] = _make_safe_default(
                defaults[bundle_name],  # type: ignore[index]
                bundle_name
            )

    return safe_defaults


def _make_safe_default(value: Any, bundle_name: str) -> Any:
    """
    Recursively convert a value to its safe default (all false/empty).

    Preserves structure but makes all leaf values safe (false for bool,
    empty for collections, etc.).

    Args:
        value: The value to convert
        bundle_name: Bundle name (for special handling if needed)

    Returns:
        Safe default version of the value
    """
    if isinstance(value, dict):
        result: Dict[str, Any] = {}
        for key, val in value.items():  # type: ignore[union-attr]
            result[key] = _make_safe_default(val, bundle_name)
        return result
    elif isinstance(value, list):
        return []  # Empty list for safe default
    elif isinstance(value, bool):
        return False  # False for all booleans
    elif isinstance(value, (int, float)):
        return 0  # Zero for numbers
    elif isinstance(value, str):
        # Keep strings as-is (like 'CRITICAL', 'spdx', etc.)
        # but could be set to '' if needed
        return value
    else:
        return None


def _get_feature_bundles(defaults: Dict[str, Any]) -> List[str]:
    """
    Dynamically detect feature bundles from defaults.yml.

    Features are detected as sections that exist in defaults.yml but NOT
    in the hardcoded list of core sections. This makes the script
    automatically discover new features.

    Args:
        defaults: The defaults.yml configuration

    Returns:
        List of feature bundle names
    """
    core_sections = {'organization', 'metadata', 'build', 'image', 'documentation'}
    detected_features = [
        key for key in defaults.keys()  # type: ignore[union-attr]
        if key not in core_sections
    ]
    return sorted(detected_features)


def activate_feature_bundles(defaults: Dict[str, Any], project: Dict[str, Any]) -> Dict[str, Any]:
    """
    Activate feature bundles based on features.* flags (dynamically detected).

    This function automatically discovers all features from defaults.yml,
    so adding a new feature requires ONLY updating defaults.yml - no Python
    code changes needed.

    How it works:
      1. Detects all feature bundles from defaults.yml (anything not a core section)
      2. Loads enabled feature bundles from defaults
      3. Applies project.yml overrides
      4. Ensures disabled features have safe defaults (prevent undefined vars in Ansible)

    Core sections (always included): organization, metadata, build, image, documentation
    Feature bundles (conditional): github, security, registry, and any future additions

    Args:
        defaults: Default configuration with feature bundles (from defaults.yml)
        project: Project-specific configuration (from project.yml)

    Returns:
        Merged configuration with all features (enabled or disabled)
    """
    merged: Dict[str, Any] = {}
    features: Dict[str, Any] = project.get('features', {})
    feature_bundles = _get_feature_bundles(defaults)
    safe_defaults = _extract_safe_defaults(defaults)
    activated_bundles: Set[str] = set()

    # Activate feature bundles (only if enabled)
    for bundle_name in feature_bundles:
        feature_enabled = features.get(bundle_name, False)

        if feature_enabled:
            # Load bundle from defaults using deep copy
            if bundle_name in defaults:
                merged[bundle_name] = copy.deepcopy(defaults[bundle_name])  # type: ignore[index]
                activated_bundles.add(bundle_name)

    # Apply project-specific overrides (separate loop to avoid duplicate merges)
    for bundle_name in feature_bundles:
        feature_enabled = features.get(bundle_name, False)

        if feature_enabled and bundle_name in project and bundle_name in merged:
            # Override with project-specific settings
            merged[bundle_name] = deep_merge(  # type: ignore[arg-type]
                merged[bundle_name],  # type: ignore[index]
                project[bundle_name]  # type: ignore[index]
            )

    # Ensure all feature bundles exist (use safe defaults if not activated)
    for bundle_name, default_value in safe_defaults.items():
        if bundle_name not in merged:
            merged[bundle_name] = copy.deepcopy(default_value)

    # Always include core sections (not feature-gated)
    core_sections = ['organization', 'metadata', 'build', 'image', 'documentation']

    for section in core_sections:
        # Start with defaults using deep copy
        if section in defaults:
            merged[section] = copy.deepcopy(defaults[section])

        # Override with project settings
        if section in project:
            merged[section] = deep_merge(  # type: ignore[arg-type]
                merged.get(section, {}),  # type: ignore[arg-type]
                project[section]  # type: ignore[index]
            )

    # Add features section for reference (shows what's enabled/disabled)
    merged['features'] = features

    return merged  # type: ignore


def validate_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate configuration has required fields.

    Args:
        config: Merged configuration

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Required fields
    required_fields = [
        ('image.name', 'Image name is required'),
        ('image.description', 'Image description is required'),
    ]

    for field_path, error_msg in required_fields:
        keys = field_path.split('.')
        value: Any = config  # type: ignore

        try:
            for key in keys:
                value = value[key]

            # Check if value is empty
            if not value or (isinstance(value, str) and not value.strip()):
                errors.append(f"{error_msg}: {field_path} is empty")  # type: ignore[union-attr]
        except (KeyError, TypeError):
            errors.append(f"{error_msg}: {field_path} not found")  # type: ignore[union-attr]

    # Validate platform architectures if present
    if 'build' in config and 'platforms' in config['build']:
        valid_platforms = [
            'linux/amd64', 'linux/arm64', 'linux/arm/v7', 'linux/arm/v6',
            'linux/386', 'linux/ppc64le', 'linux/s390x'
        ]
        platforms = config['build']['platforms']

        if not isinstance(platforms, list) or not platforms:
            errors.append("build.platforms must be a non-empty list")  # type: ignore[union-attr]
        else:
            for platform in platforms:  # type: ignore
                if platform not in valid_platforms:
                    msg = f"Invalid platform: {platform}. "
                    msg += f"Valid: {','.join(valid_platforms)}"
                    errors.append(msg)  # type: ignore[union-attr]

    return errors  # type: ignore


def flatten_for_display(
    config: Dict[str, Any],
    prefix: str = '',
    max_depth: int = 3,
    current_depth: int = 0
) -> List[str]:
    """
    Flatten config to show what's activated (for logging).

    Args:
        config: Configuration dictionary
        prefix: Key prefix for nested items
        max_depth: Maximum nesting depth to display
        current_depth: Current nesting level

    Returns:
        List of formatted config lines
    """
    lines = []

    if current_depth >= max_depth:
        return [f"{prefix}: <nested>"]

    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            lines.extend(flatten_for_display(value, full_key, max_depth, current_depth + 1))  # type: ignore
        elif isinstance(value, list):
            lines.append(f"{full_key}: [{len(value)} items]")  # type: ignore
        else:
            lines.append(f"{full_key}: {value}")  # type: ignore[union-attr]

    return lines  # type: ignore


def main() -> None:
    """Main entry point for configuration merger."""

    # File paths
    defaults_file = Path('vars/defaults.yml')
    project_file = Path('/tmp/project.yml')
    output_file = Path('/tmp/merged_config.yml')

    print("=" * 70)
    print("Docker Scaffold Configuration Merger")
    print("=" * 70)

    # Check project file exists (required)
    if not project_file.exists():
        print(f"\n❌ Error: {project_file} not found")
        print("   Please mount your project.yml to /tmp/project.yml")
        sys.exit(1)

    # Load defaults (optional but recommended)
    defaults: Dict[str, Any] = {}
    if defaults_file.exists():
        try:
            with open(defaults_file) as f:
                defaults = yaml.safe_load(f) or {}  # type: ignore
            print(f"✓ Loaded defaults from {defaults_file}")
        except yaml.YAMLError as e:
            print(f"❌ Error parsing {defaults_file}: {e}")
            sys.exit(1)
    else:
        print(f"⚠ Warning: {defaults_file} not found, using project.yml only")

    # Load project configuration (required)
    try:
        with open(project_file) as f:
            project: Dict[str, Any] = yaml.safe_load(f) or {}  # type: ignore
        print(f"✓ Loaded project from {project_file}")
    except yaml.YAMLError as e:
        print(f"❌ Error parsing {project_file}: {e}")
        sys.exit(1)

    # Merge configurations with feature activation
    print("\nMerging configurations with feature bundles...")
    merged: Dict[str, Any] = activate_feature_bundles(defaults, project)

    # Show activated features
    features: Dict[str, Any] = merged.get('features', {})
    if features:
        print("\nActivated features:")
        for feature, enabled in features.items():
            status = "✓" if enabled else "○"
            print(f"  {status} {feature}: {enabled}")

    # Validate merged configuration
    print("\nValidating configuration...")
    errors: List[str] = validate_config(merged)

    if errors:
        print("\n❌ Validation failed:\n")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)

    image_name = merged.get('image', {}).get('name', 'unknown')
    print(f"✓ Validation passed for image: {image_name}")

    # Write merged configuration
    try:
        with open(output_file, 'w') as f:
            yaml.dump(merged, f, default_flow_style=False, sort_keys=False, indent=2)
        print(f"\n✓ Generated {output_file}")
    except Exception as e:
        print(f"\n❌ Error writing output file: {e}")
        sys.exit(1)

    # Success summary
    print("=" * 70)
    print(f"🎉 Configuration ready for: {image_name}")
    print("=" * 70)
    print(f"\nNext: Ansible will use {output_file} to generate scaffold")


if __name__ == '__main__':
    sys.exit(main())
