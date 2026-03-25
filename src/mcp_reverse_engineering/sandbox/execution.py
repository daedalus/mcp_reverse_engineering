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
        self._validate_command(command)

        def preexec_fn() -> None:
            os.chdir(str(self.workspace))
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
            resource.setrlimit(
                resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024)
            )
            resource.setrlimit(resource.RLIMIT_NPROC, (50, 50))
            resource.setrlimit(
                resource.RLIMIT_FSIZE, (100 * 1024 * 1024, 100 * 1024 * 1024)
            )

        try:
            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                preexec_fn=preexec_fn,
            )

            if result.returncode < 0:
                logger.warning(
                    f"Command {command} was terminated by signal {-result.returncode}"
                )
                return f"Command terminated by signal {-result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

            if result.returncode == 0:
                return result.stdout
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
        for arg in command:
            if ".." in arg and not arg.startswith("-"):
                if not arg.startswith("-"):
                    raise ValueError(f"Suspicious argument containing '..': {arg}")

            if arg.startswith("/") and not arg.startswith(str(self.workspace)):
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
