<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Conform Commit Policy Configuration Guide

## Overview

This repository uses [Conform](https://github.com/siderolabs/conform) to enforce consistent commit policies. Conform is a tool for enforcing policies on your build pipelines, with strong support for commit message validation.

## Configuration Files

### `.conform.yaml`

The main policy configuration file that defines all commit validation rules.

### `.pre-commit-config.yaml`

Integrates Conform with [pre-commit.com](https://pre-commit.com/) hooks to validate commits automatically.

## Commit Policy

All commits must comply with the following policies:

### 1. **Developer Certificate of Origin (DCO)**

- Required: **Yes**
- All commits must include a signed-off-by line: `Signed-off-by: Your Name <your.email@example.com>`
- Use `git commit -s` to automatically add this line

### 2. **GPG Signature**

- Required: **Yes**
- All commits must be signed with a GPG key
- Use `git commit -S` to sign commits
- Configure GPG signing: `git config user.signingkey <KEY_ID>`

### 3. **Commit Header (Subject Line)**

- **Length**: Must be 89 characters or less
- **Case**: Must be lowercase
- **Mood**: Must be imperative (e.g., "add feature" not "added feature")
- **Last Character**: Cannot end with a period (`.`)
- **Conventional Format**: Must follow Conventional Commits specification

### 4. **Conventional Commits Format**

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```bash
<type>(<scope>): <description>

<body>
```

#### Allowed Types

- `build` - Build system changes (dependencies, versions)
- `chore` - Maintenance tasks, version bumps
- `ci` - CI/CD configuration changes
- `deps` - Dependency updates
- `docs` - Documentation changes
- `feat` - New feature
- `fix` - Bug fix
- `perf` - Performance improvements
- `refactor` - Code refactoring
- `release` - Release commits
- `style` - Code style changes (formatting, semicolons)
- `test` - Test additions or modifications

### 5. **Commit Body**

- **Required**: Yes
- **Description Length**: Limited to 72 characters per line
- Should explain **why** the change was made, not what was changed
- The header explains what; the body explains why

### 6. **Spell Check**

- **Enabled**: Yes
- **Locale**: US English
- Helps maintain professional documentation

## Examples

### Valid Commit

```bash
feat(docker): add multi-architecture support to Dockerfile

Adds buildx configuration to support building Docker images
for multiple architectures including arm64 and amd64. This
enables users on different platforms to use the same image.

Signed-off-by: John Doe <john@example.com>
```

### Invalid Commits

❌ **Too long header** (over 89 chars)

```bash
feat: add new feature that adds support for multi architecture docker builds
```

❌ **Wrong case** (starts uppercase)

```bash
Feat(docker): Add feature
```

❌ **Wrong mood** (not imperative)

```bash
feat(docker): added multi-architecture support
```

❌ **Period at end**

```bash
feat(docker): add multi-architecture support.
```

❌ **Invalid type**

```bash
feature(docker): add something
```

❌ **Missing body**

```bash
feat(docker): add something
```

❌ **Invalid scope**

```bash
feat(random): add something
```

## Setup Instructions

### Prerequisites

- Git
- GPG key configured for signing
- pre-commit framework (optional but recommended)

### 1. Configure GPG Signing

```bash
# List your GPG keys
gpg --list-secret-keys --keyid-format LONG

# Configure Git to use your key
git config user.signingkey YOUR_KEY_ID

# Sign commits by default
git config commit.gpgsign true
```

### 2. Install Conform Locally

```bash
# Using Go
go install github.com/siderolabs/conform/cmd/conform@latest

# Or using Docker
docker run --rm -it -v $PWD:/src:ro,Z -w /src ghcr.io/siderolabs/conform:v0.1.0-alpha.26 enforce
```

### 3. Setup Git Hook (Optional)

```bash
# Create commit-msg hook
cat <<EOF > .git/hooks/commit-msg
#!/bin/sh
conform enforce --commit-msg-file \$1
EOF

chmod +x .git/hooks/commit-msg
```

### 4. Install Pre-commit (Recommended)

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install --hook-type commit-msg
```

## Running Conform

### Manual Validation

```bash
# Validate commits
conform enforce

# Validate with verbose output
conform enforce -v
```

### Automatic Validation

Once pre-commit hooks are installed, commits will be automatically validated during the commit process.

## Troubleshooting

### Commit Rejected for GPG Signature

- Ensure GPG key is configured: `git config user.signingkey <KEY_ID>`
- Check GPG is working: `echo "test" | gpg --sign`
- Verify the key is available: `gpg --list-secret-keys`

### Commit Rejected for DCO

- Add signed-off-by line: `git commit -s`
- Or add manually: `Signed-off-by: Your Name <your.email@example.com>`

### Commit Rejected for Format

- Check header is under 89 chars
- Use lowercase (except scope and after `(` in scope)
- Use imperative mood
- Don't end with period
- Ensure type is from allowed list
- Ensure scope is from allowed list
- Add a commit body with more details

### Spell Check Failures

- Review the flagged words
- Add correct spelling in commit message
- Commonly misspelled words in code context are normal

## Resources

- [Conform Documentation](https://github.com/siderolabs/conform)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Signing](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
- [Pre-commit Framework](https://pre-commit.com/)
- [DCO - Developer Certificate of Origin](https://developercertificate.org/)

## Questions or Issues?

If commits are being rejected unexpectedly, run Conform locally to see detailed error messages:

```bash
conform enforce -v
```

This will provide detailed feedback on which policies are failing and why.
