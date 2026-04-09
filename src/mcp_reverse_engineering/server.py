"""MCP Server for Reverse Engineering Tool.

This module provides an MCP (Model Context Protocol) server interface
for the reverse engineering tool. It exposes various reverse engineering
tools as MCP tools that can be used by Claude Desktop or other MCP clients.

The server uses FastMCP to provide a stdio-based transport for integration
with Claude Desktop's MCP protocol.
"""


from fastmcp import FastMCP

from mcp_reverse_engineering.core.engine import ReverseEngineeringEngine

mcp = FastMCP("mcp-reverse-engineering")

_engine: ReverseEngineeringEngine | None = None


def get_engine() -> ReverseEngineeringEngine:
    """Get or create the ReverseEngineeringEngine singleton.

    This function maintains a singleton instance of the engine to avoid
    recreating it on each tool call, which would be inefficient.

    Returns:
        ReverseEngineeringEngine: The singleton engine instance.

    Example:
        >>> engine = get_engine()
        >>> engine.list_available_tools()
        ['strings', 'hexdump', 'objdump', ...]
    """
    global _engine
    if _engine is None:
        _engine = ReverseEngineeringEngine()
    return _engine


@mcp.tool()
def strings(args: list[str], file: str | None = None) -> str:
    """Run the strings command on a binary file to extract printable strings.

    The strings utility searches for printable strings in a binary file
    and outputs them. This is useful for extracting embedded strings,
    URLs, function names, and other text from compiled binaries.

    Args:
        args: Additional arguments to pass to the strings command.
            Common options include:
            - -n MIN: Only print strings of length MIN or greater
            - -t FORMAT: Select output format (d, o, x)
        file: Optional path to the file to analyze. If not provided,
            the file must be specified in args.

    Returns:
        str: The extracted strings from the file, or error message
            if the operation fails.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If the strings command fails to execute.

    Example:
        >>> strings(["-n", "8"], "/path/to/binary")
        "/lib64/ld-linux-x86-64.so.2\\nlibc.so.6\\n..."
    """
    engine = get_engine()
    return engine.execute_tool("strings", args, file)


@mcp.tool()
def hexdump(args: list[str], file: str | None = None) -> str:
    """Run hexdump on a file to display its contents in hexadecimal format.

    The hexdump utility displays the contents of a file in hex and ASCII,
    useful for analyzing binary file formats, identifying file headers,
    and inspecting raw file contents.

    Args:
        args: Additional arguments to pass to hexdump.
            Common options include:
            - -C: Canonical hex+ASCII output
            - -s OFFSET: Skip offset bytes from start
            - -n LENGTH: Only dump length bytes
        file: Optional path to the file to analyze.

    Returns:
        str: The hexadecimal dump of the file contents.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If hexdump fails to execute.

    Example:
        >>> hexdump(["-C"], "/path/to/binary")
        "00000000  7f 45 4c 46 02 01 01 00  ..."
    """
    engine = get_engine()
    return engine.execute_tool("hexdump", args, file)


@mcp.tool()
def xxd(args: list[str], file: str | None = None) -> str:
    """Run xxd on a file to create a hex dump.

    The xxd utility creates a hexadecimal representation of a file,
    similar to hexdump but with additional features like reverse
    conversion (hex to binary).

    Args:
        args: Additional arguments to pass to xxd.
            Common options include:
            - -r: Reverse operation (hex to binary)
            - -p: Plain hex dump format
            - -s OFFSET: Skip offset bytes
            - -l LENGTH: Limit output to length bytes
        file: Optional path to the file to analyze.

    Returns:
        str: The hex dump of the file contents.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If xxd fails to execute.

    Example:
        >>> xxd(["-l", "16"], "/path/to/binary")
        "00000000: 7f45 4c46 0201 0100 0200 3e00  ........"
    """
    engine = get_engine()
    return engine.execute_tool("xxd", args, file)


