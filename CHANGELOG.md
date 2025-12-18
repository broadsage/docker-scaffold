<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Changelog

All notable changes to this template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-12-18

### Added

- Initial release of docker-scaffold template
- Cookiecutter-based project generation
- Ansible-powered file generation via Docker container
- Version tracking system for template updates
- Template update workflow with `task check-updates` and `task update-template`
- Protected files mechanism to prevent overwriting customizations
- Multi-architecture Docker build support (AMD64, ARM64)
- GitHub Actions workflows and templates
- Security scanning and compliance tools (REUSE, MegaLinter)
- Automated backup system for safe template updates
- Comprehensive documentation for template usage

### Features

- **GitHub Integration**: Issue templates, PR templates, and discussion templates
- **Security**: Automated vulnerability scanning
- **Compliance**: REUSE license compliance and commit validation
- **Registry**: Multi-registry push support
- **Documentation**: Auto-generated project documentation

### Developer Experience

- Task-based workflow with `Taskfile.yml`
- Python virtual environment management
- Docker-based build and test environment
- CI/CD pipeline templates

---

## Version Update Guide

When updating to a new template version:

1. Check current version: `task version`
2. Check for updates: `task check-updates`
3. Review changelog (this file)
4. Create backup: `task backup`
5. Update template: `task update-template`
6. Review changes: `git diff`
7. Test the changes: `task compliance && task test`
8. Commit updates: `git commit -am "chore: update template to vX.Y.Z"`

---

## Breaking Changes Policy

- **Major version (X.0.0)**: Breaking changes that require manual migration
- **Minor version (0.Y.0)**: New features, backward compatible
- **Patch version (0.0.Z)**: Bug fixes, backward compatible

[Unreleased]: https://github.com/broadsage/docker-scaffold/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/broadsage/docker-scaffold/releases/tag/v1.0.0
