<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Using docker-scaffold as a Template

Complete guide for generating new Docker image projects from this template using Cookiecutter.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Template Variables](#template-variables)
- [Advanced Usage](#advanced-usage)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- **Python 3.8+**
- **Cookiecutter** (`pip install cookiecutter`)
- **Docker** (for building images)
- **yq** (for YAML manipulation in hooks)

### Optional but Recommended

- **Task** (`brew install go-task/tap/go-task`) - Task runner
- **Git** - Version control
- **GitHub CLI** (`gh`) - GitHub integration

### Installation

```bash
# Install cookiecutter
pip install cookiecutter

# Install yq (macOS)
brew install yq

# Install yq (Linux)
wget -qO /usr/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
chmod +x /usr/bin/yq

# Install Task (optional)
brew install go-task/tap/go-task
```

---

## Quick Start

### Method 1: From GitHub (Recommended)

```bash
# Generate new project interactively
cookiecutter gh:broadsage/docker-scaffold

# Follow the prompts:
# organization [broadsage]: mycompany
# project_name [my-docker-image]: nginx-custom
# project_short_description [Docker image for awesome application]: Custom NGINX with modules
# maintainer_name [Broadsage]: John Doe
# maintainer_email [opensource@broadsage.com]: john@mycompany.com
# ...

# Result:
cd nginx-custom/
```

### Method 2: From Local Template

```bash
# Clone template first
git clone https://github.com/broadsage/docker-scaffold.git

# Generate from local path
cookiecutter ./docker-scaffold

# Follow prompts...
```

### Method 3: Non-Interactive (CI/CD)

```bash
# Using JSON config file
cat > project-config.json <<EOF
{
  "organization": "mycompany",
  "project_name": "nginx-custom",
  "project_short_description": "Custom NGINX with SSL modules",
  "maintainer_name": "DevOps Team",
  "maintainer_email": "devops@mycompany.com",
  "license": "Apache-2.0",
  "features_github": "y",
  "features_security": "y",
  "git_init": "y",
  "git_initial_commit": "y"
}
EOF

cookiecutter gh:broadsage/docker-scaffold --no-input --config-file project-config.json
```

---

## Template Variables

### Core Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `organization` | GitHub organization/username | `broadsage` | `mycompany` |
| `project_name` | Human-readable project name | `my-docker-image` | `NGINX Custom` |
| `project_slug` | URL-safe project identifier | *auto-generated* | `nginx-custom` |
| `project_short_description` | Brief description | `Docker image for...` | `Custom NGINX` |

### Maintainer Information

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `maintainer_name` | Package maintainer name | `Broadsage` | `John Doe` |
| `maintainer_email` | Contact email | `opensource@...` | `john@example.com` |
| `vendor` | Organization legal name | `Broadsage Corporation Limited` | `MyCompany Inc.` |

### License Selection

| Variable | Options | Default |
|----------|---------|---------|
| `license` | `Apache-2.0`, `MIT`, `GPL-3.0`, `BSD-3-Clause`, `MPL-2.0` | `Apache-2.0` |

### Build Configuration

| Variable | Options | Default |
|----------|---------|---------|
| `build_platforms` | `multi-arch (amd64 + arm64)`, `amd64-only`, `arm64-only`, `custom` | `multi-arch` |

### Feature Flags

| Variable | Description | Default |
|----------|-------------|---------|
| `features_github` | Enable GitHub Actions/templates | `y` |
| `features_security` | Enable security scanning | `y` |
| `features_registry` | Enable registry push | `y` |
| `features_compliance` | Enable compliance tools | `y` |

### Compliance Tools

| Variable | Description | Default |
|----------|-------------|---------|
| `compliance_conform` | Commit message validation | `y` |
| `compliance_megalinter` | Multi-language linting | `y` |
| `compliance_reuse` | SPDX license headers | `y` |

### GitHub Options

| Variable | Description | Default |
|----------|-------------|---------|
| `github_discussions` | Enable GitHub Discussions | `n` |
| `github_projects` | Enable GitHub Projects | `n` |

### Registry Options

| Variable | Description | Default |
|----------|-------------|---------|
| `registry_dockerhub` | Push to Docker Hub | `y` |
| `registry_ghcr` | Push to GitHub Container Registry | `y` |

### Git Options

| Variable | Description | Default |
|----------|-------------|---------|
| `git_init` | Initialize git repository | `y` |
| `git_initial_commit` | Create initial commit | `y` |
| `git_remote_url` | Git remote URL (optional) | `` |

---

## Advanced Usage

### Custom Configuration File

Create reusable configuration for your organization:

```yaml
# ~/.cookiecutterrc
default_context:
  organization: "mycompany"
  maintainer_name: "DevOps Team"
  maintainer_email: "devops@mycompany.com"
  vendor: "MyCompany Inc."
  license: "MIT"
  features_security: "y"
  features_compliance: "y"
  registry_dockerhub: "n"
  registry_ghcr: "y"
```

Now all projects will use these defaults:

```bash
cookiecutter gh:broadsage/docker-scaffold
# Only prompted for project-specific values
```

### Automated GitHub Repository Creation

```bash
# Generate project
cookiecutter gh:broadsage/docker-scaffold

# Enter generated project
cd your-project-name/

# Create GitHub repo and push
gh repo create mycompany/your-project-name --source=. --public --push
```

### CI/CD Integration (GitHub Actions)

```yaml
# .github/workflows/scaffold-projects.yml
name: Generate Docker Project

on:
  workflow_dispatch:
    inputs:
      project_name:
        description: 'Project name'
        required: true

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Install cookiecutter
        run: pip install cookiecutter
      
      - name: Generate project
        run: |
          cookiecutter gh:broadsage/docker-scaffold \
            --no-input \
            project_name="${{ github.event.inputs.project_name }}" \
            organization="${{ github.repository_owner }}" \
            git_init="y"
      
      - name: Create repository
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          cd "${{ github.event.inputs.project_name }}"
          gh repo create "${{ github.repository_owner }}/${{ github.event.inputs.project_name }}" \
            --source=. --public --push
```

---

## Customization

### After Generation

1. **Review Configuration**
   ```bash
   cd your-project/
   cat project.yaml
   cat ansible/vars/defaults.yaml
   ```

2. **Customize Features**
   ```bash
   # Enable/disable features in project.yaml
   yq eval -i '.features.github = true' project.yaml
   yq eval -i '.compliance.megalinter = false' ansible/vars/defaults.yaml
   ```

3. **Generate Project Files**
   ```bash
   # Using Task
   task generate
   
   # Or using Docker
   docker run --rm -v $(pwd):/output ghcr.io/broadsage/scaffold
   ```

4. **Build & Test**
   ```bash
   task build
   task compliance
   ```

### Template Exclusions

Exclude files from generated projects by editing `project.yaml`:

```yaml
template:
  exclude:
    - REUSE.toml        # Skip REUSE if not needed
    - .mega-linter.yaml # Skip megalinter config
```

---

## Troubleshooting

### Cookiecutter Not Found

```bash
# Install globally
pip install --user cookiecutter

# Or in virtual environment
python3 -m venv venv
source venv/bin/activate
pip install cookiecutter
```

### YQ Command Not Found

Post-generation hooks require `yq` for YAML manipulation:

```bash
# macOS
brew install yq

# Linux
sudo wget -qO /usr/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/bin/yq

# Windows (WSL/Git Bash)
choco install yq
```

### Git Not Initialized

If `git_init=y` but git wasn't initialized:

```bash
cd your-project/
git init
git add .
git commit -s -m "feat: initialize project from template"
```

### Permission Denied on Hooks

```bash
# Make hooks executable
chmod +x hooks/*.py
```

### Template Variables Not Replaced

Ensure you're using cookiecutter, not regular `git clone`:

```bash
# ❌ Wrong
git clone https://github.com/broadsage/docker-scaffold.git

# ✅ Correct
cookiecutter gh:broadsage/docker-scaffold
```

---

## Examples

### Example 1: Simple NGINX Image

```bash
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  project_name="nginx-alpine" \
  project_short_description="Lightweight NGINX on Alpine Linux" \
  build_platforms="amd64-only" \
  features_github="n" \
  git_init="y"
```

### Example 2: Enterprise Application

```bash
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  organization="mycompany" \
  project_name="api-gateway" \
  project_short_description="Company API Gateway Service" \
  maintainer_name="Platform Team" \
  maintainer_email="platform@mycompany.com" \
  license="MIT" \
  build_platforms="multi-arch (amd64 + arm64)" \
  features_security="y" \
  compliance_conform="y" \
  compliance_megalinter="y" \
  github_discussions="y" \
  github_projects="y" \
  git_init="y" \
  git_remote_url="https://github.com/mycompany/api-gateway.git"
```

### Example 3: Minimal Setup

```bash
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  project_name="simple-app" \
  features_github="n" \
  features_security="n" \
  features_compliance="n" \
  git_init="n"
```

---

## Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [docker-scaffold Repository](https://github.com/broadsage/docker-scaffold)
- [Task Documentation](https://taskfile.dev/)
- [Docker BuildX](https://docs.docker.com/buildx/working-with-buildx/)

---

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/broadsage/docker-scaffold/issues)
- **Discussions**: [GitHub Discussions](https://github.com/broadsage/docker-scaffold/discussions)
- **Email**: <opensource@broadsage.com>
