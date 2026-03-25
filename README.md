# Reverse Engineering Tools MCP Server

mcp-name: io.github.daedalus/mcp_reverse_engineering

A sandboxed MCP (Managed Computation Platform) tool for reverse engineering that provides a unified interface to various reverse engineering tools with security restrictions.

## Features

- **Sandboxed Execution**: All tools run in a restricted environment with timeouts, memory limits, and filesystem jail
- **Unified Interface**: Single interface to access multiple reverse engineering tools
- **Configurable Tool Loading**: Select which tools to enable via YAML configuration to avoid overwhelming LLM context windows
- **Tool Categories**:
  - File Analysis: `file`, `strings`, `hexdump`, `xxd`
  - Binary Analysis: `objdump`, `readelf`, `ldd`, `strace`, `ltrace`, `upx`, `gdb`, `radare2`, `angr`, `ghidra`, `frida`
  - Firmware Analysis: `binwalk`, `unsquashfs`, `sasquatch`, `jefferson`, `ubi_reader`, `unpackers`, `retdc`, `qemu`
  - Network Tools: `curl`, `wget`
- **Advanced Capabilities**:
  - Radare2 AST queries
  - Angry symbolic execution
  - Ghidra headless decompilation
  - Automatic unpacker detection
  - Firmware filesystem detection
  - Auto QEMU emulation
- **Safety Features**:
  - Argument validation
  - Execution sandbox with resource limits
  - File workspace jail
  - Tool output truncation
- **Knowledge Base**: Built-in documentation for all tools
- **Testing**: Unit and functional tests included

## Installation

### Local Installation

```bash
pip install -e .
```

### Docker

Build and run with Docker:

```bash
# Build the image
docker build -t mcp-reverse-engineering .

# Run with docker-compose
docker-compose up -d

# Or run directly with volume mount
docker run -v $(pwd)/workspace:/workspace mcp-reverse-engineering --tool strings --args "-n 10" --file ./binary.exe
```

The container runs with security hardening:
- Read-only filesystem
- No new privileges
- Dropped capabilities
- Tmpfs for temporary files

### Remote Access via SSE

For remote MCP access, the container can be configured to serve over HTTP/SSE:

```bash
# With custom port mapping
docker-compose up -d
```

## Configuration

Tools are configured via YAML files to control which tools are loaded. This prevents overwhelming LLM context windows by enabling only the tools you need.

**Default config** (`tools_config.yaml`): All tools disabled

**Example configs**:
- `examples/minimal.yaml` - Only file analysis tools (3 tools)
- `examples/firmware.yaml` - File + Binary + Firmware analysis
- `examples/full.yaml` - All 25 tools enabled

```yaml
# Enable specific tool categories
settings:
  default_timeout: 300

categories:
  file_analysis:
    enabled: true
    tools:
      - file
      - strings
      - hexdump
```

## Usage

```bash
# Using the CLI with default config
mcp-re --tool strings --args "-n 10" --file ./binary.exe

# Using a specific config
mcp-re --config examples/minimal.yaml --tool strings --args [] --file ./binary.exe
```

**Programmatic usage:**
```python
from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine

# Load with default config (no tools enabled)
engine = ReverseEngineeringEngine()

# Load with specific config
engine = ReverseEngineeringEngine(config_path="examples/minimal.yaml")

# List enabled tools
print(engine.list_available_tools())

# Get MCP-compatible tool schemas
print(engine.get_mcp_tools())

# Execute a tool
result = engine.execute_tool("strings", ["-n", "10"], "./binary.exe")
print(result)
```

## Available Tools

Run `mcp-re --tool help` to see all available tools, or check the knowledge base in the source code.

## Security

The tool employs multiple layers of security:
1. Filesystem jail - all operations confined to workspace directory
2. Process resource limits - CPU, memory, process count, file size restrictions
3. Timeout enforcement - prevents hanging operations
4. Argument validation - basic sanitization of inputs
5. Output truncation - prevents excessive data exposure

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

## Requirements

See `requirements.txt` for Python dependencies.

Note: The actual reverse engineering tools (binwalk, radare2, etc.) must be installed separately on the system.

## License

MIT
