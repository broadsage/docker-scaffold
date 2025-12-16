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
from typing import Final

# ANSI Color Codes
GREEN: Final[str] = "\033[32m"
CYAN: Final[str] = "\033[36m"
YELLOW: Final[str] = "\033[33m"
BLUE: Final[str] = "\033[34m"
BOLD: Final[str] = "\033[1m"
NC: Final[str] = "\033[0m"  # No Color


def get_timestamp() -> str:
    """Get current date and time in DD-Mmm-YYYY HH:MM:SS format."""
    return datetime.now().strftime("%d-%b-%Y %H:%M:%S")


def print_event(emoji: str, message: str, color: str = "") -> None:
    """Print formatted event message with timestamp and optional color.
    
    Args:
        emoji: The emoji to display
        message: The message text
        color: ANSI color code (optional)
    """
    timestamp = get_timestamp()
    colored_msg = f"{color}{message}{NC}" if color else message
    print(f"{emoji} {colored_msg} • {timestamp}")


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
        print_event("📜", f"License file created: {YELLOW}{selected_license}{NC}", YELLOW)
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
    print_event("✅", f"Project {GREEN}{project_slug}{NC} initialized successfully", GREEN)
    print_event(
        "📦",
        f"Generated: {CYAN}project.yaml, Taskfile.yml, README.md, .gitignore, LICENSE{NC}",
        CYAN,
    )
    print_event("📝", f"Configuration: {BLUE}{project_slug}/project.yaml{NC}", BLUE)
    print()
    print_event("🚀", f"{BOLD}{CYAN}Next Steps:{NC}", CYAN)
    print()
    print(f"  1. cd {CYAN}{project_slug}{NC}")
    print(f"  2. {CYAN}task generate{NC}           # Generate full project with Docker")
    print(f"  3. {CYAN}task setup{NC}              # Setup development environment")
    print(f"  4. {CYAN}task compliance{NC}         # Run code quality checks")
    print()
    print_event("💡", f"Customize: Edit project.yaml and run {CYAN}task generate{NC} again", YELLOW)
    print_event(
        "❓",
        f"Help: {BLUE}https://github.com/broadsage/docker-scaffold/discussions{NC}",
        BLUE,
    )
    print_event(
        "📚",
        f"Docs: {BLUE}https://github.com/broadsage/docker-scaffold/blob/main/README.md{NC}",
        BLUE,
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
