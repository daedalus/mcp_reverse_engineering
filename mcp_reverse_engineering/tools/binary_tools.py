"""Binary analysis tools for MCP Reverse Engineering Tool."""

from .base import BaseTool
from ..sandbox.execution import SandboxedExecutor
from typing import List
import json


class BinaryTools(BaseTool):
    """Binary analysis tools."""

    def __init__(self, executor: SandboxedExecutor):
        self.executor = executor

    def objdump(self, args: List[str]) -> str:
        """Run the objdump command."""
        return self.executor.execute(["objdump"] + args)

    def readelf(self, args: List[str]) -> str:
        """Run the readelf command."""
        return self.executor.execute(["readelf"] + args)

    def ldd(self, args: List[str]) -> str:
        """Run the ldd command."""
        return self.executor.execute(["ldd"] + args)

    def strace(self, args: List[str]) -> str:
        """Run the strace command."""
        return self.executor.execute(["strace"] + args)

    def ltrace(self, args: List[str]) -> str:
        """Run the ltrace command."""
        return self.executor.execute(["ltrace"] + args)

    def upx(self, args: List[str]) -> str:
        """Run the upx command."""
        return self.executor.execute(["upx"] + args)

    def gdb(self, args: List[str]) -> str:
        """Run GDB in batch mode."""
        # Add batch mode and quiet flags for non-interactive use
        gdb_args = ["-batch", "-quiet"] + args
        return self.executor.execute(["gdb"] + gdb_args)

    def radare2(self, args: List[str]) -> str:
        """Run radare2 commands."""
        # Add -q for quiet mode
        r2_args = ["-q"] + args
        return self.executor.execute(["radare2"] + r2_args)

    def angr(self, args: List[str]) -> str:
        """Run angr for symbolic execution."""
        # This would typically involve running a Python script
        # For simplicity, we'll assume angr is invoked via a script
        return self.executor.execute(["python", "-c", f"import angr; print('Angr execution would happen here with args: {args}')"])

    def ghidra(self, args: List[str]) -> str:
        """Run Ghidra in headless mode."""
        # This assumes ghidra_run is in PATH
        return self.executor.execute(["ghidra_run"] + args)

    def frida(self, args: List[str]) -> str:
        """Run Frida tools."""
        # Frida is typically used via frida-trace, frida-discover, etc.
        # For simplicity, we'll just run frida with args
        return self.executor.execute(["frida"] + args)