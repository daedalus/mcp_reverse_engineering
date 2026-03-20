"""Tests for the sandboxed execution module."""

import unittest
import tempfile
import os
from pathlib import Path

# Add the package to the path so we can import it
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_reverse_engineering.sandbox.execution import SandboxedExecutor


class TestSandboxedExecutor(unittest.TestCase):
    """Test cases for SandboxedExecutor."""

    def setUp(self):
        """Set up test fixtures."""
        self.workspace = tempfile.mkdtemp()
        self.executor = SandboxedExecutor(Path(self.workspace), timeout=5)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up workspace
        import shutil
        shutil.rmtree(self.workspace)

    def test_basic_execution(self):
        """Test basic command execution."""
        result = self.executor.execute(["echo", "Hello, World!"])
        self.assertIn("Hello, World!", result)

    def test_workspace_jail(self):
        """Test that commands are executed in the workspace."""
        # Create a file in workspace
        test_file = Path(self.workspace) / "test.txt"
        test_file.write_text("test content")
        
        # Try to read it using cat
        result = self.executor.execute(["cat", "test.txt"])
        self.assertEqual(result.strip(), "test content")

    def test_command_validation(self):
        """Test that suspicious commands are handled."""
        # This should work (normal command)
        result = self.executor.execute(["ls", "-la"])
        self.assertIsInstance(result, str)
        
        # Test with suspicious path (should warn but still allow for system commands)
        result = self.executor.execute(["ls", "/bin"])
        self.assertIsInstance(result, str)

    def test_timeout(self):
        """Test that timeout is enforced."""
        # This command should timeout (sleep longer than timeout)
        result = self.executor.execute(["sleep", "10"])
        self.assertIn("timed out", result.lower())

if __name__ == "__main__":
    unittest.main()