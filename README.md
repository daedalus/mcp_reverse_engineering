# mcp-reverse-engineering

A sandboxed MCP (Model Context Protocol) tool for reverse engineering that provides a unified interface to various reverse engineering tools with security restrictions.

[![PyPI](https://img.shields.io/pypi/v/mcp-reverse-engineering.svg)](https://pypi.org/project/mcp-reverse-engineering/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-reverse-engineering.svg)](https://pypi.org/project/mcp-reverse-engineering/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/daedalus/mcp_reverse_engineering)

## Purpose

This project provides a secure, sandboxed environment for executing reverse engineering tools via CLI or MCP protocol. It wraps common reverse engineering utilities (strings, objdump, readelf, binwalk, etc.) with safety features like filesystem isolation, timeouts, and argument validation.

## Install

```bash
pip install mcp-reverse-engineering
```

Or for development:

```bash
pip install -e ".[dev]"
```

### MCP Server Installation

To use as an MCP server with Claude Desktop:

```bash
mcp install src/mcp_reverse_engineering/server.py
```

## Usage

### CLI

```bash
# Extract strings from a binary
mcp-re --tool strings --file /path/to/binary

# Disassemble a binary
mcp-re --tool objdump --args "['-d']" --file /path/to/binary

# Analyze ELF headers
mcp-re --tool readelf --args "['-h', '-s']" --file /path/to/elf

# Run binwalk for firmware analysis
mcp-re --tool binwalk --file /path/to/firmware.bin
```

### Python API

```python
from mcp_reverse_engineering import ReverseEngineeringEngine

# Create engine with default config
engine = ReverseEngineeringEngine(
    workspace="./workspace",
    timeout=30,
)

# List available tools
print(engine.list_available_tools())

# Execute a tool
result = engine.execute_tool("strings", ["-n", "8"], "/path/to/binary")
print(result)
```

### MCP Server

```python
from mcp_reverse_engineering.server import mcp, strings, objdump, readelf, binwalk

# Run the server (stdio transport for Claude Desktop)
if __name__ == "__main__":
    mcp.run()
```

## API

### ReverseEngineeringEngine

Main class for executing reverse engineering tools.

```python
engine = ReverseEngineeringEngine(
    workspace: str = "./workspace",  # Sandbox directory
    timeout: int = 30,               # Tool execution timeout
    config_path: str | Path | None = None,  # YAML config path
)
```

**Methods:**

- `execute_tool(tool_name: str, args: List[str], file_path: Optional[str] = None) -> str` - Execute a tool
- `list_available_tools() -> List[str]` - List enabled tools
- `get_tool_documentation(tool_name: str) -> Dict[str, Any]` - Get tool docs
- `get_mcp_tools() -> List[Dict[str, Any]]` - Get MCP tool schemas

### Available Tools

| Tool | Category | Description |
|------|----------|-------------|
| file | file_tools | Determine file type |
| strings | file_tools | Extract printable strings |
| hexdump | file_tools | Hexadecimal dump |
| xxd | file_tools | Hexadecimal dump |
| objdump | binary_tools | Disassemble binary |
| readelf | binary_tools | Read ELF headers |
| binwalk | firmware_tools | Firmware analysis |

## Development

```bash
# Clone the repository
git clone https://github.com/daedalus/mcp_reverse_engineering.git
cd mcp_reverse_engineering

# Install dependencies
pip install -e ".[test]"

# Run tests
pytest

# Format code
ruff format src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## MCP Server Configuration

mcp-name: io.github.daedalus/mcp-reverse-engineering

## Requirements

- Python 3.11+
- External tools: binwalk, radare2, ghidra, etc. (must be installed separately)

## License

MIT
