<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Compliance Role

Generates code quality and compliance configuration files for Docker scaffold projects.

## Description

This role manages compliance and code quality tools configuration:

- **Conform**: Commit message validation (Conventional Commits)
- **MegaLinter**: Multi-language code linting and formatting
- **REUSE**: License compliance and SPDX header validation
- **publiccode.yaml**: Public code metadata (optional, for Italian public code registry)

## Requirements

None. All tools run via Docker containers.

## Role Variables

### Feature Flags (defaults/main.yml)

```yaml
compliance:
  conform: true        # Enable commit message validation
  megalinter: true     # Enable code linting
  reuse: true          # Enable license compliance
  publiccode: false    # Enable publiccode.yaml (optional)
```

### Configuration Locations

Variables are inherited from:

1. `ansible/vars/defaults.yaml` - Organization defaults
2. `project.yaml` - Per-project overrides

### File Exclusion

Use `template.exclude` to skip individual files:

```yaml
template:
  exclude:
    - .mega-linter.yaml  # Skip MegaLinter config
    - REUSE.toml         # Skip REUSE config
```

## Dependencies

None.

## Example Usage

### Enable only specific tools

```yaml
compliance:
  conform: true
  megalinter: true
  reuse: false         # Skip license compliance
  publiccode: false    # Skip publiccode.yaml
```

### Enable publiccode.yaml for Italian projects

```yaml
compliance:
  publiccode: true     # Enable for public code registry
```

## Generated Files

| File | Purpose | Tool |
|------|---------|------|
| `.conform.yaml` | Commit message validation policy | Conform |
| `.mega-linter.yaml` | Code linting configuration | MegaLinter |
| `REUSE.toml` | License compliance rules | REUSE |
| `publiccode.yaml` | Public code metadata | publiccode-parser-go |

## License

Apache-2.0

## Author Information

Broadsage - <opensource@broadsage.com>
