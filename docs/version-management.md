<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Template Version Management

This document explains how to manage and update template versions in your docker-scaffold projects.

## Overview

Docker-scaffold uses a **version-controlled template system** that allows downstream projects to:

- Track which template version they were created from
- Check for template updates
- Safely update to newer template versions
- Maintain customizations during updates

## Version Tracking

Each project tracks its template version in `project.yaml`:

```yaml
template:
  version: "1.0.0"  # Current template version
  source: "https://github.com/broadsage/docker-scaffold"
  protected_files: []  # Files that won't be overwritten during updates
```

## Available Commands

### Check Current Version

```bash
task template:version
```

Shows the template version your project is currently using.

### Check for Updates

```bash
task template:check
```

Compares your current version with the latest available template version.

### Update Template

```bash
task template:update
```

Updates your project to the latest template version:

1. Creates a backup of your current project
2. Pulls the latest template Docker image
3. Updates `project.yaml` with new version
4. Regenerates project files
5. Preserves files listed in `protected_files`

## Protecting Custom Files

To prevent specific files from being overwritten during updates, add them to `protected_files` in `project.yaml`:

```yaml
template:
  protected_files:
    - README.md              # Custom documentation
    - scripts/custom.sh      # Custom scripts
    - .github/workflows/custom.yml  # Custom workflows
```

## Update Workflow

### Manual Update

```bash
# 1. Check for updates
task check-updates

# 2. Review changelog
curl -sL https://raw.githubusercontent.com/broadsage/docker-scaffold/main/CHANGELOG.md | less

# 3. Create a feature branch
git checkout -b update-template

# 4. Update template
task update-template

# 5. Review changes
git diff

# 6. Test changes
task compliance
task test

# 7. Commit and push
git add .
git commit -m "chore: update template to v1.1.0"
git push origin update-template
```

### Automated Update (GitHub Actions)

Add this workflow to automatically check for template updates:

```yaml
# .github/workflows/template-sync.yml
name: Template Update Check

on:
  schedule:
    - cron: '0 9 * * MON'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Task
        uses: arduino/setup-task@v1
      
      - name: Check for updates
        run: task template:check
```

## Version Pinning

You can pin to a specific version instead of using `latest`:

```yaml
template:
  version: "1.2.3"  # Pin to specific version
```

Then in `Taskfile.yml`, the `generate` task will use this version:

```bash
task generate  # Uses version from project.yaml
```

## Rollback

To rollback to a previous template version:

```bash
# 1. Update version in project.yaml
yq -i '.template.version = "1.0.0"' project.yaml

# 2. Regenerate with old version
task generate

# 3. Verify changes
git diff
```

## Best Practices

1. **Check Changelog**: Always review the changelog before updating
2. **Test Updates**: Run compliance checks and tests after updating
3. **Use Feature Branches**: Never update directly on main branch
4. **Protected Files**: Add custom files to `protected_files` list
5. **Regular Updates**: Check for updates monthly or quarterly
6. **Semantic Versioning**: Understand version numbers:
   - `1.0.0` → `1.0.1`: Bug fixes (safe to update)
   - `1.0.0` → `1.1.0`: New features (review changes)
   - `1.0.0` → `2.0.0`: Breaking changes (read migration guide)

## Troubleshooting

### Version Mismatch

If version doesn't match after update:

```bash
# Manually set version
yq -i '.template.version = "1.1.0"' project.yaml

# Verify
task version
```

### Cannot Pull Docker Image

Check Docker registry access:

```bash
# Pull manually
docker pull ghcr.io/broadsage/scaffold:latest

# Check authentication if needed
docker login ghcr.io
```

## Version History

See [CHANGELOG.md](CHANGELOG.md) for complete version history and migration guides.

## Getting Help

- Check [template documentation](https://github.com/broadsage/docker-scaffold)
- Open an [issue](https://github.com/broadsage/docker-scaffold/issues)
- Review [changelog](CHANGELOG.md) for known issues
