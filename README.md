# Context Packer - The Webpack for AI Context

[![PyPI version](https://badge.fury.io/py/context-packer.svg)](https://badge.fury.io/py/context-packer)
[![Python Support](https://img.shields.io/pypi/pyversions/context-packer.svg)](https://pypi.org/project/context-packer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/MarkShawn2020/context-packer.svg)](https://github.com/MarkShawn2020/context-packer/stargazers)

> 🎯 **One file, full context** - Package your entire project into a single markdown file optimized for LLMs and documentation.

## 🌟 Why Context Packer?

In the age of AI-powered development, we face a critical challenge: **Large Language Models need complete project context**, but sharing multiple files is cumbersome and inefficient. 

Just as **webpack** revolutionized JavaScript bundling and **esbuild** transformed build speeds, **Context Packer** transforms how we share code with AI models and documentation systems.

### The Problem
- 📁 **LLMs work best with single-file contexts** - No need to manage multiple uploads
- 🔄 **Modern documentation systems** (like Next.js) support single-file downloads for offline viewing
- 🤖 **AI code reviews** require complete project understanding in one shot
- 📚 **Knowledge sharing** becomes complex with scattered files

### The Solution
Context Packer intelligently bundles your entire project into a **single, AI-optimized markdown file** - complete with structure visualization, smart filtering, and symlink support for complex project organization.

## ✨ Key Features

- **🔗 Advanced Symlink Support**: Organize complex projects with symbolic links - perfect for selective file inclusion
- **🎯 AI-Optimized Output**: Formatted specifically for LLM consumption with clear structure and syntax highlighting
- **📊 Smart Filtering**: Automatically excludes build artifacts, dependencies, and binary files
- **🌳 Visual Project Tree**: Instant understanding of project structure with status indicators
- **⚡ Lightning Fast**: Efficient processing even for large codebases
- **🔧 Highly Configurable**: Fine-tune output with extensive options

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install context-packer

# Using uv (10-100x faster)
uv pip install context-packer

# Using pipx (isolated environment)
pipx install context-packer
```

### Basic Usage

```bash
# Pack current directory
ctxpack .

# Pack specific project
ctxpack /path/to/project -o project_context.md

# Pack with custom settings
ctxpack . --max-size 20 --ignore "*.test.js" "docs/*"
```

## 🎨 Advanced: The Symlink Workflow

Context Packer's **symlink support** enables a powerful workflow for complex projects where you need fine-grained control over what gets packed.

### Scenario: Selective Project Packing

Instead of using complex ignore patterns, create a "packing directory" with symlinks to exactly what you need:

```bash
# Create a packing directory
mkdir my-project-pack
cd my-project-pack

# Symlink specific files and directories
ln -s ../src/core core
ln -s ../src/utils/helpers.js helpers.js
ln -s ../config config
ln -s ../package.json package.json
ln -s ../README.md README.md

# Pack only what you've selected
ctxpack . -o ../my-project-context.md
```

### Real-World Example: Multi-Module Project

```bash
# You have a monorepo with multiple packages
project/
├── packages/
│   ├── frontend/     # React app
│   ├── backend/      # Node.js API  
│   ├── shared/       # Shared utilities
│   └── mobile/       # React Native app

# Create a context for AI review of web platform only
mkdir web-platform-context
cd web-platform-context

# Link only web-related packages
ln -s ../packages/frontend frontend
ln -s ../packages/backend backend  
ln -s ../packages/shared shared
ln -s ../docker-compose.yml docker-compose.yml
ln -s ../.env.example .env.example

# Generate context
ctxpack . -o web-platform.md --follow-symlinks
```

This approach gives you **surgical precision** in creating contexts for different purposes:
- 🎯 **Code Review Context**: Only the files changed in a PR
- 🏗️ **Architecture Context**: High-level structure without implementation details  
- 🐛 **Debug Context**: Specific module with its dependencies
- 📖 **Documentation Context**: README files and examples only

## 📋 Output Format

Context Packer generates a structured markdown file with:

### 1. Project Structure Visualization
```
MyProject
├── src/
│   ├── index.js ✅      # High-priority file
│   ├── utils/ 🔗📁      # Symlinked directory
│   │   └── helper.js ☑️  # Included file
│   └── tests/ ⏭️        # Ignored directory
├── package.json ✅      # Configuration file
└── README.md ✅         # Documentation
```

### 2. Status Indicators
- ✅ High-priority files (configs, README)
- ☑️ Source code files
- 🔗 Symbolic links
- 🔗📁 Symlinked directories  
- ⚠️ Circular reference detected
- 📊 Large files (truncated)
- ⏭️ Ignored files

### 3. Complete File Contents
Each file is presented with:
- Relative path
- Syntax highlighting
- Smart truncation for large files
- Clear section separators

## 🎯 Perfect For

### 🤖 AI Development
```bash
# Prepare context for AI analysis
ctxpack . -o for_claude.md --max-size 30

# Get AI to review your architecture
ctxpack src/ -o architecture_review.md --max-depth 2
```

### 📚 Documentation
```bash
# Create offline documentation bundle
ctxpack docs/ -o documentation.md --ignore "*.png" "*.jpg"
```

### 🔍 Code Review
```bash
# Package PR changes for review
ctxpack . -o pr_context.md --ignore "node_modules" "*.test.*"
```

### 🎓 Learning & Teaching
```bash
# Create educational material
ctxpack examples/ -o tutorial_code.md --max-files 20
```

## 🛠️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `project_path` | Directory to pack | Required |
| `-o, --output` | Output file path | `{project}_context_{timestamp}.md` |
| `--ignore` | Additional ignore patterns | None |
| `--max-size` | Maximum total size (MB) | 10 |
| `--max-files` | Maximum number of files | 100 |
| `-L, --max-depth` | Maximum directory depth | Unlimited |
| `--follow-symlinks` | Follow symbolic links | Yes |
| `--no-follow-symlinks` | Don't follow symbolic links | No |
| `-v, --verbose` | Show detailed progress | No |

## ⚡ Performance Tips

1. **Large Codebases**: Use `--verbose` to monitor progress
2. **Selective Packing**: Use symlinks for precise control
3. **Size Management**: Adjust `--max-size` based on LLM limits
4. **Speed Optimization**: Use `--max-depth` to limit traversal

## 🔒 Security & Best Practices

- **Automatic Exclusions**: `.env`, `.git`, `node_modules` are ignored by default
- **Gitignore Respect**: Honors your `.gitignore` patterns
- **Size Limits**: Prevents accidental huge outputs
- **Review Before Sharing**: Always check output before sending to third parties

## 🧑‍💻 Development

### Setting up with UV (Recommended)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/MarkShawn2020/context-packer.git
cd context-packer

# Install in development mode
uv pip install -e .
uv pip install -r requirements-dev.txt

# Run tests
uv run pytest
```

### Quick Commands
```bash
make test      # Run tests
make lint      # Check code quality
make format    # Format code
make build     # Build package
make publish   # Publish to PyPI
```

## 📦 Publishing

With PyPI token configured:

```bash
# One-command publish (with version bump)
make release VERSION=patch  # or minor, major

# Or manual steps
python bump_version.py patch
git commit -am "Bump version"
git tag v1.2.3
git push --tags
make publish
```

## 🌍 Ecosystem

Context Packer is part of the modern AI development workflow:

- **Use with Claude, GPT-4, Gemini** for code analysis
- **Integrate with CI/CD** for automatic documentation
- **Combine with AI editors** like Cursor, Windsurf
- **Works with documentation systems** like Docusaurus, Next.js

## 🤝 Contributing

We welcome contributions! Context Packer is designed to be the definitive solution for project context packaging.

### Ideas for Contribution
- 🎨 GUI interface (planned)
- 🔌 Plugin system for custom processors
- 🌐 Web service API
- 📊 Context analytics
- 🔄 Incremental packing

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Created by [MarkShawn2020](https://github.com/MarkShawn2020) to solve the real-world challenge of sharing complete project context with AI models. Inspired by the elegance of webpack and the speed of esbuild, Context Packer brings the same innovation to AI-assisted development.

---

<div align="center">

**🚀 Transform how you share code with AI**

[Documentation](https://github.com/MarkShawn2020/context-packer#readme) • 
[Issues](https://github.com/MarkShawn2020/context-packer/issues) • 
[PyPI](https://pypi.org/project/context-packer/) • 
[Releases](https://github.com/MarkShawn2020/context-packer/releases)

</div>