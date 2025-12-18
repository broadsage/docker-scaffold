<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->
<!-- markdownlint-configure-file { "MD033": { "allowed_elements": ["details", "summary", "b"] } } -->

# Docker Scaffold Template Usage Guide

Generate production-ready Docker image projects with best practices built-in using Cookiecutter & Ansible.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Methods](#usage-methods)
- [Template Variables](#template-variables)
- [Customization Guide](#customization-guide)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Troubleshooting

## Overview

**docker-scaffold** is a Cookiecutter template for creating Docker image projects with:

✅ **Multi-architecture support** - Build for AMD64, ARM64, and more  
✅ **Security by default** - Automated vulnerability scanning and security policies  
✅ **Compliance tools** - REUSE, MegaLinter, and commit validation  
✅ **CI/CD ready** - GitHub Actions workflows included  
✅ **Best practices** - Industry-standard project structure and tooling  

### Why Use This Template?

- **Save time**: Skip repetitive setup and configuration
- **Consistency**: Standardize Docker projects across your organization
- **Best practices**: Built-in security, testing, and compliance tools
- **Flexibility**: Modular features you can enable/disable as needed
- **Maintenance**: Easy updates when best practices evolve

### Who Should Use This?

- DevOps teams building Docker images
- Organizations standardizing container workflows
- Developers creating custom base images
- Platform engineers managing container infrastructure

## Quick Start

Get started in 60 seconds:

```bash
# 1. Install Cookiecutter
pip install cookiecutter

# 2. Generate your project
cookiecutter gh:broadsage/docker-scaffold

# 3. Navigate to your new project
cd <your-project-name>

# 4. Review generated files
ls -la
```

That's it! You now have a production-ready Docker project structure.

## Installation

### System Requirements

| Requirement | Minimum Version | Purpose |
|-------------|----------------|---------|
| Python | 3.8+ | Run Cookiecutter |
| pip | 20.0+ | Install Python packages |
| Git | 2.0+ | Version control |

### Required Tools

Install Cookiecutter (the only hard requirement):

```bash
# Using pip
pip install --user cookiecutter

# Using pipx (recommended)
pipx install cookiecutter

# Verify installation
cookiecutter --version
```

### Optional Tools

These enhance functionality but aren't required for basic usage:

<details>
<summary><b>yq</b> - YAML processor (for advanced customization)</summary>

```bash
# macOS
brew install yq

# Linux
sudo wget -qO /usr/bin/yq \
  https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/bin/yq

# Verify
yq --version
```

</details>

<details>
<summary><b>Task</b> - Task runner (simplifies common operations)</summary>

```bash
# macOS
brew install go-task/tap/go-task

# Linux (via sh installer)
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

# Verify
task --version
```

</details>

<details>
<summary><b>GitHub CLI</b> - Automate repository creation</summary>

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
  sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
  https://cli.github.com/packages stable main" | \
  sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Authenticate
gh auth login
```

</details>

<details>
<summary><b>Docker<b> - Build and test generated projects</summary>

```bash
# Installation varies by platform
# See: https://docs.docker.com/get-docker/

# Verify
docker --version
docker buildx version
```

</details>

## Usage Methods

### Interactive Mode (Recommended for First-Time Users)

Generate a project by answering prompts:

```bash
cookiecutter gh:broadsage/docker-scaffold
```

**Example session:**

```text
organization [broadsage]: mycompany
project_name [my-docker-image]: nginx-custom  
project_short_description [Docker image for awesome application]: Custom NGINX with SSL
maintainer_name [Broadsage]: John Doe
maintainer_email [opensource@broadsage.com]: john@mycompany.com
license [Apache-2.0]: MIT
build_platforms [multi-arch (amd64 + arm64)]: 
features_github [y]: 
features_security [y]: 
...
```

### Non-Interactive Mode (For Automation)

Use configuration files for reproducible builds:

```bash
# Create configuration file
cat > my-config.json <<EOF
{
  "organization": "mycompany",
  "project_name": "nginx-custom",
  "project_short_description": "Custom NGINX with SSL modules",
  "maintainer_name": "DevOps Team",
  "maintainer_email": "devops@mycompany.com",
  "license": "Apache-2.0",
  "build_platforms": "multi-arch (amd64 + arm64)",
  "features_github": "y",
  "features_security": "y",
  "git_init": "y"
}
EOF

# Generate without prompts
cookiecutter gh:broadsage/docker-scaffold --no-input --config-file my-config.json
```

### Local Template Mode (For Development)

Work with a local copy of the template:

```bash
# Clone template repository
git clone https://github.com/broadsage/docker-scaffold.git

# Generate from local path
cookiecutter ./docker-scaffold

# Or specify a branch/tag
cookiecutter ./docker-scaffold --checkout develop
```

### Using a Cookiecutter Config File

Store defaults in `~/.cookiecutterrc` for all projects:

```yaml
# ~/.cookiecutterrc
default_context:
  organization: "mycompany"
  maintainer_name: "Platform Team"
  maintainer_email: "platform@mycompany.com"
  vendor: "MyCompany Inc."
  license: "MIT"
  features_security: "y"
  features_compliance: "y"
  registry_dockerhub: "n"
  registry_ghcr: "y"

abbreviations:
  ds: https://github.com/broadsage/docker-scaffold.git
```

Now you can use abbreviations:

```bash
cookiecutter ds
# Automatically uses your defaults
```

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

### Customization Guide

How to tailor the generated project to your needs.

### Post-Generation Steps

After generating your project, follow these steps:

#### 1. Review Generated Configuration

```bash
cd your-project-name/

# View project metadata
cat project.yaml

# Review feature flags
yq eval '.features' project.yaml

# Check Ansible configuration
cat ansible/vars/defaults.yaml
```

#### 2. Customize Features

Enable or disable features by editing `project.yaml`:

```yaml
# project.yaml
features:
  github: true
  security: true
  registry: true
  compliance: true

compliance:
  conform: true
  megalinter: true
  reuse: true
```

#### 3. Regenerate Project Files

After modifying configuration:

```bash
# Using Task (recommended)
task generate

# Or using Docker
docker run --rm -v $(pwd):/output ghcr.io/broadsage/scaffold

# Or using Ansible directly
ansible-playbook ansible/generate.yaml
```

#### 4. Customize the Dockerfile

Edit `Dockerfile` for your specific needs:

```dockerfile
# Add build arguments
ARG NODE_VERSION=20

# Install dependencies
RUN apk add --no-cache nodejs=${NODE_VERSION}

# Copy application files
COPY src/ /app/
```

#### 5. Add Custom Tasks

Extend `Taskfile.yml` with your own tasks:

```yaml
# Taskfile.yml
version: '3'

taskAutomated Repository Creation

Complete automation from template to GitHub:

```bash
#!/bin/bash
# create-project.sh

PROJECT_NAME="$1"
ORGANIZATION="mycompany"

# Generate project
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  project_name="$PROJECT_NAME" \
  organization="$ORGANIZATION" \
  git_init="y"

# Navigate to project
cd "$PROJECT_NAME" || exit

# Create GitHub repository and push
gh repo create "$ORGANIZATION/$PROJECT_NAME" \
  --source=. \
  --public \
  --push \
  --description "$(yq eval '.description' project.yaml)"

echo "✅ Project created: https://github.com/$ORGANIZATION/$PROJECT_NAME"
```

Usage:

```bash
chmod +x create-project.sh
./create-project.sh my-new-service
```

### CI/CD Pipeline Integration

#### GitHub Actions Workflow

Automate project generation in your CI/CD:

```yaml
# .github/workflows/scaffold-new-project.yml
name: Generate New Docker Project

on:
  workflow_dispatch:
    inputs:
      project_name:
        description: 'Project name (kebab-case)'
        required: true
        type: string
      description:
        description: 'Project description'
        required: true
        type: string
      platforms:
        description: 'Build platforms'
        required: false
        default: 'multi-arch (amd64 + arm64)'
        type: choice
        options:
          - 'multi-arch (amd64 + arm64)'
          - 'amd64-only'
          - 'arm64-only'

jobs:
  generate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      
    steps:
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Cookiecutter
        run: pip install cookiecutter
      
      - name: Generate Project
        run: |
          cookiecutter gh:broadsage/docker-scaffold \
            --no-input \
            project_name="${{ inputs.project_name }}" \
            project_short_description="${{ inputs.description }}" \
            organization="${{ github.repository_owner }}" \
            build_platforms="${{ inputs.platforms }}" \
            git_init="y"
      
      - name: Create Repository
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          cd "${{ inputs.project_name }}"
          gh repo create \
            "${{ github.repository_owner }}/${{ inputs.project_name }}" \
            --source=. \
            --public \
            --push
      
      - name: Summary
        run: |
          echo "### ✅ Project Created" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Project**: ${{ inputs.project_name }}" >> $GITHUB_STEP_SUMMARY
          echo "**URL**: https://github.com/${{ github.repository_owner }}/${{ inputs.project_name }}" >> $GITHUB_STEP_SUMMARY
```

#### GitLab CI Integration

```yaml
# .gitlab-ci.yml
generate_project:
  stage: deploy
  image: python:3.11-slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "trigger"'
  script:
    - pip install cookiecutter
    - |
      cookiecutter gh:broadsage/docker-scaffold \
        --no-input \
        project_name="$PROJECT_NAME" \
        organization="$CI_PROJECT_NAMESPACE"
    - cd "$PROJECT_NAME"
    - git init
    - git add .
    - git commit -m "feat: initialize from template"
    - git remote add origin "$GITLAB_URL/$CI_PROJECT_NAMESPACE/$PROJECT_NAME.git"
    - git push -u origin main
```

### Template Customization & Forking

Create your own customized version:

```bash
# Fork the template
gh repo fork broadsage/docker-scaffold --clone

cd docker-scaffold/

# Customize default values
vi cookiecutter.json

# Modify templates
vi {{cookiecutter.project_slug}}/Dockerfile
vi ansible/roles/*/templates/*.j2

# Test locally
cookiecutter . --no-input

# Push to your organization
gh repo create myorg/custom-docker-scaffold --source=. --push

# Use your custom template
cookiecutter gh:myorg/custom-docker-scaffold
```

### Organization-Wide Standards

Enforce organization standards using a wrapper repository:

```text
company-templates/
├── docker-scaffold-config.yaml    # Default config
├── requirements.txt                # Locked versions
└── generate.sh                     # Wrapper script
```

**docker-scaffold-config.yaml:**

```yaml
default_context:
  organization: "mycompany"
  vendor: "MyCompany Inc."
  license: "MIT"
  maintainer_email: "devops@mycompany.com"
  features_security: "y"
  features_compliance: "y"
  compliance_megalinter: "y"
  registry_ghcr: "y"
  registry_dockerhub: "n"
```

**generate.sh:**

```bash
#!/bin/bash
set -euo pipefail

# Validate environment
command -v cookiecutter >/dev/null 2>&1 || {
  echo "❌ cookiecutter not found. Install: pip install cookiecutter"
  exit 1
}

# Use organization config
cookiecutter gh:broadsage/docker-scaffold \
  --config-file ./docker-scaffold-config.yaml \
  "$@"
```

### Version Pinning

Pin specific template versions for reproducibility:

```bash
# Use specific Git tag
cookiecutter gh:broadsage/docker-scaffold --checkout v1.2.3

# Use specific commit
cookiecutter gh:broadsage/docker-scaffold --checkout abc1234

# Use specific branch
cookiecutter gh:broadsage/docker-scaffold --checkout develop
```

Store in requirements:

```text
# requirements-templates.txt
cookiecutter==2.5.0
```

```bash
pip install -r requirements-templates.txt
cookiecutter gh:broadsage/docker-scaffold --checkout v1.2.3
### Example 2: Enterprise Application

**Use case**: Production API gateway with full compliance

```bash
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  organization="mycompany" \
  project_name="api-gateway" \
  project_short_description="Company API Gateway Service" \
  maintainer_name="Platform Team" \
  maintainer_email="platform@mycompany.com" \
  vendor="MyCompany Inc." \
  license="MIT" \
  build_platforms="multi-arch (amd64 + arm64)" \
  features_github="y" \
  features_security="y" \
  features_compliance="y" \
  compliance_conform="y" \
  compliance_megalinter="y" \
  compliance_reuse="y" \
  github_discussions="y" \
  github_projects="y" \
  registry_dockerhub="y" \
  registry_ghcr="y" \
  git_init="y"
```

**What you get**: Full-featured project with CI/CD, security scanning, compliance tools

### Example 3: ARM64-Only IoT Image

**Use case**: Raspberry Pi or ARM-based edge devices

```bash
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  project_name="iot-sensor-collector" \
  project_short_description="IoT sensor data collector" \
  build_platforms="arm64-only" \
  features_security="y" \
  registry_dockerhub="n" \
  registry_ghcr="y"
```

**What you get**: ARM64-optimized project with security scanning

### Example 4: Multi-Organization Template

**Use case**: Multiple teams using same template with different defaults

Create organization-specific configs:

```bash
# team-a-config.json
{
  "organization": "team-a",
  "maintainer_name": "Team A",
  "maintainer_email": "team-a@company.com",
  "registry_dockerhub": "n",
  "registry_ghcr": "y"
}

# team-b-config.json
{
  "organization": "team-b",
  "maintainer_name": "Team B",
  "maintainer_email": "team-b@company.com",
  "registry_dockerhub": "y",
  "registry_ghcr": "n"
}
```

Generate projects:

```bash
# Team A project
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  --config-file team-a-config.json \
  project_name="team-a-app"

# Team B project
cookiecutter gh:broadsage/docker-scaffold \
  --no-input \
  --config-file team-b-config.json \
  project_name="team-b-service"
 docker-compose.yml          # Local testing setup
├── Taskfile.yml               # Task automation
├── project.yaml               # Project metadata
├── .conform.yaml              # Commit validation rules
├── .pre-commit-config.yaml    # Pre-commit hooks
├── .mega-linter.yml           # Linter configuration
├── REUSE.toml                 # License compliance
├── README.md                  # Project documentation
├── LICENSE                    # Project license
├── CODE_OF_CONDUCT.md        # Community guidelines
├── CONTRIBUTING.md            # Contribution guide
└── SECURITY.md               # Security policy
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `Dockerfile` | Container image definition |
| `Taskfile.yml` | Common tasks (build, test, publish) |
| `project.yaml` | Project configuration and metadata |
| `.github/workflows/` | Automated CI/CD pipelines |
| `docs/` | User and developer documentation |
| `.conform.yaml` | Enforces commit message standards |
| `REUSE.toml` | Manages license compliance |

### Conditional Files

Some files are only generated based on your configuration:

| Feature Flag | Generated Files |
|-------------|-----------------|
| `features_github=y` | `.github/*` templates and workflows |
| `features_security=y` | Security scanning workflows |
| `features_compliance=y` | `.mega-linter.yml`, `REUSE.toml` |
| `compliance_conform=y` | `.conform.yaml`, pre-commit hooks |

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
Common issues and their solutions.

### Installation Issues

<details>
<summary><b>❌ Cookiecutter command not found</b></summary>

**Symptoms:**
```bash
$ cookiecutter --version
-bash: cookiecutter: command not found
```

**Solution:**

```bash
# Check Python installation
python3 --version

# Install cookiecutter
pip3 install --user cookiecutter

# Add to PATH (if needed)
export PATH="$HOME/.local/bin:$PATH"

# Verify
cookiecutter --version
```

</details>

<details>
<summary><b>❌ Python version too old</b></summary>

**Symptoms:**

```text
ERROR: Python 3.7 or higher is required
```

**Solution:**

```bash
# Check current version
python3 --version

# Install Python 3.11 (recommended)
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv

# Verify
python3.11 --version
```

</details>

### Generation Issues

<details>
<summary><b>❌ Template not found or repository error</b></summary>

**Symptoms:**

```text
ERROR: Repository broadsage/docker-scaffold not found
```

**Solutions:**

```bash
# 1. Check internet connection
ping github.com

# 2. Use full HTTPS URL
cookiecutter https://github.com/broadsage/docker-scaffold.git

# 3. Clone locally first
git clone https://github.com/broadsage/docker-scaffold.git
cookiecutter ./docker-scaffold
```

</details>

<details>
<summary><b>❌ Hook execution failed (yq not found)</b></summary>

**Symptoms:**

```text
Error: yq: command not found
Hook script failed
```

**Solution:**

```bash
# macOS
brew install yq

# Linux (Ubuntu/Debian)
sudo wget -qO /usr/bin/yq \
  https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/bin/yq

# Verify
yq --version
```

**Alternative:** Skip hooks (not recommended):

```bash
cookiecutter gh:broadsage/docker-scaffold --no-input --skip-hooks
```

</details>

<details>
<summary><b>❌ Permission denied on hooks</b></summary>

**Symptoms:**

```text
Permission denied: hooks/post_gen_project.py
```

**Solution:**

```bash
# Make hooks executable
cd docker-scaffold/
chmod +x hooks/*.py

# Regenerate
cookiecutter .
```

</details>

### Configuration Issues

<details>
<summary><b>❌ Invalid project name format</b></summary>

**Symptoms:**

```text
Error: Project name must be lowercase with hyphens
```

**Valid formats:**

- ✅ `my-docker-image`
- ✅ `api-gateway`
- ✅ `nginx-alpine`

**Invalid formats:**

- ❌ `My_Docker_Image` (uppercase, underscores)
- ❌ `myDockerImage` (camelCase)
- ❌ `my.docker.image` (dots)

**Solution:**

```bash
# Convert to valid format
echo "My Docker Image" | tr '[:upper:]' '[:lower:]' | tr ' ' '-'
# Output: my-docker-image
```

</details>

<details>
<summary><b>❌ Template variables not replaced in generated files</b></summary>

**Symptoms:**
Seeing `{{cookiecutter.variable}}` in generated files

**Common cause:** Using `git clone` instead of `cookiecutter`

**Solution:**

```bash
# ❌ Wrong approach
git clone https://github.com/broadsage/docker-scaffold.git
cd docker-scaffold
# Files contain template syntax

# ✅ Correct approach
cookiecutter gh:broadsage/docker-scaffold
# Files have variables replaced
```

</details>

### Git Issues

<details>
<summary><b>❌ Git repository not initialized</b></summary>

**Symptoms:**
Selected `git_init=y` but no `.git` directory

**Solution:**

```bash
cd your-project/
git init
git add .
git commit -s -m "feat: initialize project from docker-scaffold template"
```

</details>

<details>
<summary><b>❌ GPG signing errors in commits</b></summary>

**Symptoms:**

```text
error: gpg failed to sign the data
```

**Solution:**

```bash
# Configure GPG
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Or disable signing
git config --global commit.gpgsign false
```

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

### Official Documentation

| Resource | Description | Link |
|----------|-------------|------|
| **Cookiecutter** | Template engine documentation | [cookiecutter.readthedocs.io](https://cookiecutter.readthedocs.io/) |
| **Docker** | Container platform docs | [docs.docker.com](https://docs.docker.com/) |
| **Docker Buildx** | Multi-platform builds | [docs.docker.com/buildx](https://docs.docker.com/buildx/working-with-buildx/) |
| **Task** | Task runner documentation | [taskfile.dev](https://taskfile.dev/) |
| **yq** | YAML processor | [mikefarah.gitbook.io/yq](https://mikefarah.gitbook.io/yq/) |

### docker-scaffold Resources

- 📦 **Repository**: [github.com/broadsage/docker-scaffold](https://github.com/broadsage/docker-scaffold)
- 📖 **Documentation**: [docs/](https://github.com/broadsage/docker-scaffold/tree/main/docs)
- 🐛 **Issues**: [github.com/broadsage/docker-scaffold/issues](https://github.com/broadsage/docker-scaffold/issues)
- 💬 **Discussions**: [github.com/broadsage/docker-scaffold/discussions](https://github.com/broadsage/docker-scaffold/discussions)
- 🔒 **Security**: [SECURITY.md](../SECURITY.md)
- 🤝 **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)

### Related Tools & Technologies

| Tool | Purpose | Link |
|------|---------|------|
| **MegaLinter** | Multi-language linting | [megalinter.io](https://megalinter.io/) |
| **Conform** | Commit message validation | [github.com/siderolabs/conform](https://github.com/siderolabs/conform) |
| **REUSE** | License compliance | [reuse.software](https://reuse.software/) |
| **GitHub Actions** | CI/CD automation | [docs.github.com/actions](https://docs.github.com/en/actions) |
| **Ansible** | Automation framework | [docs.ansible.com](https://docs.ansible.com/) |

### Learning Resources

- **Cookiecutter Tutorial**: [Creating your first template](https://cookiecutter.readthedocs.io/en/stable/tutorials.html)
- **Docker Best Practices**: [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- **Multi-arch Builds**: [Building multi-platform images](https://docs.docker.com/build/building/multi-platform/)
- **SPDX Licenses**: [SPDX License List](https://spdx.org/licenses/)

### Community & Support

#### Get Help

- 📧 **Email**: <opensource@broadsage.com>
- 💬 **Discussions**: Ask questions and share ideas
- 🐛 **Bug Reports**: [Report issues](https://github.com/broadsage/docker-scaffold/issues/new/choose)
- 💡 **Feature Requests**: [Suggest enhancements](https://github.com/broadsage/docker-scaffold/issues/new/choose)

#### Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for:

- Code of Conduct
- Development setup
- Pull request process
- Coding standards

#### Stay Updated

- ⭐ **Star the repo**: Get notifications about releases
- 👁️ **Watch releases**: [github.com/broadsage/docker-scaffold/releases](https://github.com/broadsage/docker-scaffold/releases)
- 📰 **Changelog**: [CHANGELOG.md](../CHANGELOG.md) (if available)

---

```bash
**Version**: 1.0.0  
**Last Updated**: December 2025  
**License**: Apache-2.0
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

## Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [docker-scaffold Repository](https://github.com/broadsage/docker-scaffold)
- [Task Documentation](https://taskfile.dev/)
- [Docker BuildX](https://docs.docker.com/buildx/working-with-buildx/)

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/broadsage/docker-scaffold/issues)
- **Discussions**: [GitHub Discussions](https://github.com/broadsage/docker-scaffold/discussions)
- **Email**: <opensource@broadsage.com>
