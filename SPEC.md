# SPEC.md — mcp_reverse_engineering

## Purpose

A sandboxed MCP (Managed Computation Platform) tool for reverse engineering that provides a unified interface to various reverse engineering tools with security restrictions. It offers a CLI and Python API for executing binary analysis, firmware analysis, file analysis, and network tools in a controlled environment.

## Scope

### What IS in scope

- Sandboxed execution of reverse engineering tools with timeouts and filesystem jail
- Unified interface to multiple reverse engineering tools via CLI and Python API
- Configurable tool loading via YAML configuration
- Tool categories: File Analysis, Binary Analysis, Firmware Analysis, Network Tools
- Argument validation and output truncation for safety
- Built-in tool documentation
- MCP-compatible tool schemas for integration

### What is NOT in scope

- Installation of reverse engineering tools (binwalk, radare2, etc.) - must be installed separately
- GUI or web interface
- Remote execution
- Persistence or database
- User authentication/authorization

## Public API / Interface

### Python API

```python
from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine

engine = ReverseEngineeringEngine(
    workspace: str = "./workspace",
    timeout: int = 30,
    config_path: str | Path | None = None
) -> ReverseEngineeringEngine
```

Methods:
- `engine.execute_tool(tool_name: str, args: List[str], file_path: Optional[str] = None) -> str` - Execute a tool
- `engine.list_available_tools() -> List[str]` - List enabled tools
- `engine.get_tool_documentation(tool_name: str) -> Dict[str, Any]` - Get tool docs
- `engine.get_mcp_tools() -> List[Dict[str, Any]]` - Get MCP tool schemas

### CLI API

```bash
mcp-re --tool <tool_name> [--args <args>] [--file <file>] [--workspace <dir>] [--config <path>]
```

### Tools Available

| Tool | Category | Description |
|------|----------|-------------|
| file | file_tools | Determine file type |
| strings | file_tools | Extract printable strings |
| hexdump | file_tools | Hexadecimal dump |
| xxd | file_tools | Hexadecimal dump |
| objdump | binary_tools | Disassemble binary |
| readelf | binary_tools | Read ELF headers |
| ldd | binary_tools | List dynamic dependencies |
| strace | binary_tools | System call trace |
| ltrace | binary_tools | Library call trace |
| upx | binary_tools | UPX packer/unpacker |
| gdb | binary_tools | GNU Debugger |
| radare2 | binary_tools | Radare2 framework |
| angr | binary_tools | Symbolic execution |
| ghidra | binary_tools | Ghidra decompiler |
| frida | binary_tools | Dynamic instrumentation |
| fq | binary_tools | jq for binary formats |
| binwalk | firmware_tools | Firmware analysis |
| unsquashfs | firmware_tools | Extract squashfs |
| sasquatch | firmware_tools | Squashfs extractor |
| jefferson | firmware_tools | JFFS2 extractor |
| ubi_reader | firmware_tools | UBI reader |
| unpackers | firmware_tools | Auto unpacker detection |
| retdc | firmware_tools |firmware decryption |
| qemu | firmware_tools | QEMU emulation |
| curl | network_tools | HTTP client |
| wget | network_tools | HTTP downloader |

## Data Formats

- Configuration: YAML (tools_config.yaml)
- Tool output: Plain text string
- Documentation: Dictionary with keys: description, usage, examples

## Edge Cases

1. **File not found**: Raises FileNotFoundError with descriptive message
2. **Tool not enabled in config**: Raises ValueError listing available tools
3. **Invalid arguments**: Basic validation strips potentially dangerous args
4. **Tool timeout**: Executor terminates process after timeout
5. **Large output**: Truncated to 100 lines with message
6. **Empty workspace**: Created automatically if doesn't exist
7. **Invalid config file**: Raises error with details

## Performance & Constraints

- Default timeout: 30 seconds per tool
- Output truncation: 100 lines max
- Sandbox: Filesystem jail to workspace directory
- Resource limits: Via Python's resource module (if available)
- No external network access beyond wget/curl tools
- Memory and CPU limits configurable

## Core Subsystems

```
src/mcp_reverse_engineering/
├── __init__.py          # Exports version + public API
├── __main__.py         # CLI entry point
├── py.typed           # Type hints marker
├── cli.py              # CLI layer
├── core/              # Core domain logic
│   ├── __init__.py
│   ├── config.py       # Config loading
│   └── engine.py      # Main engine
├── tools/             # Tool implementations
│   ├── __init__.py
│   ├── base.py       # Base tool class
│   ├── file_tools.py
│   ├── binary_tools.py
│   ├── firmware_tools.py
│   └── network_tools.py
├── sandbox/          # Execution sandbox
│   ├── __init__.py
│   └── execution.py
└── knowledge_base/    # Documentation
    ├── __init__.py
    └── documentation.py
```