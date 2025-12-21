<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# docker-scaffold

> **Ansible-powered Cookiecutter template for professional Docker image repositories**

A production-ready template for generating Docker image projects with built-in compliance, security scanning, multi-architecture builds, and comprehensive CI/CD integration.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Cookiecutter](https://img.shields.io/badge/Cookiecutter-template-D4AA00?logo=cookiecutter&logoColor=fff)](https://github.com/cookiecutter/cookiecutter)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](CHANGELOG.md)

## 📦 Quick Start

```bash
# 1. Install Cookiecutter
pip install cookiecutter

# 2. Generate your project
cookiecutter gh:broadsage/docker-scaffold

# 3. Navigate to your new project
cd <your-project-name>

# 4. Generate all project files
task generate
```

## 🔄 Template Updates

Projects created from this template can easily stay up-to-date:

```bash
# Check your current version
task template:version

# Check for template updates
task template:check

# Update to latest version
task template:update
```

See [CHANGELOG.md](CHANGELOG.md) for version history and migration guides.