@mcp.tool()
def file_cmd(args: list[str], file: str | None = None) -> str:
    """Run the file command to determine file type.

    The file command performs a series of tests to identify the type
    of a file. It can detect file formats like ELF, PE, archives,
    images, and many others based on magic bytes and file structure.

    Args:
        args: Additional arguments to pass to file command.
            Common options include:
            - -b: Brief output (don't show filename)
            - -z: Try to detect compressed files
            - -i: Output MIME type instead of human-readable
        file: Optional path to the file to analyze.

    Returns:
        str: Description of the file type.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If file command fails to execute.

    Example:
        >>> file_cmd([], "/path/to/binary")
        "/path/to/binary: ELF 64-bit LSB executable, x86-64..."
    """
    engine = get_engine()
    return engine.execute_tool("file", args, file)


@mcp.tool()
def objdump(args: list[str], file: str | None = None) -> str:
    """Run objdump to disassemble and analyze binary files.

    The objdump utility displays information about object files,
    including disassembly, symbol tables, section headers, and
    relocation information. Essential for reverse engineering
    and analyzing compiled binaries.

    Args:
        args: Additional arguments to pass to objdump.
            Common options include:
            - -d: Disassemble executable sections
            - -t: Display symbol table
            - -h: Display section headers
            - -x: Display all available headers
            - -s: Display full contents of sections
        file: Optional path to the binary file to analyze.

    Returns:
        str: The objdump output containing disassembly and/or
            file information.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If objdump fails to execute.

    Example:
        >>> objdump(["-d"], "/path/to/binary")
        "Disassembly of section .text:\\n0000000000401000 <_start>:\\n..."
    """
    engine = get_engine()
    return engine.execute_tool("objdump", args, file)


@mcp.tool()
def readelf(args: list[str], file: str | None = None) -> str:
    """Run readelf to display ELF binary information.

    The readelf utility displays information about ELF (Executable
    and Linkable Format) files, including headers, sections, symbols,
    dynamic linking information, and more. Specific to Linux/Unix
    ELF binaries.

    Args:
        args: Additional arguments to pass to readelf.
            Common options include:
            - -h: Display ELF file header
            - -S: Display section headers
            - -s: Display symbol table
            - -d: Display dynamic section
            - -l: Display program headers
            - -r: Display relocations
        file: Optional path to the ELF file to analyze.

    Returns:
        str: The readelf output with ELF file information.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If readelf fails to execute.

    Example:
        >>> readelf(["-h"], "/path/to/elf")
        "ELF Header:\\n  Magic:   7f 45 4c 46 02 01 01 00 ..."
    """
    engine = get_engine()
    return engine.execute_tool("readelf", args, file)


@mcp.tool()
def binwalk(args: list[str], file: str | None = None) -> str:
    """Run binwalk to find embedded files and code in a binary.

    Binwalk is a tool for analyzing binary files to find embedded
    files and executable code. It uses entropy analysis and signature
    matching to identify compressed data, file systems, archives,
    and other embedded content.

    Args:
        args: Additional arguments to pass to binwalk.
            Common options include:
            - -e: Extract found files automatically
            - -M: Enable signature matching
            - -B: Scan for common file signatures
            - -Y: Entropy analysis mode
            - -q: Quiet output (suppress banners)
        file: Optional path to the file to analyze.

    Returns:
        str: Analysis results showing identified signatures,
            entropy graph, and potential embedded content.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If binwalk fails to execute.

    Example:
        >>> binwalk(["-B"], "/path/to/firmware.bin")
        "DECIMAL       HEXADECIMAL     DESCRIPTION\\n---------------------------------------------\\n
        0             0x0             Linux kernel..."
    """
    engine = get_engine()
    return engine.execute_tool("binwalk", args, file)


@mcp.tool()
def list_tools() -> list[str]:
    """List all available reverse engineering tools.

    This function returns a list of all tools that are currently
    enabled in the configuration and available for use through
    the MCP server.

    Returns:
        List[str]: List of available tool names.

    Example:
        >>> list_tools()
        ['strings', 'hexdump', 'objdump', 'readelf', 'binwalk']
    """
    engine = get_engine()
    return engine.list_available_tools()


if __name__ == "__main__":
    mcp.run()
