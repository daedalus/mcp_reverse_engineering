"""File tools for MCP Reverse Engineering Tool."""

from .base import BaseTool
from ..sandbox.execution import SandboxedExecutor
from typing import List


class FileTools(BaseTool):
    """File analysis tools."""

    def __init__(self, executor: SandboxedExecutor):
        self.executor = executor

    def file(self, args: List[str]) -> str:
        """Run the file command."""
        return self.executor.execute(["file"] + args)

    def strings(self, args: List[str]) -> str:
        """Run the strings command."""
        return self.executor.execute(["strings"] + args)

    def hexdump(self, args: List[str]) -> str:
        """Run the hexdump command."""
        return self.executor.execute(["hexdump"] + args)

    def xxd(self, args: List[str]) -> str:
        """Run the xxd command."""
        return self.executor.execute(["xxd"] + args)