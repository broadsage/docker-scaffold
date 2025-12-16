#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

"""Post-generation hook for cookiecutter template.

This hook runs AFTER project.yaml and Taskfile.yml are generated.
Handles license file selection and displays progress events for completing
project setup.
"""

import sys
from datetime import datetime
from pathlib import Path
import os


def get_timestamp() -> str:
    """Get current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")


def print_event(emoji: str, message: str) -> None:
    """Print formatted event message with timestamp."""
    timestamp = get_timestamp()
    print(f"{emoji} {message} • {timestamp}")


def handle_license_file() -> None:
    """Handle license file selection and setup.

    Reads selected license template from templates/licenses/ and creates LICENSE file.
    Supports Jinja2 variable substitution for year and maintainer name.
    """
    selected_license: str = "{{ cookiecutter.license }}"

    if selected_license == "Not Open Source":  # type: ignore[comparison-overlap]
        print_event("📋", "No open source license selected")
        return

    # Get the template directory - Cookiecutter sets COOKIECUTTER_TEMPLATE_FOLDER env var
    template_folder: str = os.environ.get(
        "COOKIECUTTER_TEMPLATE_FOLDER", str(Path(__file__).parent.parent)
    )
    license_template: Path = (
        Path(template_folder) / "templates" / "licenses" / selected_license
    )
    license_dest: Path = Path("LICENSE")

    # Debug: print paths for troubleshooting
    print_event(
        "🔍",
        f"Looking for license in: {license_template}",
    )

    if not license_template.exists():
        print_event("⚠️ ", f"License template not found: {selected_license}")
        print_event("💡", f"Expected path: {license_template}")
        return

    try:
        # Read template content and write to LICENSE
        content: str = license_template.read_text(encoding="utf-8")
        license_dest.write_text(content, encoding="utf-8")
        print_event("📜", f"License file created: {selected_license}")
    except Exception as e:
        print_event("❌", f"Error creating license file: {e}")


def display_next_steps() -> None:
    """Display instructions for completing project setup."""
    project_slug = "{{ cookiecutter.project_slug }}"

    print()
    print_event("✅", f"Project '{project_slug}' initialized successfully")
    print_event(
        "📦", "Generated: project.yaml, Taskfile.yml, README.md, .gitignore, LICENSE"
    )
    print_event("📝", f"Configuration: {project_slug}/project.yaml")
    print()
    print_event("🚀", "Next Steps:")
    print()
    print(f"  1. cd {project_slug}")
    print("  2. task generate           # Generate full project with Docker")
    print("  3. task build              # Build Docker image")
    print("  4. task compliance         # Run code quality checks")
    print()
    print_event("💡", "Customize: Edit project.yaml and run 'task generate' again")
    print_event("❓", "Help: https://github.com/broadsage/docker-scaffold/discussions")
    print_event(
        "📚", "Docs: https://github.com/broadsage/docker-scaffold/blob/main/README.md"
    )
    print()


def main() -> None:
    """Run post-generation tasks."""
    try:
        handle_license_file()
        display_next_steps()
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        print("   Project was created but post-generation setup failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
