import shutil

import pytest


@pytest.fixture
def workspace(tmp_path):
    """Create a temporary workspace directory."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()
    yield workspace_dir
    shutil.rmtree(workspace_dir, ignore_errors=True)


@pytest.fixture
def sample_binary(tmp_path):
    """Create a sample binary file for testing."""
    binary_path = tmp_path / "sample"
    with open(binary_path, "wb") as f:
        f.write(b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x3e\x00")
    yield binary_path


@pytest.fixture
def sample_text(tmp_path):
    """Create a sample text file for testing."""
    text_path = tmp_path / "sample.txt"
    text_path.write_text("Hello, World!\nTest content\n")
    yield text_path
