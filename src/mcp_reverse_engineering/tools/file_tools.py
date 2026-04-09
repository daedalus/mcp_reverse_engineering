"""File tools for MCP Reverse Engineering Tool."""

from ..sandbox.execution import SandboxedExecutor
from .base import BaseTool


class FileTools(BaseTool):
    """File analysis tools."""

    def __init__(self, executor: SandboxedExecutor) -> None:
        self.executor = executor

    def file(self, args: list[str]) -> str:
        """Run the file command."""
        return self.executor.execute(["file"] + args)

    def strings(self, args: list[str]) -> str:
        """Run the strings command."""
        return self.executor.execute(["strings"] + args)

    def hexdump(self, args: list[str]) -> str:
        """Run the hexdump command."""
        return self.executor.execute(["hexdump"] + args)

    def xxd(self, args: list[str]) -> str:
        """Run the xxd command."""
        return self.executor.execute(["xxd"] + args)
