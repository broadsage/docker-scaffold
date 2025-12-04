#!/usr/bin/env python3
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


def _get_feature_bundle_map() -> Dict[str, List[str]]:
    """
    Get the feature bundle mapping (features → config sections).

    Returns:
        Dictionary mapping feature names to bundle keys
    """
    return {
        'github': ['github'],
        'security': ['security'],
        'registry': ['registry'],
        'signing': ['security'],  # Part of security bundle
        'sbom': ['security'],     # Part of security bundle
    }


def _get_safe_defaults() -> Dict[str, Any]:
    """
    Get safe default values for all feature bundles (when disabled).

    These ensure all variables are always present in merged config,
    even when features are disabled. Ansible conditions work gracefully
    without undefined variable errors.

    Returns:
        Dictionary of safe default values for disabled features
    """
    return {
        'github': {
            'issues': False,
            'workflows': False,
            'dependabot': False,
            'pull_requests': False,
            'projects': {
                'enabled': False,
                'number': 0
            }
        },
        'security': {
            'scan': {
                'enabled': False,
                'provider': [],
                'severity': [],
                'fail_on_severity': 'CRITICAL'
            },
            'signing': False,
            'sbom': {
                'enabled': False,
                'format': 'spdx'
            }
        },
        'registry': {
            'github': False,
            'dockerhub': False
        }
    }


def activate_feature_bundles(defaults: Dict[str, Any], project: Dict[str, Any]) -> Dict[str, Any]:
    """
    Activate feature bundles based on features.* flags.

    Feature Bundle Mapping:
      - features.github → github.*
      - features.security → security.*
      - features.registry → registry.*
      - features.signing → security.signing
      - features.sbom → security.sbom

    When a feature is disabled, safe default values are used to ensure
    all variables are always present in the merged config. This prevents
    undefined variable errors in Ansible tasks.

    Args:
        defaults: Default configuration with feature bundles
        project: Project-specific configuration

    Returns:
        Merged configuration with all features (enabled or disabled)
    """
    merged: Dict[str, Any] = {}
    features: Dict[str, Any] = project.get('features', {})
    feature_bundles = _get_feature_bundle_map()
    safe_defaults = _get_safe_defaults()
    activated_bundles: Set[str] = set()

    # Activate feature bundles (only if enabled)
    for feature_name, bundle_keys in feature_bundles.items():
        feature_enabled = features.get(feature_name, False)

        if feature_enabled:
            for bundle_key in bundle_keys:  # type: ignore
                if bundle_key in activated_bundles:
                    continue

                # Load bundle from defaults using deep copy
                if bundle_key in defaults:
                    merged[bundle_key] = copy.deepcopy(defaults[bundle_key])
                    activated_bundles.add(bundle_key)

    # Apply project-specific overrides (separate loop to avoid duplicate merges)
    for feature_name, bundle_keys in feature_bundles.items():
        feature_enabled = features.get(feature_name, False)

        if feature_enabled:
            for bundle_key in bundle_keys:
                # Override with project-specific settings
                if bundle_key in project and bundle_key in merged:
                    merged[bundle_key] = deep_merge(  # type: ignore[arg-type]
                        merged[bundle_key],  # type: ignore[index]
                        project[bundle_key]
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
                project[section]
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
