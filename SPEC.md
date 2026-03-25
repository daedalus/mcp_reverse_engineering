# SPEC.md — MCP Reverse Engineering Tool

## Purpose

A sandboxed MCP (Managed Computation Platform) tool for reverse engineering that provides a unified interface to various reverse engineering tools with security restrictions. It enables safe execution of binary analysis, firmware analysis, and file analysis tools within a controlled environment.

## Scope

### What IS in scope
- Sandboxed execution of reverse engineering tools with resource limits
- Unified Python API for multiple RE tools (file, strings, hexdump, xxd, objdump, readelf, ldd, strace, ltrace, upx, gdb, radare2, angr, ghidra, frida, binwalk, unsquashfs, sasquatch, jefferson, ubi_reader, unpackers, retdc, qemu, curl, wget)
- Configurable tool loading via YAML to control LLM context usage
- Workspace jail for filesystem operations
- MCP-compatible tool schemas for integration
- CLI interface for direct tool execution
- Comprehensive documentation for all tools
- Docker container support for remote deployment and execution

### What is NOT in scope
- Actual installation of external RE tools (binwalk, radare2, etc.)
- Full decompilation output handling (beyond what tools provide)
- Binary patching or modification capabilities
- GUI or interactive RE sessions

## Public API / Interface

### `ReverseEngineeringEngine` class
- `__init__(workspace: str = "./workspace", timeout: int = 30, config_path: str | Path | None = None)` - Initialize engine
- `execute_tool(tool_name: str, args: list[str], file_path: str | None = None) -> str` - Execute a tool
- `list_available_tools() -> list[str]` - List enabled tools
- `get_tool_documentation(tool_name: str) -> dict[str, Any]` - Get tool docs
- `get_mcp_tools() -> list[dict[str, Any]]` - Get MCP-compatible schemas

### `SandboxedExecutor` class
- `execute(command: list[str]) -> str` - Execute command in sandbox
- Properties: `timeout`, `workspace`

### CLI
- `mcp-re --tool <name> --args <args> --file <path> --config <yaml> --workspace <dir>`

## Data Formats

- Configuration: YAML files with tool enablement settings
- Tool output: Raw string output from subprocess
- MCP schemas: JSON-compatible dict structures

## Edge Cases

1. **Tool not enabled**: Raises `ValueError` with message "Unknown tool: {tool_name}"
2. **File not found**: Raises `FileNotFoundError`
3. **Execution timeout**: Output includes "timed out" message
4. **Invalid arguments**: Basic validation prevents directory traversal (`..`)
5. **Empty workspace**: Creates directory automatically on init
6. **Long output**: Truncates at 100 lines with summary message
7. **Missing tool binary**: Propagates subprocess error
8. **Config file not found**: Uses default (all tools disabled)

## Performance & Constraints

- O(n) where n is number of enabled tools at init time
- Memory: Limited by subprocess constraints and output truncation
- No external network access except via curl/wget with sandboxing
- Python 3.11+ required
- Dependencies: psutil, pyyaml, requests (no RE tool binaries bundled)
