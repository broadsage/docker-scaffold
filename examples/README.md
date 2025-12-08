<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Configuration Examples

This directory contains example configurations for different use cases.

## Quick Start

1. **Copy an example** that matches your needs:

   ```bash
   cp examples/minimal-image.yml my-image.yml
   ```

2. **Customize** the image name and description:

   ```yaml
   image:
     name: my-awesome-app
     description: My awesome Docker application
   ```

3. **Generate** the scaffold:

   ```bash
   docker run --rm \
     -v $(pwd)/my-image.yml:/tmp/project.yml \
     -v $(pwd)/defaults.yml:/tmp/defaults.yml \
     -v $(pwd)/output:/tmp \
     ghcr.io/broadsage/scaffold
   ```

## Examples Overview

| Example | Use Case | Features Enabled |
|---------|----------|------------------|
| `minimal-image.yml` | Quick setup, inherits all defaults | Workflows only |
| `production-image.yml` | Production-ready with security | All security features |
| `single-arch-image.yml` | Platform-specific builds | ARM64 only |

## Configuration Hierarchy

```text
defaults.yml (organization defaults)
    ↓
project.yml (image-specific overrides)
    ↓
ansible/vars/common.yml (variable mapping)
    ↓
Ansible roles (generation)
```

## Common Patterns

### Minimal Configuration (90% of images)

```yaml
image:
  name: simple-app
  description: A simple application
```

### Enable Security Scanning

```yaml
image:
  name: secure-app
  description: Security-scanned application

features:
  security_scan: true
```

### Multi-Registry Push

```yaml
image:
  name: popular-app
  description: App published to multiple registries

features:
  dockerhub_push: true
```

### Override Build Platforms

```yaml
image:
  name: x86-only-app
  description: x86-64 only application

build:
  platforms:
    - linux/amd64
```

## Tips for Managing 100+ Images

1. **Keep defaults.yml stable** - rarely modify it
2. **Use minimal project.yml** - only specify differences
3. **Organize by category**:

   ```text
   images/
   ├── web-apps/
   │   ├── nginx.yml
   │   └── apache.yml
   ├── databases/
   │   ├── postgres.yml
   │   └── mysql.yml
   └── utilities/
       ├── backup.yml
       └── monitor.yml
   ```

4. **Automate generation** with CI/CD
5. **Version control** all .yml files
6. **Use consistent naming** (kebab-case recommended)

## Advanced Configuration

See the main `project.yml` for all available options and inline documentation.
