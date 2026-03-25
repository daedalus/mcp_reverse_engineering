"""Network tools for MCP Reverse Engineering Tool."""

from mcp_reverse_engineering.sandbox.execution import SandboxedExecutor
from mcp_reverse_engineering.tools.base import BaseTool


class NetworkTools(BaseTool):
    """Network analysis tools."""

    def __init__(self, executor: SandboxedExecutor) -> None:
        self.executor = executor

    def curl(self, args: list[str]) -> str:
        """Run the curl command."""
        return self.executor.execute(["curl"] + args)

    def wget(self, args: list[str]) -> str:
        """Run the wget command."""
        return self.executor.execute(["wget"] + args)
