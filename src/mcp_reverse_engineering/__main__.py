"""CLI entry point for mcp_reverse_engineering.

This module provides the command-line interface entry point for the
reverse engineering tool. It is invoked when running the package as
a CLI application.
"""


from mcp_reverse_engineering.cli import main


def cli_main() -> int:
    """Entry point for the CLI.

    Returns:
        int: Exit code (0 for success, non-zero for failure).

    Example:
        >>> sys.exit(cli_main())
    """
    return main()


if __name__ == "__main__":
    raise SystemExit(cli_main())
