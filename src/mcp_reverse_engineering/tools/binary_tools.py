"""Binary analysis tools for MCP Reverse Engineering Tool."""

from ..sandbox.execution import SandboxedExecutor
from .base import BaseTool


class BinaryTools(BaseTool):
    """Binary analysis tools."""

    def __init__(self, executor: SandboxedExecutor) -> None:
        self.executor = executor

    def objdump(self, args: list[str]) -> str:
        """Run the objdump command."""
        return self.executor.execute(["objdump"] + args)

    def readelf(self, args: list[str]) -> str:
        """Run the readelf command."""
        return self.executor.execute(["readelf"] + args)

    def ldd(self, args: list[str]) -> str:
        """Run the ldd command."""
        return self.executor.execute(["ldd"] + args)

    def strace(self, args: list[str]) -> str:
        """Run the strace command."""
        return self.executor.execute(["strace"] + args)

    def ltrace(self, args: list[str]) -> str:
        """Run the ltrace command."""
        return self.executor.execute(["ltrace"] + args)

    def upx(self, args: list[str]) -> str:
        """Run the upx command."""
        return self.executor.execute(["upx"] + args)

    def gdb(self, args: list[str]) -> str:
        """Run GDB in batch mode."""
        # Add batch mode and quiet flags for non-interactive use
        gdb_args = ["-batch", "-quiet"] + args
        return self.executor.execute(["gdb"] + gdb_args)

    def radare2(self, args: list[str]) -> str:
        """Run radare2 commands."""
        # Add -q for quiet mode
        r2_args = ["-q"] + args
        return self.executor.execute(["radare2"] + r2_args)

    def angr(self, args: list[str]) -> str:
        """Run angr for symbolic execution."""
        # This would typically involve running a Python script
        # For simplicity, we'll assume angr is invoked via a script
        return self.executor.execute(
            [
                "python",
                "-c",
                f"import angr; print('Angr execution would happen here with args: {args}')",
            ]
        )

    def ghidra(self, args: list[str]) -> str:
        """Run Ghidra in headless mode."""
        # This assumes ghidra_run is in PATH
        return self.executor.execute(["ghidra_run"] + args)

    def frida(self, args: list[str]) -> str:
        """Run Frida tools."""
        # Frida is typically used via frida-trace, frida-discover, etc.
        # For simplicity, we'll just run frida with args
        return self.executor.execute(["frida"] + args)

    def fq(self, args: list[str]) -> str:
        """Run fq - jq for binary formats."""
        # fq is a jq-like query tool for binary data
        # Supports various formats like ELF, PE, ZIP, etc.
        return self.executor.execute(["fq"] + args)
