"""Tests for the MCP Reverse Engineering Engine."""

# Add the package to the path so we can import it
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine
from mcp_reverse_engineering.tools.binary_tools import BinaryTools


class TestReverseEngineeringEngine(unittest.TestCase):
    """Test cases for ReverseEngineeringEngine."""

    def setUp(self):
        """Set up test fixtures."""
        self.workspace = tempfile.mkdtemp()
        self.engine = ReverseEngineeringEngine(workspace=self.workspace)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up workspace
        import shutil

        shutil.rmtree(self.workspace)

    def test_initialization(self):
        """Test that the engine initializes correctly."""
        self.assertIsInstance(self.engine, ReverseEngineeringEngine)
        self.assertTrue(Path(self.engine.workspace).exists())

    def test_list_available_tools(self):
        """Test that we can list available tools."""
        tools = self.engine.list_available_tools()
        self.assertIsInstance(tools, list)

    def test_get_tool_documentation(self):
        """Test that we can get tool documentation."""
        docs = self.engine.get_tool_documentation("file")
        self.assertIsInstance(docs, dict)
        self.assertIn("description", docs)
        self.assertEqual(docs["description"], "Determine file type")

    def test_validate_args(self):
        """Test argument validation."""
        # This is a basic test - in reality, validation happens in the executor
        args = ["--help", "-n", "5"]
        validated = self.engine._validate_args("strings", args)
        self.assertIsInstance(validated, list)

    def test_fq_in_tool_map(self):
        """Test that fq is mapped in TOOL_CATEGORY_MAP and TOOL_METHOD_MAP."""
        from mcp_reverse_engineering.core.engine import (
            TOOL_CATEGORY_MAP,
            TOOL_METHOD_MAP,
        )

        self.assertIn("fq", TOOL_CATEGORY_MAP)
        self.assertEqual(TOOL_CATEGORY_MAP["fq"], "binary_tools")
        self.assertIn("fq", TOOL_METHOD_MAP)
        self.assertEqual(TOOL_METHOD_MAP["fq"], "fq")

    def test_prepare_file(self):
        """Test file preparation."""
        # Create a test file
        test_file = Path(self.workspace) / "test.txt"
        test_file.write_text("Hello, World!")

        # Test preparing a file inside workspace
        prepared = self.engine._prepare_file(str(test_file))
        self.assertEqual(prepared, str(test_file))

    def test_truncate_output(self):
        """Test output truncation."""
        # Test with short output
        short_output = "Line 1\nLine 2\nLine 3"
        truncated = self.engine._truncate_output(short_output, max_lines=5)
        self.assertEqual(truncated, short_output)

        # Test with long output
        long_output = "\n".join([f"Line {i}" for i in range(150)])
        truncated = self.engine._truncate_output(long_output, max_lines=100)
        self.assertIn("... (output truncated", truncated)
        self.assertTrue(
            len(truncated.split("\n")) <= 101
        )  # 100 lines + truncation message


class TestBinaryTools(unittest.TestCase):
    """Test cases for BinaryTools."""

    def setUp(self):
        """Set up test fixtures."""
        self.workspace = Path(tempfile.mkdtemp())
        from mcp_reverse_engineering.sandbox.execution import SandboxedExecutor

        self.executor = SandboxedExecutor(self.workspace, timeout=30)
        self.binary_tools = BinaryTools(self.executor)

    def tearDown(self):
        """Tear down test fixtures."""
        import shutil

        shutil.rmtree(self.workspace)

    def test_fq_method_exists(self):
        """Test that fq method exists in BinaryTools."""
        self.assertTrue(hasattr(self.binary_tools, "fq"))
        self.assertTrue(callable(getattr(self.binary_tools, "fq")))

    def test_fq_help(self):
        """Test fq --help execution."""
        result = self.binary_tools.fq(["--help"])
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
