"""Base tool class for MCP Reverse Engineering Tool."""

from typing import List


class BaseTool:
    """Base class for all tools."""

    def execute(self, args: List[str]) -> str:
        """
        Execute the tool with given arguments.
        Subclasses must implement this method.

        Args:
            args: List of arguments for the tool

        Returns:
            Tool output as string
        """
        raise NotImplementedError("Subclasses must implement execute method")

    def validate_args(self, args: List[str]) -> List[str]:
        """Validate tool arguments. Override in subclasses for specific validation."""
        return args