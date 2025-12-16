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


def get_timestamp() -> str:
    """Get current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")


def print_event(emoji: str, message: str) -> None:
    """Print formatted event message with timestamp."""
    timestamp = get_timestamp()
    print(f"{emoji} {message} • {timestamp}")


def handle_license_file() -> None:
    """Handle license file selection and setup.
    
    Copies the selected license template file to LICENSE if not "Not Open Source".
    Removes all other license template files after selection.
    """
    selected_license: str = "{{ cookiecutter.license }}"
    
    if selected_license == "Not Open Source":  # type: ignore[comparison-overlap]
        # Remove all license templates for closed source projects
        for license_file in Path(".").glob("LICENSE.*"):
            license_file.unlink()
        print_event("📋", "No open source license selected")
        return
    
    # Copy selected license template to LICENSE
    license_source: Path = Path(f"LICENSE.{selected_license}")
    license_dest: Path = Path("LICENSE")
    
    if license_source.exists():
        license_dest.write_text(license_source.read_text(encoding="utf-8"), encoding="utf-8")
        print_event("📜", f"License file created: {selected_license}")
    else:
        print_event("⚠️ ", f"License template not found: LICENSE.{selected_license}")
        return
    
    # Remove all license template files
    for license_file in Path(".").glob("LICENSE.*"):
        license_file.unlink()


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
