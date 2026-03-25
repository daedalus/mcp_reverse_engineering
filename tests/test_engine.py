"""Tests for the MCP Reverse Engineering Engine."""

from pathlib import Path

import pytest

from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine


class TestReverseEngineeringEngine:
    """Test cases for ReverseEngineeringEngine."""

    def test_initialization(self, workspace: Path) -> None:
        """Test that the engine initializes correctly."""
        engine = ReverseEngineeringEngine(workspace=str(workspace))
        assert isinstance(engine, ReverseEngineeringEngine)
        assert engine.workspace.exists()

    def test_list_available_tools(
        self, engine_with_tools: ReverseEngineeringEngine
    ) -> None:
        """Test that we can list available tools."""
        tools = engine_with_tools.list_available_tools()
        assert isinstance(tools, list)
        assert "file" in tools
        assert "strings" in tools
        assert "objdump" in tools

    def test_get_tool_documentation(self, workspace: Path) -> None:
        """Test that we can get tool documentation."""
        engine = ReverseEngineeringEngine(workspace=str(workspace))
        docs = engine.get_tool_documentation("file")
        assert isinstance(docs, dict)
        assert "description" in docs
        assert docs["description"] == "Determine file type"

    def test_validate_args(self, workspace: Path) -> None:
        """Test argument validation."""
        engine = ReverseEngineeringEngine(workspace=str(workspace))
        args = ["--help", "-n", "5"]
        validated = engine._validate_args("strings", args)
        assert isinstance(validated, list)

    def test_prepare_file(self, workspace: Path) -> None:
        """Test file preparation."""
        test_file = workspace / "test.txt"
        test_file.write_text("Hello, World!")

        engine = ReverseEngineeringEngine(workspace=str(workspace))
        prepared = engine._prepare_file(str(test_file))
        assert prepared == str(test_file)

    def test_prepare_file_not_found(self, workspace: Path) -> None:
        """Test that FileNotFoundError is raised for missing files."""
        engine = ReverseEngineeringEngine(workspace=str(workspace))
        with pytest.raises(FileNotFoundError, match="File not found"):
            engine._prepare_file(str(workspace / "nonexistent.txt"))

    def test_truncate_output_short(self, workspace: Path) -> None:
        """Test output truncation with short output."""
        engine = ReverseEngineeringEngine(workspace=str(workspace))
        short_output = "Line 1\nLine 2\nLine 3"
        truncated = engine._truncate_output(short_output, max_lines=5)
        assert truncated == short_output

    def test_truncate_output_long(self, workspace: Path) -> None:
        """Test output truncation with long output."""
        engine = ReverseEngineeringEngine(workspace=str(workspace))
        long_output = "\n".join([f"Line {i}" for i in range(150)])
        truncated = engine._truncate_output(long_output, max_lines=100)
        assert "... (output truncated" in truncated
        assert len(truncated.split("\n")) <= 101

    def test_execute_tool_unknown_tool(self, workspace: Path) -> None:
        """Test that ValueError is raised for unknown tools."""
        engine = ReverseEngineeringEngine(workspace=str(workspace))
        with pytest.raises(ValueError, match="Unknown tool"):
            engine.execute_tool("nonexistent_tool", [])

    def test_get_mcp_tools(self, engine_with_tools: ReverseEngineeringEngine) -> None:
        """Test MCP tool schema generation."""
        mcp_tools = engine_with_tools.get_mcp_tools()
        assert isinstance(mcp_tools, list)
        assert len(mcp_tools) > 0
        assert all("name" in tool for tool in mcp_tools)
        assert all("description" in tool for tool in mcp_tools)
        assert all("inputSchema" in tool for tool in mcp_tools)
