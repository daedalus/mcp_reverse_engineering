"""Sandboxed execution module for MCP Reverse Engineering Tool."""

import logging
import os
import resource
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class SandboxedExecutor:
    """Executor that runs commands in a sandboxed environment."""

    def __init__(self, workspace: Path, timeout: int = 30) -> None:
        """
        Initialize the sandboxed executor.

        Args:
            workspace: Directory jail for file operations
            timeout: Default timeout for command execution in seconds
        """
        self.workspace = workspace.resolve()
        self.timeout = timeout
        # Ensure workspace exists
        self.workspace.mkdir(parents=True, exist_ok=True)

    def execute(self, command: list[str], input_data: bytes | None = None) -> str:
        """
        Execute a command in a sandboxed environment.

        Args:
            command: Command and arguments as list of strings
            input_data: Optional input data for stdin

        Returns:
            Command output as string
        """
        # Validate command doesn't attempt to escape workspace
        self._validate_command(command)

        # Set up sandbox constraints
        def preexec_fn() -> None:
            # Change working directory to workspace
            os.chdir(str(self.workspace))

            # Set resource limits
            # Limit CPU time
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
            # Limit memory usage (256 MB)
            resource.setrlimit(
                resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024)
            )
            # Limit number of processes
            resource.setrlimit(resource.RLIMIT_NPROC, (50, 50))
            # Limit file size (100 MB)
            resource.setrlimit(
                resource.RLIMIT_FSIZE, (100 * 1024 * 1024, 100 * 1024 * 1024)
            )

        try:
            # Execute command with timeout
            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                preexec_fn=preexec_fn,
            )

            # Check if process was killed due to timeout or signal
            if result.returncode < 0:
                logger.warning(
                    f"Command {command} was terminated by signal {-result.returncode}"
                )
                return f"Command terminated by signal {-result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

            # Return stdout if successful, otherwise include stderr
            if result.returncode == 0:
                return result.stdout  # type: ignore[no-any-return]
            else:
                logger.warning(
                    f"Command {command} failed with return code {result.returncode}"
                )
                return f"Command failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

        except subprocess.TimeoutExpired:
            logger.error(f"Command {command} timed out after {self.timeout} seconds")
            return f"Command timed out after {self.timeout} seconds"
        except Exception as e:
            logger.error(f"Error executing command {command}: {str(e)}")
            return f"Error executing command: {str(e)}"

    def _validate_command(self, command: list[str]) -> None:
        """Validate that command doesn't attempt to escape the workspace."""
        # Check for obvious escape attempts in arguments
        for arg in command:
            if ".." in arg and not arg.startswith("-"):
                # Allow .. in flags like --parent but not in path arguments
                if not arg.startswith("-"):
                    raise ValueError(f"Suspicious argument containing '..': {arg}")

            # Check for absolute paths that might escape workspace
            if arg.startswith("/") and not arg.startswith(str(self.workspace)):
                # Allow certain system paths that are typically safe
                safe_paths = [
                    "/bin/",
                    "/usr/bin/",
                    "/usr/local/bin/",
                    "/lib/",
                    "/usr/lib/",
                    "/etc/",
                ]
                if not any(arg.startswith(safe) for safe in safe_paths):
                    logger.warning(f"Potentially unsafe absolute path: {arg}")
                    # In a stricter implementation, we might block this
                    # For now, we'll just warn and allow it since many tools need system paths
