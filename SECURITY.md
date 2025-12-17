<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Security Policy

## Overview

We take security seriously in the `docker-scaffold` project. This document outlines our security practices, vulnerability reporting procedures, and supported versions.

We are committed to:

- Responding promptly to security reports
- Following responsible disclosure practices
- Maintaining transparency with our community
- Providing timely security updates

---

## Supported Versions

We provide security updates for the following versions of docker-scaffold:

| Version | Support Status | End of Life |
|---------|----------------|-------------|
| Latest (main) | ✅ Active | Ongoing |
| 1.x | ✅ Active | TBD |

For optimal security, we recommend always using the latest stable release. Check the [Releases](https://github.com/broadsage/docker-scaffold/releases) page for version information.

---

## Reporting a Vulnerability

### ⚠️ IMPORTANT: Do NOT file public GitHub issues for security vulnerabilities

If you discover a security vulnerability in docker-scaffold, please report it responsibly through a private channel to minimize potential impact to users.

### Reporting Channels

Choose one of the following secure channels to report vulnerabilities:

1. **GitHub Security Advisory** (Recommended)
   - Use the [GitHub Security Advisory](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability) feature
   - Allows private communication with maintainers
   - Automatically creates a draft advisory

2. **Email**
   - Primary contact: [security@broadsage.com](mailto:security@broadsage.com)
   - Encrypted email is encouraged for sensitive reports
   - Include `[docker-scaffold]` in the subject line

3. **Direct Contact**
   - Contact individual maintainers via email (if publicly available)
   - Found in repository [maintainers section](https://github.com/broadsage/docker-scaffold#maintainers)

### What to Include in Your Report

Please provide as much detail as possible to help us understand and address the vulnerability:

- **Title**: Clear, descriptive vulnerability title
- **Your Information**: Name, affiliation/company (if applicable)
- **Project Version(s) Affected**: Specific version(s) with the vulnerability
- **Vulnerability Type**: e.g., RCE, Privilege Escalation, Data Disclosure, Supply Chain, etc.
- **Description**: Detailed explanation of the vulnerability
- **Reproduction Steps**: Clear steps to reproduce (POC, scripts, or configuration)
- **Docker Image Details**: Base image, runtime configuration, or Dockerfile patterns affected
- **Impact Assessment**: Potential impact on deployments and users
- **Attack Surface**: How the vulnerability could be exploited
- **Dependencies**: Any dependencies or external systems involved
- **Suggested Fix** (Optional): Proposed mitigation or fix if available
- **Supporting Materials**: Screenshots, logs, or additional documentation

### When to Report a Vulnerability

Report a vulnerability if:

- ✅ You discover a potential security vulnerability in docker-scaffold
- ✅ You suspect a vulnerability but are unsure if it impacts this project
- ✅ You discover a vulnerability in a dependency used by docker-scaffold
- ✅ You find security issues in generated Docker images from this template

**Do NOT report through this channel:**

- ❌ Non-security bugs or issues (use [GitHub Issues](https://github.com/broadsage/docker-scaffold/issues) instead)
- ❌ Requests for help with configuration or usage

---

## Vulnerability Severity Classification

We use CVSS v3.1 for scoring to determine response priority:

| Severity | CVSS Score | Impact | Response Time |
|----------|-----------|--------|----------------|
| **Critical** | 9.0 - 10.0 | Immediate security risk, potential RCE | 24-48 hours |
| **High** | 7.0 - 8.9 | Significant security risk | 3-7 days |
| **Medium** | 4.0 - 6.9 | Moderate security concern | 7-30 days |
| **Low** | 0.1 - 3.9 | Minor security issue | 30-90 days |

---

## Response & Resolution Timeline

We are committed to timely responses following this coordinated 90-day disclosure process:

| Stage | Timeline | Details |
|-------|----------|---------|
| Initial Acknowledgment | Within 48 hours | Receipt confirmation |
| Initial Assessment | Within 3-5 business days | Severity determination |
| Triage & Validation | Days 0-7 | Reproducibility verification |
| Investigation | Days 7-30 | Impact assessment & fix development |
| Testing | Days 30-60 | Multi-architecture builds, QA |
| Final Preparation | Days 60-90 | Public release readiness |
| Public Disclosure | Day 90+ | Security advisory publication |
| Regular Updates | Every 5 business days | Progress notifications (if ongoing) |

### Response Process

1. **Triage & Validation**
   - Our security team investigates the report
   - Determines severity using CVSS v3.1 scoring
   - Validates reproducibility

2. **Investigation**
   - Assess impact on docker-scaffold and generated images
   - Identify affected components and versions
   - Develop mitigation strategies

3. **Fix Development**
   - Create fix in private branch
   - Test thoroughly including multi-architecture builds
   - Backport to supported versions if applicable

4. **Disclosure & Communication**
   - Prepare security advisory with CVSS score
   - Coordinate disclosure timing with reporter
   - Publish advisory and release patched version
   - Announce via release notes and social channels
   - Provide credit to reporter (unless anonymous requested)

### Expedited Response

Critical vulnerabilities with active exploitation may be expedited:

- Security patches may be released immediately for critical issues
- Coordination continues with reporter throughout the process
- Public disclosure may occur before the 90-day window if actively exploited

---

## Security Best Practices

### For Generated Docker Images

Docker-scaffold generates containerized projects. We recommend the following practices for maximum security:

### Base Image Security

- Always use up-to-date base images
- Regularly rebuild images to apply security patches
- Subscribe to security advisories for base images
- Consider using minimal base images (Alpine, Distroless)
- Verify image signatures using Docker content trust

### Supply Chain Security

- Use container image scanning tools (Snyk, Trivy, Grype)
- Sign images with tools like Cosign
- Verify image signatures before deployment
- Use private registries for internal images
- Use lock files for reproducible builds
- Regularly scan dependencies for vulnerabilities
- Monitor for CVEs in your dependencies

### Runtime Security

- Run containers as non-root users
- Use read-only root filesystems where possible
- Implement resource limits and security policies
- Enable container runtime security policies
- Follow [Dockerfile best practices](https://docs.docker.com/develop/dev-best-practices/)
- Use `.dockerignore` to exclude sensitive files
- Implement proper secrets management

### Access & Maintenance

- Keep images updated with latest patches
- Apply security patches promptly
- Monitor security advisories regularly
- Manage repository access carefully
- Use GitHub branch protection rules
- Require code reviews for changes
- Review generated Ansible configurations

### Supported Platforms

Security updates will be provided for all architectures:

- Linux/x86_64 (amd64)
- Linux/ARM64 (arm64v8)
- Linux/ARM (armv7)

---

## Contact Information

### Security Issues

📧 **Email**: [security@broadsage.com](mailto:security@broadsage.com)  
🔐 **GitHub Security Advisory**: Use the [private reporting feature](https://github.com/broadsage/docker-scaffold/security/advisories)  
👥 **Maintainers**: See [repository maintainers](https://github.com/broadsage/docker-scaffold#maintainers)

### General Inquiries

For non-security questions:

- 📋 **Issues**: [GitHub Issues](https://github.com/broadsage/docker-scaffold/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/broadsage/docker-scaffold/discussions)
- 🌐 **Website**: [broadsage.com](https://broadsage.com)

---

## Security Advisory Archive

We maintain a public archive of security advisories and responses in accordance with OpenSSF best practices:

- **Location**: [GitHub Security Advisories](https://github.com/broadsage/docker-scaffold/security/advisories)
- **Details**: Date, description, investigation steps, resolution, and remediation
- **Transparency**: No sensitive or private information is included

---

## Compliance & Standards

Docker-scaffold follows:

- **OpenSSF Best Practices**: [Best Practices Badge](https://bestpractices.coreinfrastructure.org/)
- **Secure Software Development Framework (SSDF)**: Practice P3.1 on vulnerability management
- **OWASP Guidelines**: Container security recommendations
- **NIST Cybersecurity Framework**: Risk management principles
- **REUSE Compliance**: License compliance and attribution

---

## Bug Bounty Program

Currently, `Broadsage` does not operate a formal bug bounty program. However, we deeply appreciate security researchers who responsibly disclose vulnerabilities. We may offer recognition, swag, or other forms of gratitude at our discretion.

---

## Acknowledgments

We thank the security researchers and community members who help improve docker-scaffold's security through responsible disclosure. Their contributions make our open-source docker image safer for everyone.

---

## Additional Resources

- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) - Community code of conduct
- [LICENSE](./LICENSE) - Project license
- [REUSE.toml](./REUSE.toml) - License compliance configuration
- [OpenSSF Security Best Practices](https://best.openssf.org/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

---

**Last Updated**: December 2025  
**Policy Version**: 1.0
