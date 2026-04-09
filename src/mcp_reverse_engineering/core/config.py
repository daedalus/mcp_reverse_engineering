"""Tool configuration loader for MCP Reverse Engineering."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ToolSettings:
    timeout: int = 300
    enabled: bool = True
    default_args: list[str] = field(default_factory=list)


@dataclass
class CategoryConfig:
    name: str
    enabled: bool
    tools: list[str]


@dataclass
class ToolConfig:
    settings: dict[str, ToolSettings] = field(default_factory=dict)
    categories: list[CategoryConfig] = field(default_factory=list)
    default_timeout: int = 300
    sandbox_enabled: bool = True
    log_level: str = "INFO"
    _enabled_tools: set[str] = field(default_factory=set, init=False)

    def is_tool_enabled(self, tool_name: str) -> bool:
        return tool_name in self._enabled_tools

    def get_tool_settings(self, tool_name: str) -> ToolSettings:
        return self.settings.get(tool_name, ToolSettings())

    def list_enabled_tools(self) -> list[str]:
        return sorted(self._enabled_tools)


def load_config(config_path: str | Path | None = None) -> ToolConfig:
    if config_path is None:
        # Check project root (four levels up from core/config.py: core -> package -> src -> project)
        project_root = Path(__file__).parent.parent.parent.parent
        config_path = project_root / "tools_config.yaml"
        if not config_path.exists():
            return _default_config()

    config_path = Path(config_path)

    if not config_path.exists():
        return _default_config()

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if not data:
        return _default_config()

    global_settings = data.get("settings", {})
    categories_data = data.get("categories", {})
    tools_overrides = data.get("tools", {})

    config = ToolConfig(
        default_timeout=global_settings.get("default_timeout", 300),
        sandbox_enabled=global_settings.get("sandbox_enabled", True),
        log_level=global_settings.get("log_level", "INFO"),
    )

    enabled_tools = set()

    for category_name, category_data in categories_data.items():
        if not category_data.get("enabled", False):
            continue

        category_tools = category_data.get("tools", [])
        config.categories.append(
            CategoryConfig(
                name=category_name,
                enabled=True,
                tools=category_tools,
            )
        )
        enabled_tools.update(category_tools)

    for tool_name, tool_override in (tools_overrides or {}).items():
        settings = ToolSettings(
            timeout=tool_override.get("timeout", config.default_timeout),
            enabled=tool_override.get("enabled", True),
            default_args=tool_override.get("args", {}).get("default_args", []),
        )
        config.settings[tool_name] = settings

        if tool_override.get("enabled", True):
            enabled_tools.add(tool_name)
        else:
            enabled_tools.discard(tool_name)

    config._enabled_tools = enabled_tools
    return config


def _default_config() -> ToolConfig:
    config = ToolConfig()
    config._enabled_tools = set()
    return config
