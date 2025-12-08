<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# GitHub Role

Generates GitHub issue templates and configuration files for your repository.

## Overview

This Ansible role creates a complete set of GitHub issue templates following industry best practices. It generates:

- **Bug Report Template** - Comprehensive bug reporting with environment details
- **Feature Request Template** - Feature suggestions with priority and use cases
- **Documentation Template** - Documentation improvement requests
- **Question/Support Template** - User support and questions
- **Config File** - Contact links for discussions, documentation, and security

All templates use modern YAML-based forms with validation and are fully customizable through variables from `project.yml`.

## Requirements

| Requirement | Version | Purpose |
|------------|---------|---------|
| Ansible | 2.9+ | Role execution |
| Git repository | - | Target must have `.github/` directory support |

## Role Variables

Variables are sourced from `ansible/vars/common.yml`, which maps `project.yml` configuration to role-friendly names.

### Core Variables

| Variable | Source | Default | Description |
|----------|--------|---------|-------------|
| `project_name` | `project.name` | `docker-scaffold` | Project name |
| `project_organization` | `project.organization` | `broadsage` | GitHub organization |
| `project_description` | `project.description` | - | Project description |
| `project_version` | `project.version` | `1.0.0` | Version number |
| `project_license` | `project.license` | `Apache-2.0` | License identifier |

### GitHub Configuration

| Variable | Source | Default | Description |
|----------|--------|---------|-------------|
| `github_issues` | `github.issues` | `true` | Enable issue templates |
| `github_workflows` | `github.workflows` | `true` | Enable workflows |
| `github_project_enabled` | `github.projects.enabled` | `false` | Enable Projects integration |
| `github_project_number` | `github.projects.number` | `1` | Project number for auto-assignment |

### Registry Configuration

Used in issue templates for Docker commands:

| Variable | Source | Default | Description |
|----------|--------|---------|-------------|
| `registry_primary_provider` | `registries.primary.provider` | `ghcr.io` | Registry provider |
| `registry_primary_namespace` | `registries.primary.namespace` | `broadsage` | Registry namespace |
| `registry_primary_image_name` | `registries.primary.image_name` | `scaffold` | Image name |

### Metadata

| Variable | Source | Default | Description |
|----------|--------|---------|-------------|
| `maintainer_name` | `metadata.maintainer.name` | `Broadsage Maintainers` | Maintainer name |
| `maintainer_email` | `metadata.maintainer.email` | `opensource@broadsage.com` | Contact email |
| `vendor_name` | `metadata.vendor` | `Broadsage Corporation Limited` | Vendor name |

### Variable Flow

```text
project.yml → common.yml → Role Templates
```

1. **project.yml** - Central configuration file with all project settings
2. **common.yml** - Maps nested YAML structure to flat role variables
3. **Templates** - Use variables from common.yml with Jinja2

## Dependencies

None.

## Example Playbook

### Basic Usage

```yaml
- name: Generate GitHub templates
  hosts: localhost
  connection: local
  gather_facts: false
  
  pre_tasks:
    - name: Load project configuration
      ansible.builtin.include_vars:
        file: "project.yml"
    
    - name: Load common variables
      ansible.builtin.include_vars:
        file: "vars/common.yml"
  
  roles:
    - role: github
      tags: 
        - github
```

### Minimal project.yml

```yaml
---
project:
  name: docker-scaffold
  organization: broadsage
  description: Ansible-powered scaffolding tool

github:
  issues: true
  projects:
    enabled: true
    number: 6

registries:
  primary:
    provider: ghcr.io
    namespace: broadsage
    image_name: scaffold
```

### With Tags

```yaml
- hosts: localhost
  roles:
    - role: github
      tags: 
        - github
        - scaffold
        - templates
```

## Generated Files

```text
.github/
└── ISSUE_TEMPLATE/
    ├── bug-report.yml         # Bug reporting with environment details
    ├── feature-request.yml    # Feature suggestions with priority
    ├── documentation.yml      # Documentation improvements
    ├── question.yml           # Support and questions
    └── config.yml             # Contact links configuration
```

## Features

### Modern YAML Forms

- ✅ GitHub issue forms (YAML-based, not markdown)
- ✅ Structured data with validation
- ✅ Rich input types: dropdowns, checkboxes, text areas
- ✅ Required field validation
- ✅ Syntax highlighting for code blocks

### Customization

- ✅ Project-specific placeholders from `project.yml`
- ✅ Conditional GitHub Projects integration
- ✅ Dynamic Docker registry references
- ✅ Templated URLs and links

### Best Practices

- ✅ Industry-standard template structure
- ✅ Modern emojis for visual clarity (💭📚🛡️🆘)
- ✅ Private security vulnerability reporting
- ✅ Prevents blank issues
- ✅ Comprehensive prerequisite checks
- ✅ Environment and architecture detection

## Conditional Rendering

Templates support conditional blocks based on configuration:

```jinja
{% if github_project_enabled and github_project_number %}
projects: ["{{ project_organization }}/{{ github_project_number }}"]
{% endif %}
```

**To disable GitHub Projects:**

```yaml
# project.yml
github:
  projects:
    enabled: false  # Skips projects line in templates
```

## Testing

```bash
# Run only github role
ansible-playbook generate.yml --tags github

# Run with verbose output
ansible-playbook generate.yml --tags github -vvv

# Check syntax
ansible-playbook generate.yml --syntax-check
```

## Troubleshooting

### Templates Not Generated

**Check:**

- `project.yml` exists and is valid YAML
- `common.yml` is loaded in playbook pre_tasks
- Target directory is writable

### Variables Not Replaced

**Ensure:**

- Variables are defined in `project.yml`
- `common.yml` is loaded before role execution
- Variable names match exactly (case-sensitive)

### GitHub Projects Not Applied

**Verify:**

- `github.projects.enabled: true` in `project.yml`
- `github.projects.number` is set
- Both conditions must be met for projects to be added

## License

MIT-0

## Author Information

**Created by:** Broadsage  
**Project:** docker-scaffold  
**Repository:** https://github.com/broadsage/docker-scaffold

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

## Support

- 📖 [Documentation](https://github.com/broadsage/docker-scaffold)
- 💬 [Discussions](https://github.com/broadsage/docker-scaffold/discussions)
- 🐛 [Issues](https://github.com/broadsage/docker-scaffold/issues)
