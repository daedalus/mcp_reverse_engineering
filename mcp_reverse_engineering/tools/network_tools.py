"""Network tools for MCP Reverse Engineering Tool."""

from .base import BaseTool
from ..sandbox.execution import SandboxedExecutor
from typing import List


class NetworkTools(BaseTool):
    """Network analysis tools."""

    def __init__(self, executor: SandboxedExecutor):
        self.executor = executor

    def curl(self, args: List[str]) -> str:
        """Run the curl command."""
        return self.executor.execute(["curl"] + args)

    def wget(self, args: List[str]) -> str:
        """Run the wget command."""
        return self.executor.execute(["wget"] + args)