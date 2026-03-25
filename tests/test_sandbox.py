"""Tests for the sandboxed execution module."""

from pathlib import Path

import pytest

from mcp_reverse_engineering.sandbox.execution import SandboxedExecutor


class TestSandboxedExecutor:
    """Test cases for SandboxedExecutor."""

    def test_basic_execution(self, workspace: Path) -> None:
        """Test basic command execution."""
        executor = SandboxedExecutor(workspace, timeout=5)
        result = executor.execute(["echo", "Hello, World!"])
        assert "Hello, World!" in result

    def test_workspace_jail(self, workspace: Path) -> None:
        """Test that commands are executed in the workspace."""
        test_file = workspace / "test.txt"
        test_file.write_text("test content")

        executor = SandboxedExecutor(workspace, timeout=5)
        result = executor.execute(["cat", "test.txt"])
        assert result.strip() == "test content"

    def test_command_validation_suspicious(self, workspace: Path) -> None:
        """Test that suspicious commands raise ValueError."""
        executor = SandboxedExecutor(workspace, timeout=5)
        with pytest.raises(ValueError, match="Suspicious argument"):
            executor.execute(["ls", "../../../etc/passwd"])

    def test_timeout(self, workspace: Path) -> None:
        """Test that timeout is enforced."""
        executor = SandboxedExecutor(workspace, timeout=1)
        result = executor.execute(["sleep", "10"])
        assert "timed out" in result.lower()

    def test_failed_command(self, workspace: Path) -> None:
        """Test handling of failed commands."""
        executor = SandboxedExecutor(workspace, timeout=5)
        result = executor.execute(["false"])
        assert "failed with return code" in result

    def test_invalid_command(self, workspace: Path) -> None:
        """Test handling of invalid commands."""
        executor = SandboxedExecutor(workspace, timeout=5)
        result = executor.execute(["nonexistent_command_xyz"])
        assert "Error executing command" in result
