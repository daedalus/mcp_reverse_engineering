# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for `fq` - jq for binary formats

### Changed
- Updated documentation for tool categories
- README now lists all available tools

## [0.1.0] - 2026-03-20

### Added
- Initial release
- Sandboxed execution with filesystem jail and timeouts
- Unified interface to multiple reverse engineering tools
- Configurable tool loading via YAML
- Tool categories: File Analysis, Binary Analysis, Firmware Analysis, Network Tools
- Argument validation and output truncation
- Built-in tool documentation
- MCP-compatible tool schemas
- CLI entry point
- Test suite with pytest

[0.1.0]: https://github.com/daedalus/mcp_reverse_engineering/releases/tag/v0.1.0