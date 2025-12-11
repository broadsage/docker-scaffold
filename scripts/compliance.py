#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Code Quality & Compliance Check Script

Description:
  Automated compliance checking framework for code quality assurance.
  Runs multiple checks: linting, licensing, commit validation, and configuration.

Requirements:
  - Docker installed and running
  - Network access for container images
  - Git repository for commit checks
  - Python 3.7+
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple


class CheckStatus(Enum):
    """Enum for check status."""

    PASS = "✓ PASS"
    FAIL = "✗ FAIL"
    SKIP = "⊘ SKIP"


@dataclass
class CheckResult:
    """Data class for individual check results."""

    name: str
    status: CheckStatus
    message: str = ""


@dataclass
class ComplianceConfig:
    """Configuration for compliance checks."""

    project_root: Path
    container_engine: str = "docker"
    compare_branch: str = "main"
    debug: bool = False


class Logger:
    """Beautiful console output formatter following industry standards."""

    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    WHITE = "\033[37m"

    # Shared constants for DRY code
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def _get_timestamp() -> str:
        """Get formatted timestamp (DRY)."""
        return datetime.now().strftime(Logger.TIME_FORMAT)

    @staticmethod
    def supports_color() -> bool:
        """Check if terminal supports color."""
        return sys.stdout.isatty() and sys.stderr.isatty()

    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Apply color to text if supported."""
        if Logger.supports_color():
            return f"{color}{text}{Logger.RESET}"
        return text

    @staticmethod
    def banner(text: str) -> None:
        """Print main banner with timestamp."""
        colored_text = Logger.colorize(text, Logger.BOLD + Logger.CYAN)
        colored_time = Logger.colorize(
            Logger._get_timestamp(), Logger.DIM + Logger.CYAN
        )
        print(f"\n➜  {colored_text} [{colored_time}]\n")

    @staticmethod
    def header(text: str) -> None:
        """Print section header with timestamp."""
        colored_text = Logger.colorize(text, Logger.BOLD + Logger.BLUE)
        colored_time = Logger.colorize(
            Logger._get_timestamp(), Logger.DIM + Logger.BLUE
        )
        print(f"  {colored_text} [{colored_time}]")

    @staticmethod
    def info(text: str) -> None:
        """Print info message."""
        icon = Logger.colorize("•", Logger.BLUE)
        print(f"{icon} {text}")

    @staticmethod
    def ok(text: str) -> None:
        """Print success message."""
        icon = Logger.colorize("✓", Logger.GREEN)
        msg = Logger.colorize(text, Logger.GREEN)
        print(f"{icon} {msg}")

    @staticmethod
    def error(text: str) -> None:
        """Print error message to stderr."""
        icon = Logger.colorize("✗", Logger.RED)
        msg = Logger.colorize(text, Logger.RED)
        print(f"{icon} {msg}", file=sys.stderr)

    @staticmethod
    def debug(text: str, debug_mode: bool = False) -> None:
        """Print debug message if debug mode enabled."""
        if debug_mode:
            icon = Logger.colorize("⚙", Logger.MAGENTA)
            msg = Logger.colorize(text, Logger.DIM)
            print(f"{icon} {msg}")


class DockerCommand:
    """Wrapper for Docker command execution."""

    def __init__(self, engine: str = "docker"):
        """Initialize Docker command wrapper."""
        self.engine = engine
        self._verify_engine()

    def _verify_engine(self) -> None:
        """Verify Docker/container engine is available."""
        try:
            subprocess.run(
                [self.engine, "--version"], capture_output=True, check=True, timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            Logger.error(f"{self.engine} not found")
            Logger.error("Please install Docker: https://docs.docker.com/get-docker/")
            sys.exit(2)

    def run(
        self, image: str, *args: str, stdin_data: str | None = None, **kwargs: str
    ) -> Tuple[int, str]:
        """
        Run a Docker container.

        Args:
            image: Container image name
            *args: Additional arguments
            stdin_data: Optional data to pass to stdin
            **kwargs: Volume mappings (volume_name -> container_path)

        Returns:
            Tuple of (exit_code, output)
        """
        cmd: List[str] = [self.engine, "run", "--rm"]

        # Add stdin flag if data provided
        if stdin_data:
            cmd.append("-i")

        # Add volume mappings
        for host_path, container_path in kwargs.items():
            cmd.extend(["-v", f"{host_path}:{container_path}"])

        cmd.append(image)
        cmd.extend(list(args))

        try:
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True,
                input=stdin_data,
                check=False,
            )
            return result.returncode, ""
        except Exception as e:
            Logger.error(f"Docker execution failed: {e}")
            return 1, str(e)


class ComplianceChecker:
    """Main compliance checker orchestrator."""

    def __init__(self, config: ComplianceConfig):
        """Initialize compliance checker."""
        self.config = config
        self.docker = DockerCommand(config.container_engine)
        self.results: List[CheckResult] = []

    def _create_result(
        self,
        name: str,
        exit_code: int,
        pass_msg: str = "Check passed",
        fail_msg: str = "Check failed, see logs above",
    ) -> CheckResult:
        """Create a check result from exit code."""
        if exit_code == 0:
            return CheckResult(name, CheckStatus.PASS, pass_msg)
        return CheckResult(name, CheckStatus.FAIL, fail_msg)

    def _run_docker_check(
        self, name: str, image: str, *args: str, **kwargs: str
    ) -> CheckResult:
        """Run a Docker-based check and return result."""
        exit_code, _ = self.docker.run(image, *args, **kwargs)
        return self._create_result(name, exit_code)

    def check_lint(self) -> CheckResult:
        """Run MegaLinter check using official Docker image with python flavor."""
        Logger.header("LINTER HEALTH (MEGALINTER - python flavor)")
        # Prepare Docker volumes with Docker socket support
        volumes = {str(self.config.project_root): "/tmp/lint"}
        # Add Docker socket for Docker-in-Docker support
        volumes["/var/run/docker.sock"] = "/var/run/docker.sock:rw"

        return self._run_docker_check(
            "Lint", "oxsecurity/megalinter-python:v9", "-e", "LOG_LEVEL=INFO", **volumes
        )

    def check_publiccode(self) -> CheckResult:
        """Validate publiccode.yaml using publiccode-parser-go."""
        Logger.header("LINTER publiccode.yaml (publiccode-parser-go)")

        publiccode_path = self.config.project_root / "publiccode.yaml"

        if not publiccode_path.exists():
            return CheckResult(
                "publiccode.yaml", CheckStatus.SKIP, "publiccode.yaml not found"
            )

        try:
            with open(publiccode_path, "r", encoding="utf-8") as f:
                file_content = f.read()

            exit_code, _ = self.docker.run(
                "italia/publiccode-parser-go",
                "-no-network",
                "/dev/stdin",
                stdin_data=file_content,
            )

            return self._create_result(
                "publiccode.yaml",
                exit_code,
                "Validation passed",
                "Validation failed, see logs above",
            )

        except Exception as e:
            return CheckResult("publiccode.yaml", CheckStatus.FAIL, f"Error: {e}")

    def check_license(self) -> CheckResult:
        """Run REUSE license compliance check with automatic download."""
        Logger.header("LICENSE HEALTH (REUSE)")

        # Step 1: Download missing licenses (best effort, non-blocking)
        Logger.info("Downloading missing licenses from SPDX registry...")
        download_exit, _ = self.docker.run(
            "docker.io/fsfe/reuse:latest",
            "download",
            "--all",
            **{str(self.config.project_root): "/data"},
        )

        if download_exit == 0:
            Logger.ok("Licenses downloaded successfully")
        else:
            Logger.info(
                "License download completed with warnings (proceeding with lint)"
            )

        # Step 2: Run lint check
        Logger.info("Running license compliance lint check...")
        lint_exit, _ = self.docker.run(
            "docker.io/fsfe/reuse:latest",
            "lint",
            **{str(self.config.project_root): "/data"},
        )

        # Return based on lint result (download is preparation)
        return self._create_result(
            "License",
            lint_exit,
            "License compliance check passed",
            "License check failed, see logs above",
        )

    def check_commit(self) -> CheckResult:
        """Validate commit messages with Conform."""
        Logger.header("COMMIT HEALTH (CONFORM)")

        try:
            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.config.project_root,
                capture_output=True,
                text=True,
                check=False,
            )
            current_branch = result.stdout.strip()

            # Count commits
            result = subprocess.run(
                ["git", "rev-list", "--count", f"{self.config.compare_branch}.."],
                cwd=self.config.project_root,
                capture_output=True,
                text=True,
                check=False,
            )
            commit_count = int(result.stdout.strip()) if result.returncode == 0 else 0

            if commit_count == 0:
                Logger.info(
                    f"No commits found in {current_branch}, "
                    f"compared to {self.config.compare_branch}"
                )
                return CheckResult(
                    "Commit", CheckStatus.SKIP, "No new commits to validate"
                )

            # Run Conform check
            return self._run_docker_check(
                "Commit",
                "ghcr.io/siderolabs/conform:latest",
                "enforce",
                f"--base-branch={self.config.compare_branch}",
                **{str(self.config.project_root): "/repo"},
            )

        except Exception as e:
            return CheckResult("Commit", CheckStatus.FAIL, f"Error: {e}")

    def run_all(self) -> List[CheckResult]:
        """Run all checks."""
        checks = [
            self.check_lint,
            self.check_publiccode,
            self.check_license,
            self.check_commit,
        ]

        results: List[CheckResult] = []
        for check_func in checks:
            result = check_func()
            self.results.append(result)
            results.append(result)

        return results

    def _get_status_color(self, status: CheckStatus) -> str:
        """Get ANSI color code for a check status (DRY)."""
        color_map = {
            CheckStatus.PASS: Logger.GREEN,
            CheckStatus.FAIL: Logger.RED,
            CheckStatus.SKIP: Logger.YELLOW,
        }
        return color_map.get(status, Logger.WHITE)

    def _build_table_borders(self) -> Dict[str, str]:
        """Build colored unicode box-drawing border characters (DRY)."""
        return {
            "h": Logger.colorize("─", Logger.CYAN),
            "v": Logger.colorize("│", Logger.CYAN),
            "tl": Logger.colorize("┌", Logger.CYAN),
            "tr": Logger.colorize("┐", Logger.CYAN),
            "bl": Logger.colorize("└", Logger.CYAN),
            "br": Logger.colorize("┘", Logger.CYAN),
            "t": Logger.colorize("┬", Logger.CYAN),
            "b": Logger.colorize("┴", Logger.CYAN),
            "mid": Logger.colorize("┼", Logger.CYAN),
            "cross": Logger.colorize("┤", Logger.CYAN),
        }

    def _format_table_row(
        self,
        name: str,
        status_colored: str,
        col1_width: int,
        col2_width: int,
        v_char: str,
        status_value: str,
    ) -> str:
        """Format a single table row with proper alignment (DRY)."""
        name_padded = name + " " * (col1_width - len(name))
        status_padded = status_colored + " " * (col2_width - len(status_value))
        return f"{v_char} {name_padded} {v_char} {status_padded} {v_char}"

    def print_summary(self) -> int:
        """Print results summary table and return exit code using stdlib only."""
        Logger.banner("CODE QUALITY & COMPLIANCE SUMMARY")

        # Calculate column widths for proper alignment
        col1_width = max(
            len("Check Name"), max((len(r.name) for r in self.results), default=0)
        )
        col2_width = len("Status")

        # Get colored border characters
        borders = self._build_table_borders()

        # Build table lines
        table_lines: List[str] = []

        # Top border
        top_border = (
            f"{borders['tl']}{borders['h'] * (col1_width + 2)}{borders['t']}"
            f"{borders['h'] * (col2_width + 2)}{borders['tr']}"
        )
        table_lines.append(top_border)

        # Header row
        name_space = " " * (col1_width - len("Check Name") + 1)
        status_space = " " * (col2_width - len("Status") + 1)
        header = (
            f"{borders['v']} Check Name{name_space}"
            f"{borders['v']} Status{status_space}{borders['v']}"
        )
        table_lines.append(header)

        # Separator line
        separator = (
            f"{borders['mid']}{borders['h'] * (col1_width + 2)}{borders['mid']}"
            f"{borders['h'] * (col2_width + 2)}{borders['cross']}"
        )
        table_lines.append(separator)

        # Data rows
        failed_count = 0
        for result in self.results:
            status_text = result.status.value
            status_color = self._get_status_color(result.status)
            status_colored = Logger.colorize(status_text, status_color)

            if result.status == CheckStatus.FAIL:
                failed_count += 1

            row = self._format_table_row(
                result.name,
                status_colored,
                col1_width,
                col2_width,
                borders["v"],
                status_text,
            )
            table_lines.append(row)

        # Bottom border
        bottom_border = (
            f"{borders['bl']}{borders['h'] * (col1_width + 2)}{borders['b']}"
            f"{borders['h'] * (col2_width + 2)}{borders['br']}"
        )
        table_lines.append(bottom_border)

        # Print table
        print("\n".join(table_lines) + "\n")

        return 1 if failed_count > 0 else 0


def get_project_root() -> Path:
    """Get project root directory."""
    script_dir = Path(__file__).parent.resolve()
    return script_dir.parent


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Compliance check runner (use 'task --help' for available checks)",
        add_help=True,
    )

    parser.add_argument(
        "check",
        nargs="?",
        default="all",
        metavar="CHECK",
        help="Check to run: all|lint|publiccodelint|license|commit",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--version", action="version", version="1.0.0")

    args = parser.parse_args()

    # Map check names to methods
    check_map = {
        "lint": "check_lint",
        "publiccodelint": "check_publiccode",
        "license": "check_license",
        "commit": "check_commit",
    }

    valid_checks = {"all"} | check_map.keys()

    if args.check not in valid_checks:
        Logger.error(f"Unknown check: {args.check}")
        Logger.error(f"Valid checks: {', '.join(sorted(valid_checks))}")
        return 1

    # Initialize configuration
    project_root = get_project_root()
    config = ComplianceConfig(project_root=project_root, debug=args.debug)

    Logger.banner("Starting Code Quality & Compliance Checks")

    # Create checker instance
    checker = ComplianceChecker(config)

    # Run checks
    if args.check == "all":
        checker.results = checker.run_all()
    else:
        check_method = getattr(checker, check_map[args.check])
        checker.results = [check_method()]

    print()

    # Print summary and return exit code
    return checker.print_summary()


if __name__ == "__main__":
    sys.exit(main())
