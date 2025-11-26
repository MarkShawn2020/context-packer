# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Context Packer is a Python CLI tool that packages project directories into a single markdown file optimized for LLM consumption. Single-file architecture: all core logic in `context_packer.py`.

## Commands

```bash
# Development install
uv pip install -e .
uv pip install -r requirements-dev.txt

# Run tests
make test                          # Quick test
pytest tests/                      # Full pytest

# Code quality
make lint                          # ruff + mypy
make format                        # black + ruff --fix

# Build & Release
make build                         # Build package
make release                       # patch release (test + format + version bump + tag + push + publish)
make release VERSION=minor         # minor release
python release.py [patch|minor|major]  # Alternative
```

## Architecture

`ContextPacker` class handles:
- File collection with symlink support and circular reference detection
- gitignore parsing + built-in ignore patterns (node_modules, .git, binaries, etc.)
- Text file detection via extension whitelist + MIME type fallback
- Priority-based file sorting (README/configs > code > docs)
- Markdown generation with file tree visualization and status indicators

Key methods:
- `collect_files_recursive()` - Walks directories following symlinks
- `get_file_tree()` - Generates tree with status symbols (✅☑️🔗⏭️💾📊)
- `pack_project()` - Main entry point

CLI entry points: `ctxpack` and `context-packer` (defined in pyproject.toml)
