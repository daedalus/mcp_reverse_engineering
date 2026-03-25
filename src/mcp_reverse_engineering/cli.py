"""Command Line Interface for MCP Reverse Engineering Tool."""

import argparse
import sys

from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="MCP Reverse Engineering Tool")
    parser.add_argument(
        "--tool", required=True, help="Tool to use (e.g., strings, objdump)"
    )
    parser.add_argument(
        "--args", nargs=argparse.REMAINDER, help="Arguments for the tool"
    )
    parser.add_argument("--file", help="File to analyze")
    parser.add_argument(
        "--workspace", default="./workspace", help="Workspace directory"
    )
    parser.add_argument("--config", help="Path to tools_config.yaml")

    args = parser.parse_args()

    engine = ReverseEngineeringEngine(
        workspace=args.workspace,
        config_path=args.config,
    )

    try:
        result = engine.execute_tool(args.tool, args.args or [], args.file)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
