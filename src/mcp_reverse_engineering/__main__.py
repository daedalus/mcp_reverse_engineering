"""CLI entry point for mcp_reverse_engineering.

This module provides the command-line interface entry point for the
reverse engineering tool. It is invoked when running the package as
a CLI application.
"""

from mcp_reverse_engineering.server import mcp


def main() -> None:
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
