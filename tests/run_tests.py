#!/usr/bin/env python
# ///////////////////////////////////////////////////////////////
# RUN_TESTS - Test runner script
# Project: flash-excel
# ///////////////////////////////////////////////////////////////

"""
Test runner script for flash-excel.

Provides a convenient CLI wrapper around pytest for executing tests
with various configurations. Tests live flat under tests/ and are
categorized via markers (unit, integration, robustness) rather than
subdirectories.

Supports:
    - Running all tests or filtering by marker (unit/integration/robustness)
    - Coverage reporting
    - Verbose output
    - Parallel execution via pytest-xdist
    - Fast mode (excluding slow tests)

Example:
    python run_tests.py --type unit --verbose --coverage
    python run_tests.py --type all --parallel
    python run_tests.py --marker integration --fast
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import argparse
import logging
import subprocess
import sys
from pathlib import Path

# ///////////////////////////////////////////////////////////////
# HELPER FUNCTIONS
# ///////////////////////////////////////////////////////////////

logger = logging.getLogger(__name__)


def run_command(cmd: list[str], description: str) -> bool:
    """
    Execute a shell command and display output in real-time.

    Runs a command using subprocess with output displayed directly to the console
    without buffering. This provides real-time feedback during test execution.

    Args:
        cmd: Command and arguments as list of strings
        description: Human-readable description of what's running

    Returns:
        bool: True if command succeeded (exit code 0), False otherwise

    Note:
        Uses S603 security rule bypass for subprocess.run() since this is
        a test runner with trusted input.
    """
    logger.info("\n%s", "=" * 60)
    logger.info("%s", description)
    logger.info("%s", "=" * 60)
    try:
        # Run without capturing output - displays in real-time
        result = subprocess.run(cmd, check=False)  # noqa: S603
        return result.returncode == 0
    except Exception as e:
        logger.exception("Execution error: %s", e)
        return False


# ///////////////////////////////////////////////////////////////
# MAIN FUNCTION
# ///////////////////////////////////////////////////////////////


def main() -> None:
    """
    Main entry point for the test runner.

    Parses CLI arguments and executes pytest with appropriate configuration.
    Validates that pyproject.toml exists before running tests.

    Exit codes:
        0: All tests passed
        1: Tests failed or pyproject.toml not found
    """
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Test runner for EzCompiler with flexible configuration"
    )
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "robustness", "all"],
        default="all",
        help="Test type to run, filtered by marker if not 'all' (default: all, "
        "since existing tests are not yet marker-categorized)",
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report (HTML + terminal)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output (shows each test)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Exclude slow tests (deselect with 'slow' marker)",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel using pytest-xdist",
    )
    parser.add_argument(
        "--marker",
        type=str,
        help="Run only tests with specific marker (e.g., integration, robustness)",
    )
    args = parser.parse_args()

    # Validate project structure
    if not Path("pyproject.toml").exists():
        logger.error("pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)

    # Build pytest command
    cmd_parts = [sys.executable, "-m", "pytest"]

    # Add verbosity flag
    if args.verbose:
        cmd_parts.append("-v")

    # Add marker-based filtering (tests are flat under tests/, categorized via markers)
    markers = []
    if args.fast:
        markers.append("not slow")
    if args.marker:
        markers.append(args.marker)
    elif args.type != "all":
        markers.append(args.type)
    if markers:
        cmd_parts.extend(["-m", " and ".join(markers)])

    # Add parallel execution
    if args.parallel:
        cmd_parts.extend(["-n", "auto"])

    # Test path (flat directory, filtering handled via markers above)
    cmd_parts.append("tests/")

    # Add coverage options
    if args.coverage:
        cmd_parts.extend(
            [
                "--cov=src/flash_excel",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
            ]
        )

    # Execute tests
    success = run_command(cmd_parts, f"Running {args.type} tests")

    # Display results
    if success:
        logger.info("Tests passed successfully")
        if args.coverage:
            logger.info("Coverage report generated in htmlcov/")
            logger.info("Open htmlcov/index.html in your browser")
    else:
        logger.error("Tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
