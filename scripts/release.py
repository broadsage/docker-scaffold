#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Release manager - handles version checking, comparison, and updates.

This script manages versioning for multiple components:
- Template versions (docker-scaffold)
- Software package versions (nginx, alpine, etc.) - coming soon

Supports checking for updates and updating versions while preserving configuration.
"""

import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from ruamel.yaml import YAML
except ImportError:
    print("Error: ruamel.yaml is not installed", file=sys.stderr)
    print("Install it with: pip install ruamel.yaml", file=sys.stderr)
    sys.exit(1)


class ReleaseManager(ABC):
    """Abstract base class for release managers."""

    @abstractmethod
    def get_current_version(self) -> str:
        """Get the currently installed/configured version."""
        pass

    @abstractmethod
    def get_latest_version(self) -> str:
        """Get the latest available version."""
        pass

    def check_update(self) -> Dict[str, Any]:
        """
        Compare current and latest versions.

        Returns:
            Dict with current, latest, and update_available status
        """
        current = self.get_current_version()
        latest = self.get_latest_version()

        update_available = (
            current != latest and current != "latest" and latest != "latest"
        )

        return {
            "current": current,
            "latest": latest,
            "update_available": update_available,
        }

    @abstractmethod
    def update_version(self, version: Optional[str] = None) -> None:
        """
        Update to specified version or latest.

        Args:
            version: Version to set, or None to use latest
        """
        pass


class TemplateReleaseManager(ReleaseManager):
    """Manages docker-scaffold template version operations."""

    def __init__(
        self,
        project_file: str = "project.yaml",
        docker_image: str = "ghcr.io/broadsage/scaffold",
    ):
        """
        Initialize the template version manager.

        Args:
            project_file: Path to project.yaml
            docker_image: Docker image name
        """
        self.project_file = Path(project_file)
        self.docker_image = docker_image
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.default_flow_style = False
        self.yaml.width = 4096
        self.yaml.indent(mapping=2, sequence=2, offset=0)  # type: ignore[attr-defined]

    def get_current_version(self) -> str:
        """
        Read current template version from project.yaml.

        Returns:
            Current version string or "unknown" if not found
        """
        if not self.project_file.exists():
            return "unknown"

        try:
            data: Any = self.yaml.load(self.project_file)  # type: ignore[assignment]
            if "template" in data and "version" in data["template"]:
                return str(data["template"]["version"])  # type: ignore[arg-type]
            return "unknown"
        except Exception:
            return "unknown"

    def get_latest_version(self) -> str:
        """
        Fetch latest template version from Docker image.

        Returns:
            Latest version string or "latest" if cannot determine
        """
        try:
            # Pull latest image quietly
            subprocess.run(
                ["docker", "pull", f"{self.docker_image}:latest"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )

            # Read VERSION file from image
            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    f"{self.docker_image}:latest",
                    "cat",
                    "/app/VERSION",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()

            return "latest"
        except Exception:
            return "latest"

    def update_version(self, version: Optional[str] = None) -> None:
        """
        Update template version in project.yaml.

        Args:
            version: Version to set, or None to use latest
        """
        if version is None:
            version = self.get_latest_version()

        if not self.project_file.exists():
            print(f"Error: File '{self.project_file}' not found", file=sys.stderr)
            sys.exit(1)

        try:
            data: Any = self.yaml.load(self.project_file)  # type: ignore[assignment]

            if "template" not in data or "version" not in data["template"]:
                print("Error: template.version not found in YAML", file=sys.stderr)
                sys.exit(1)

            data["template"]["version"] = version
            self.yaml.dump(data, self.project_file)  # type: ignore[arg-type]
            print(f"✓ Updated template version to {version}")
        except Exception as e:
            print(f"Error updating version: {e}", file=sys.stderr)
            sys.exit(1)


class ReleaseManagerFactory:
    """Factory for creating appropriate release managers."""

    @staticmethod
    def create(component: str = "template") -> ReleaseManager:
        """
        Create a release manager for the specified component.

        Args:
            component: Component type (template, nginx, alpine, etc.)

        Returns:
            Appropriate ReleaseManager instance

        Raises:
            ValueError: If component type is not supported
        """
        if component == "template":
            return TemplateReleaseManager()
        else:
            raise ValueError(
                f"Unsupported component: {component}. "
                f"Supported components: template"
            )


def print_usage() -> None:
    """Print usage information."""
    print("Usage: release.py <component> <command> [args]", file=sys.stderr)
    print("", file=sys.stderr)
    print("Components:", file=sys.stderr)
    print("  template             Docker-scaffold template", file=sys.stderr)
    print("", file=sys.stderr)
    print("Commands:", file=sys.stderr)
    print("  current              Show current version", file=sys.stderr)
    print("  latest               Show latest available version", file=sys.stderr)
    print("  check                Compare current vs latest (exit 1 if update available)", file=sys.stderr)
    print("  update [version]     Update to version (or latest if not specified)", file=sys.stderr)
    print("", file=sys.stderr)
    print("Examples:", file=sys.stderr)
    print("  release.py template check", file=sys.stderr)
    print("  release.py template update", file=sys.stderr)
    print("  release.py template update 1.2.0", file=sys.stderr)


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    component = sys.argv[1]
    command = sys.argv[2]
    command_args = sys.argv[3:] if len(sys.argv) > 3 else []

    # Create appropriate manager
    try:
        manager = ReleaseManagerFactory.create(component)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print_usage()
        sys.exit(1)

    # Execute command
    if command == "current":
        print(manager.get_current_version())

    elif command == "latest":
        print(manager.get_latest_version())

    elif command == "check":
        result = manager.check_update()
        print(f"Current {component} version: {result['current']}")
        print(f"Latest {component} version:  {result['latest']}")

        if result["update_available"]:
            print("")
            print("⚠️  Updates available! Run 'task template:update' to upgrade")
            sys.exit(1)
        else:
            print("")
            print(f"✓ {component.capitalize()} is up to date")
            sys.exit(0)

    elif command == "update":
        version = command_args[0] if command_args else None
        manager.update_version(version)

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
