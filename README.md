# Context Packer

A powerful Python tool that intelligently packages project directories into a single markdown file, optimized for AI analysis and code review.

## ✨ Features

- **🔗 Symlink Support**: Recursively follows symbolic links with circular reference detection
- **🎯 Smart Filtering**: Automatically ignores build artifacts, dependencies, and system files
- **📊 Size Management**: Intelligent file prioritization and content truncation
- **🌳 Visual Tree**: Clear project structure visualization with status indicators
- **⚡ Performance**: Efficient handling of large codebases with progress tracking
- **🔧 Flexible Configuration**: Extensive customization options via command-line arguments

## 🚀 Quick Start

### Installation

```bash
# Clone and install globally
git clone <repository-url>
cd context-packer
pip install .

# Now use anywhere
context-packer /path/to/project
# or shorter alias
ctxpack /path/to/project
```

### Basic Usage

```bash
# Pack current directory
ctxpack .

# Pack with custom output
ctxpack /my/project -o project_analysis.md

# Pack with symlink following disabled
ctxpack . --no-follow-symlinks

# Verbose mode for large projects
ctxpack . --verbose
```

## 📖 Advanced Usage

### Symlink Handling

Context Packer now intelligently handles symbolic links:

```bash
# Follow symlinks (default behavior)
ctxpack /project/with/symlinks

# Disable symlink following
ctxpack /project/with/symlinks --no-follow-symlinks
```

**Features:**
- Automatically detects and prevents circular references
- Visual indicators: 🔗 for symlink files, 🔗📁 for symlink directories
- Safe recursion with visited path tracking

### Custom Ignore Patterns

```bash
# Ignore specific patterns
ctxpack . --ignore "*.log" "temp/*" "secrets.env"

# Combine with gitignore (automatic)
# .gitignore rules are automatically applied
```

### Size and Depth Control

```bash
# Limit file size and count
ctxpack . --max-size 20 --max-files 200

# Limit directory traversal depth
ctxpack . --max-depth 3

# Complete example
ctxpack ~/large-project \
  -o analysis.md \
  --max-size 15 \
  --max-depth 4 \
  --ignore "*.test.js" \
  --verbose
```

## 📋 Output Format

The generated markdown includes:

### 1. Project Structure
```
MyProject
├── src/
│   ├── main.py ✅
│   └── utils/ 🔗📁
│       └── helpers.py ☑️
├── README.md ✅
└── config.yml ✅
```

### 2. Status Indicators
- ✅ High priority files (README, package.json, config)
- ☑️ Medium priority files (source code)
- 🔗 Symbolic link files
- 🔗📁 Symbolic link directories
- ⚠️ Circular reference detected
- 📊 File too large (truncated)
- 💾 Binary file (skipped)

### 3. File Contents
Organized by priority with syntax highlighting:
```python
# main.py
def main():
    print("Hello, World!")
```

## 🛠️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `project_path` | Project directory to pack | Required |
| `-o, --output` | Output file path | `{project}_context_{timestamp}.md` |
| `--ignore` | Additional ignore patterns | None |
| `--max-size` | Maximum total size (MB) | 10 |
| `--max-files` | Maximum number of files | 100 |
| `-L, --max-depth` | Maximum directory depth | Unlimited |
| `--follow-symlinks` | Follow symbolic links | True |
| `--no-follow-symlinks` | Don't follow symbolic links | False |
| `-v, --verbose` | Show detailed progress | False |

## 🎯 Use Cases

### AI Code Analysis
Package your entire codebase for comprehensive AI review:
```bash
ctxpack . -o for_ai_review.md --max-size 30
```

### Documentation Generation
Create project overviews for documentation:
```bash
ctxpack . --max-depth 2 -o project_overview.md
```

### Code Sharing
Share project context without sending entire repositories:
```bash
ctxpack ./src --ignore "*.test.*" -o code_context.md
```

### Security Auditing
Prepare code for security review (exclude sensitive files):
```bash
ctxpack . --ignore ".env*" "*secret*" "*.key" -o security_review.md
```

## ⚡ Performance Tips

1. **Large Projects**: Use `--verbose` to monitor progress
2. **Many Files**: Adjust `--max-files` based on your needs
3. **Deep Structures**: Set `--max-depth` to limit traversal
4. **Symlink Heavy**: Use `--no-follow-symlinks` if not needed

## 🔒 Security Considerations

- Automatically excludes `.env` files
- Respects `.gitignore` patterns
- Use `--ignore` for additional sensitive files
- Review output before sharing externally

## 📊 Default Ignore Patterns

Automatically excludes:
- **VCS**: `.git`, `.svn`, `.hg`
- **Dependencies**: `node_modules`, `venv`, `__pycache__`
- **Build**: `dist`, `build`, `target`, `.next`
- **IDE**: `.vscode`, `.idea`, `*.swp`
- **System**: `.DS_Store`, `Thumbs.db`
- **Media**: Images, videos, PDFs
- **Archives**: `.zip`, `.tar.gz`, `.rar`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with ❤️ for developers who need to share and analyze code efficiently with AI tools.

---

**Pro Tip**: For best results with AI models like ChatGPT, Claude, or Gemini, keep output under 10MB using `--max-size` parameter.