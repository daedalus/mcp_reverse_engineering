"""Documentation knowledge base for MCP Reverse Engineering Tool."""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ToolDocumentation:
    """Knowledge base for tool documentation and usage examples."""

    def __init__(self):
        self.docs: Dict[str, Any] = {}
        self._load_documentation()

    def _load_documentation(self) -> None:
        """Load tool documentation from YAML files."""
        # In a real implementation, this would load from files
        # For now, we'll hardcode some basic documentation
        self.docs = {
            "file": {
                "description": "Determine file type",
                "usage": "file [options] file",
                "examples": [
                    "file binary.exe",
                    "file -b /bin/bash"
                ]
            },
            "strings": {
                "description": "Find printable strings in binary files",
                "usage": "strings [options] file",
                "examples": [
                    "strings -n 5 binary.exe",
                    "strings -t x malware.bin"
                ]
            },
            "hexdump": {
                "description": "Print hexadecimal and ASCII dump of files",
                "usage": "hexdump [options] file",
                "examples": [
                    "hexdump -C binary.exe | head -20",
                    "hexdump -b firmware.img"
                ]
            },
            "xxd": {
                "description": "Make a hexdump or do the reverse",
                "usage": "xxd [options] file",
                "examples": [
                    "xxd binary.exe",
                    "xxd -r hexdump.txt > binary.bin"
                ]
            },
            "objdump": {
                "description": "Display information from object files",
                "usage": "objdump [options] file",
                "examples": [
                    "objdump -d binary.exe",
                    "objdump -T library.so"
                ]
            },
            "readelf": {
                "description": "Display ELF file information",
                "usage": "readelf [options] file",
                "examples": [
                    "readelf -h binary.exe",
                    "readelf -S library.so"
                ]
            },
            "ldd": {
                "description": "Print shared library dependencies",
                "usage": "ldd [options] file",
                "examples": [
                    "ldd binary.exe",
                    "ldd /usr/bin/ssh"
                ]
            },
            "strace": {
                "description": "Trace system calls and signals",
                "usage": "strace [options] command",
                "examples": [
                    "strace -o trace.log ./binary",
                    "strace -f -e open ./binary"
                ]
            },
            "ltrace": {
                "description": "Trace library calls",
                "usage": "ltrace [options] command",
                "examples": [
                    "ltrace -o libtrace.log ./binary",
                    "ltrace -f -e malloc ./binary"
                ]
            },
            "upx": {
                "description": "Ultimate Packer for eXecutables",
                "usage": "upx [options] file",
                "examples": [
                    "upx -d packed.exe",
                    "upx --best --lzma binary.exe"
                ]
            },
            "gdb": {
                "description": "GNU Debugger",
                "usage": "gdb [options] file",
                "examples": [
                    "gdb -batch -ex 'info functions' binary.exe",
                    "gdb -q -ex 'break main' -ex 'run' -ex 'quit' ./binary"
                ]
            },
            "radare2": {
                "description": "Reverse engineering framework",
                "usage": "radare2 [options] file",
                "examples": [
                    "radare2 -qc 'izz' binary.exe",
                    "radare2 -qc 'pd 10@entry0' binary.exe"
                ]
            },
            "angr": {
                "description": "Symbolic execution engine",
                "usage": "angr [options] file",
                "examples": [
                    "angr -p binary.exe --find 0x401000 --avoid 0x402000",
                    "angr -d binary.exe"
                ]
            },
            "ghidra": {
                "description": "Software reverse engineering framework",
                "usage": "ghidra_run [options]",
                "examples": [
                    "ghidra_run -import binary.exe -processor X86:LE:32:default -postScript Decompile.java",
                    "ghidra_run -analysisTimeoutPerPass 300000"
                ]
            },
            "frida": {
                "description": "Dynamic instrumentation toolkit",
                "usage": "frida [options] target",
                "examples": [
                    "frida -U -f com.example.app -l hook.js --no-pause",
                    "frida-ps -Uai"
                ]
            },
            "binwalk": {
                "description": "Firmware analysis tool",
                "usage": "binwalk [options] file",
                "examples": [
                    "binwalk -e firmware.img",
                    "binwalk -A firmware.img"
                ]
            },
            "unsquashfs": {
                "description": "Extract Squashfs filesystem",
                "usage": "unsquashfs [options] file",
                "examples": [
                    "unsquashfs filesystem.squashfs",
                    "unsquashfs -d output_dir filesystem.squashfs"
                ]
            },
            "sasquatch": {
                "description": "Squashfs filesystem extractor/modifier",
                "usage": "sasquatch [options] file",
                "examples": [
                    "sasquatch -x filesystem.squashfs -d output_dir",
                    "sasquatch -i filesystem.squashfs -o modified.squashfs"
                ]
            },
            "jefferson": {
                "description": "JFFS2 filesystem extractor",
                "usage": "jefferson [options] file",
                "examples": [
                    "jefferson -i jffs2.img -o output_dir",
                    "jefferson -v jffs2.img"
                ]
            },
            "ubi_reader": {
                "description": "UBI filesystem reader",
                "usage": "ubi_reader [options] file",
                "examples": [
                    "ubi_reader ubi.img",
                    "ubi_reader -o output_dir ubi.img"
                ]
            },
            "retdc": {
                "description": "Return-oriented decompiler",
                "usage": "retdc [options] file",
                "examples": [
                    "retdc binary.exe",
                    "retdc -o decompiled.c binary.exe"
                ]
            },
            "curl": {
                "description": "Transfer data from or to a server",
                "usage": "curl [options] URL",
                "examples": [
                    "curl -O https://example.com/file.bin",
                    "curl -v -H 'User-Agent: Mozilla/5.0' https://example.com"
                ]
            },
            "wget": {
                "description": "Network downloader",
                "usage": "wget [options] URL",
                "examples": [
                    "wget https://example.com/file.bin",
                    "wget --limit-rate=100k https://example.com/largefile.iso"
                ]
            },
            "qemu": {
                "description": "Quick Emulator",
                "usage": "qemu-system-arch [options]",
                "examples": [
                    "qemu-system-arm -M versatilepb -kernel kernel.img -nographic",
                    "qemu-system-x86_64 -cdrom image.iso -boot d"
                ]
            }
        }

    def get_tool_docs(self, tool_name: str) -> Dict[str, Any]:
        """Get documentation for a specific tool."""
        return self.docs.get(tool_name, {})

    def list_documented_tools(self) -> list:
        """List all documented tools."""
        return list(self.docs.keys())