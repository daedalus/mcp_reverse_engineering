"""Pytest configuration and fixtures for MCP Reverse Engineering tests."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine


@pytest.fixture
def workspace() -> Generator[Path, None, None]:
    """Create a temporary workspace for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_binary(workspace: Path) -> Path:
    """Create a sample binary file for testing."""
    binary_path = workspace / "test_binary"
    binary_path.write_bytes(b"Hello, World!\x00\x00\x00\x00" + b"\x00" * 100)
    return binary_path


@pytest.fixture
def engine_with_tools(workspace: Path) -> ReverseEngineeringEngine:
    """Create an engine with tools enabled for testing."""
    config_content = """
settings:
  default_timeout: 120
  sandbox_enabled: true
  log_level: INFO

categories:
  file_analysis:
    enabled: true
    tools:
      - file
      - strings
      - hexdump
      - xxd

  binary_analysis:
    enabled: true
    tools:
      - objdump
      - readelf
      - ldd
      - strace
      - ltrace

  firmware_analysis:
    enabled: false
    tools: []

  network:
    enabled: false
    tools: []
"""
    config_path = workspace / "test_config.yaml"
    config_path.write_text(config_content)
    return ReverseEngineeringEngine(
        workspace=str(workspace), config_path=str(config_path)
    )
