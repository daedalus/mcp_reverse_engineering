"""Binary analysis tools for MCP Reverse Engineering Tool."""

from mcp_reverse_engineering.sandbox.execution import SandboxedExecutor
from mcp_reverse_engineering.tools.base import BaseTool


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
        gdb_args = ["-batch", "-quiet"] + args
        return self.executor.execute(["gdb"] + gdb_args)

    def radare2(self, args: list[str]) -> str:
        """Run radare2 commands."""
        r2_args = ["-q"] + args
        return self.executor.execute(["radare2"] + r2_args)

    def angr(self, args: list[str]) -> str:
        """Run angr for symbolic execution."""
        return self.executor.execute(
            [
                "python",
                "-c",
                f"import angr; print('Angr execution would happen here with args: {args}')",
            ]
        )

    def ghidra(self, args: list[str]) -> str:
        """Run Ghidra in headless mode."""
        return self.executor.execute(["ghidra_run"] + args)

    def frida(self, args: list[str]) -> str:
        """Run Frida tools."""
        return self.executor.execute(["frida"] + args)
