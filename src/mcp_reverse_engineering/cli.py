#!/usr/bin/env python3
"""Command Line Interface for MCP Reverse Engineering Tool.

This module provides the CLI interface for the reverse engineering tool.
It allows users to execute various reverse engineering tools from
the command line with sandboxed execution.
"""

import argparse
import sys

from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine


def cli_main() -> int:
    """Main entry point for the CLI.

    Parses command-line arguments and executes the specified tool
    using the ReverseEngineeringEngine.

    Returns:
        int: Exit code (0 for success, non-zero for failure).

    Raises:
        SystemExit: If argument parsing fails or tool execution fails.
    """
    parser = argparse.ArgumentParser(
        description="MCP Reverse Engineering Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --tool strings --file /path/to/binary
  %(prog)s --tool objdump --args "['-d']" --file /path/to/binary
  %(prog)s --tool readelf --args "['-h', '-s']" --file /path/to/elf
        """,
    )
    parser.add_argument(
        "--tool",
        required=True,
        help="Tool to use (e.g., strings, objdump, readelf, hexdump)",
    )
    parser.add_argument(
        "--args",
        nargs=argparse.REMAINDER,
        help="Arguments for the tool as a JSON list",
    )
    parser.add_argument(
        "--file",
        help="File to analyze",
    )
    parser.add_argument(
        "--workspace",
        default="./workspace",
        help="Workspace directory (default: ./workspace)",
    )
    parser.add_argument(
        "--config",
        help="Path to tools_config.yaml",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout for tool execution in seconds (default: 30)",
    )

    args = parser.parse_args()

    engine = ReverseEngineeringEngine(
        workspace=args.workspace,
        config_path=args.config,
        timeout=args.timeout,
    )

    try:
        result = engine.execute_tool(args.tool, args.args or [], args.file)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Entry point for the MCP server (runs in stdio mode)."""
    from mcp_reverse_engineering.server import mcp

    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
