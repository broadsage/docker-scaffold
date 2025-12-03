# Python Scripts for Configuration Merging

## Overview

Python scripts that handle the complex configuration merging logic for docker-scaffold.

## Files

- **`merge_config.py`** - Main configuration merger script
- **`test_merge_config.py`** - Unit tests for the merger
- **`requirements.txt`** - Python dependencies

## Installation

Install dependencies (only needed for local testing):

```bash
pip install -r requirements.txt
```

**Note:** The Docker container already has PyYAML installed, so this is only needed for local development.

## Usage

### In Docker Container (Production)

The script runs automatically when the container starts:

```bash
docker run -v $(pwd)/project.yml:/tmp/project.yml ghcr.io/broadsage/scaffold
```

### Local Testing

```bash
# Run unit tests
cd ansible/scripts
python3 test_merge_config.py

# Test merge manually
python3 merge_config.py
```

## How It Works

```text
defaults.yml + project.yml → merge_config.py → merged_config.yml → Ansible
```

### Feature Activation Logic

1. **Feature enabled** (`features.github: true`)
   - Loads entire `github.*` bundle from `defaults.yml`
   - Applies project-specific overrides from `project.yml`

2. **Feature disabled** (`features.github: false`)
   - Skips entire `github.*` bundle
   - Ignores any `github.*` settings in `project.yml`

### Example

**defaults.yml:**

```yaml
github:
  workflows: true
  issues: true
  projects:
    enabled: false
```

**project.yml:**

```yaml
features:
  github: true

github:
  issues: false
  projects:
    enabled: true
    number: 6
```

**Result (merged_config.yml):**

```yaml
github:
  workflows: true      # From defaults
  issues: false        # Overridden
  projects:
    enabled: true      # Overridden
    number: 6          # Overridden
```

## Functions

### `deep_merge(base, override)`

Recursively merges two dictionaries. Override values win on conflicts.

### `activate_feature_bundles(defaults, project)`

Activates feature bundles based on `features.*` flags and merges with project overrides.

### `validate_config(config)`

Validates merged configuration:

- Required fields present
- Valid platform architectures
- Non-empty values

## Validation Rules

- `image.name` - Required, non-empty
- `image.description` - Required, non-empty
- `build.platforms` - Must be valid architectures

Valid platforms:

- `linux/amd64`
- `linux/arm64`
- `linux/arm/v7`
- `linux/arm/v6`
- `linux/386`
- `linux/ppc64le`
- `linux/s390x`

## Error Handling

The script provides clear error messages:

```bash
❌ Error: /tmp/project.yml not found
   Please mount your project.yml to /tmp/project.yml

❌ Validation failed:
  • Image name is required: image.name not found
  • Invalid platform: linux/invalid. Valid: linux/amd64, linux/arm64, ...
```

## Testing

Run all tests:

```bash
python3 test_merge_config.py
```

Tests cover:

- Deep merge logic
- Feature activation
- Nested overrides
- Validation rules
- Edge cases

## Troubleshooting

### PyYAML not found

```bash
pip install pyyaml
```

### Script not executable

```bash
chmod +x merge_config.py
```

### Tests failing

Check you're in the correct directory:

```bash
cd ansible/scripts
python3 test_merge_config.py
```
