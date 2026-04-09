"""Main engine for MCP Reverse Engineering Tool."""

from pathlib import Path
from typing import Any

from ..knowledge_base.documentation import ToolDocumentation
from ..sandbox.execution import SandboxedExecutor
from ..tools.binary_tools import BinaryTools
from ..tools.file_tools import FileTools
from ..tools.firmware_tools import FirmwareTools
from ..tools.network_tools import NetworkTools
from .config import load_config

TOOL_CATEGORY_MAP = {
    "file": "file_tools",
    "strings": "file_tools",
    "hexdump": "file_tools",
    "xxd": "file_tools",
    "objdump": "binary_tools",
    "readelf": "binary_tools",
    "ldd": "binary_tools",
    "strace": "binary_tools",
    "ltrace": "binary_tools",
    "upx": "binary_tools",
    "gdb": "binary_tools",
    "radare2": "binary_tools",
    "angr": "binary_tools",
    "ghidra": "binary_tools",
    "frida": "binary_tools",
    "fq": "binary_tools",
    "binwalk": "firmware_tools",
    "unsquashfs": "firmware_tools",
    "sasquatch": "firmware_tools",
    "jefferson": "firmware_tools",
    "ubi_reader": "firmware_tools",
    "unpackers": "firmware_tools",
    "retdc": "firmware_tools",
    "qemu": "firmware_tools",
    "curl": "network_tools",
    "wget": "network_tools",
}

TOOL_METHOD_MAP = {
    "file": "file",
    "strings": "strings",
    "hexdump": "hexdump",
    "xxd": "xxd",
    "objdump": "objdump",
    "readelf": "readelf",
    "ldd": "ldd",
    "strace": "strace",
    "ltrace": "ltrace",
    "upx": "upx",
    "gdb": "gdb",
    "radare2": "radare2",
    "angr": "angr",
    "ghidra": "ghidra",
    "frida": "frida",
    "fq": "fq",
    "binwalk": "binwalk",
    "unsquashfs": "unsquashfs",
    "sasquatch": "sasquatch",
    "jefferson": "jefferson",
    "ubi_reader": "ubi_reader",
    "unpackers": "unpackers",
    "retdc": "retdc",
    "qemu": "qemu",
    "curl": "curl",
    "wget": "wget",
}


class ReverseEngineeringEngine:
    """Main engine for the MCP Reverse Engineering Tool."""

    def __init__(
        self,
        workspace: str = "./workspace",
        timeout: int = 30,
        config_path: str | Path | None = None,
    ) -> None:
        """
        Initialize the reverse engineering engine.

        Args:
            workspace: Directory for file operations (will be jailed)
            timeout: Default timeout for tool execution in seconds
            config_path: Path to tools_config.yaml. If None, uses default location.
        """
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self.executor = SandboxedExecutor(self.workspace, timeout)
        self.documentation = ToolDocumentation()

        self.tool_config = load_config(config_path)

        self.file_tools = FileTools(self.executor)
        self.binary_tools = BinaryTools(self.executor)
        self.firmware_tools = FirmwareTools(self.executor)
        self.network_tools = NetworkTools(self.executor)

        self._tool_instances = {
            "file_tools": self.file_tools,
            "binary_tools": self.binary_tools,
            "firmware_tools": self.firmware_tools,
            "network_tools": self.network_tools,
        }

        self.tools = self._load_enabled_tools()

    def _load_enabled_tools(self) -> dict[str, Any]:
        """Load only tools that are enabled in the configuration."""
        enabled_tools = self.tool_config.list_enabled_tools()

        tools = {}
        for tool_name in enabled_tools:
            category = TOOL_CATEGORY_MAP.get(tool_name)
            method_name = TOOL_METHOD_MAP.get(tool_name)

            if category and method_name:
                instance = self._tool_instances.get(category)
                if instance:
                    method = getattr(instance, method_name, None)
                    if method:
                        tools[tool_name] = method

        return tools

    def execute_tool(
        self, tool_name: str, args: list[str], file_path: str | None = None
    ) -> str:
        """
        Execute a tool with given arguments.

        Args:
            tool_name: Name of the tool to execute
            args: List of arguments for the tool
            file_path: Optional file path to operate on

        Returns:
            Tool output as string
        """
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        # Validate arguments
        validated_args = self._validate_args(tool_name, args)

        # Prepare file if needed
        if file_path:
            file_path = self._prepare_file(file_path)
            # Add file to args if not already present
            if file_path not in validated_args:
                validated_args.append(file_path)

        # Execute tool
        try:
            result = self.tools[tool_name](validated_args)
            return self._truncate_output(result)
        except Exception as e:
            raise RuntimeError(f"Failed to execute {tool_name}: {str(e)}")

    def _validate_args(self, _tool_name: str, args: list[str]) -> list[str]:
        """Validate and sanitize tool arguments."""
        # tool_name reserved for future validation rules per-tool
        # Basic validation - in a real implementation, this would be more sophisticated
        validated = []
        for arg in args:
            # Prevent directory traversal
            if ".." in arg or arg.startswith("/"):
                # Only allow args that are within workspace or are simple flags/values
                if not (arg.startswith("-") or "_" in arg or "." in arg):
                    continue
            validated.append(arg)
        return validated

    def _prepare_file(self, file_path: str) -> str:
        """Prepare a file for use within the workspace jail."""
        source_path = Path(file_path).resolve()
        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Copy file to workspace if it's outside
        if not str(source_path).startswith(str(self.workspace)):
            # In a real implementation, we'd copy the file to workspace
            # For now, we'll just use the source if it's accessible
            return str(source_path)
        return str(source_path)

    def _truncate_output(self, output: str, max_lines: int = 100) -> str:
        """Truncate tool output to prevent excessive data."""
        lines = output.split("\n")
        if len(lines) > max_lines:
            return (
                "\n".join(lines[:max_lines])
                + f"\n... (output truncated, {len(lines)} total lines)"
            )
        return output

    def get_tool_documentation(self, tool_name: str) -> dict[str, Any]:
        """Get documentation for a specific tool."""
        return self.documentation.get_tool_docs(tool_name)

    def list_available_tools(self) -> list[str]:
        """List all available tools."""
        return list(self.tools.keys())

    def get_mcp_tools(self) -> list[dict[str, Any]]:
        """
        Get tools formatted as MCP tool schemas.

        Returns:
            List of tool definitions compatible with MCP protocol.
        """
        mcp_tools = []
        for tool_name in self.tools:
            docs = self.documentation.get_tool_docs(tool_name)
            mcp_tools.append(
                {
                    "name": tool_name,
                    "description": docs.get("description", f"Execute {tool_name} tool"),
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "args": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Arguments for the tool",
                            },
                            "file": {
                                "type": "string",
                                "description": "File path to operate on",
                            },
                        },
                    },
                }
            )
        return mcp_tools
