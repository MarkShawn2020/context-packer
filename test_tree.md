# context-packer - 项目上下文

## 项目结构

```
context-packer
├── .claude
│   └── settings.local.json ✅
├── .gitignore 💾
├── README.md ✅
├── context_packer.egg-info
│   ├── PKG-INFO 💾
│   ├── SOURCES.txt ✅
│   ├── dependency_links.txt ✅
│   ├── entry_points.txt ✅
│   └── top_level.txt ✅
├── context_packer.py ☑️
└── setup.py ☑️
```

## 项目文件内容

本文档包含了 15 个主要文件的内容。


### README.md

```markdown
# Context Packer

将项目文件夹自动打包成单个markdown文件，便于AI模型(如Gemini)一次性分析整个项目。

## 功能特点

- 🗂️ **智能文件筛选**: 自动忽略不重要的文件（node_modules、.git、编译产物等）
- 📏 **大小控制**: 智能压缩和截断，避免超出AI模型限制
- 🌳 **项目结构**: 生成清晰的文件树展示项目结构
- 📝 **Markdown格式**: 输出格式化的markdown，便于AI理解
- ⚙️ **高度可配置**: 支持自定义忽略规则和大小限制

## 安装

### 方法一：全局安装（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd context-packer

# 全局安装
pip install .

# 或者开发模式安装
pip install -e .
```

安装后可以直接使用命令：

```bash
# 使用完整命令名
context-packer /path/to/project

# 或使用简短别名
ctxpack /path/to/project
```

### 方法二：直接运行

```bash
# 确保Python 3.6+
python3 context_packer.py --help
```

## 使用方法

### 基本用法

```bash
# 打包当前项目（全局安装后）
context-packer /path/to/your/project

# 或使用简短命令
ctxpack /path/to/your/project

# 指定输出文件
ctxpack /path/to/your/project -o my_project_context.md

# 直接运行方式
python3 context_packer.py /path/to/your/project
```

### 高级选项

```bash
# 自定义忽略规则
ctxpack /path/to/project --ignore "*.log" "temp/*" "private/"

# 调整大小限制
ctxpack /path/to/project --max-size 20 --max-files 200

# 完整示例
ctxpack ~/my-react-app \
  -o react_project_context.md \
  --ignore "*.test.js" "coverage/" \
  --max-size 15 \
  --max-files 150
```

## 输出格式

生成的markdown文件包含：

1. **项目结构**: 文件树形式展示
2. **文件内容**: 按重要性排序的文件内容
3. **语法高亮**: 根据文件类型自动识别语言

示例输出：

```markdown
# MyProject - 项目上下文

## 项目结构

```
MyProject
├── src/
│   ├── components/
│   │   └── Button.tsx
│   └── utils/
│       └── helpers.js
├── package.json
└── README.md
```

## 项目文件内容

### package.json

```json
{
  "name": "my-project",
  "version": "1.0.0"
}
```

### src/components/Button.tsx

```tsx
import React from 'react';

export const Button = ({ children, onClick }) => {
  return <button onClick={onClick}>{children}</button>;
};
```
```

## 默认忽略规则

工具会自动忽略以下文件/目录：

- **版本控制**: `.git`, `.svn`, `.hg`
- **依赖管理**: `node_modules`, `venv`, `__pycache__`
- **构建产物**: `build`, `dist`, `target`, `.next`
- **IDE文件**: `.vscode`, `.idea`, `*.swp`
- **系统文件**: `.DS_Store`, `Thumbs.db`
- **媒体文件**: `*.jpg`, `*.png`, `*.mp4`, `*.pdf`
- **压缩文件**: `*.zip`, `*.tar.gz`, `*.rar`

## 配置文件支持

工具会自动读取项目中的 `.gitignore` 文件，并应用其中的忽略规则。

## 使用场景

- **AI代码审查**: 让AI一次性分析整个项目
- **项目文档**: 快速生成项目概览文档
- **代码分享**: 将项目打包分享给他人
- **学习研究**: 快速了解开源项目结构

## 技术实现

- **智能文件检测**: 基于扩展名和MIME类型判断文本文件
- **大小控制**: 多层次的大小限制防止输出过大
- **优先级排序**: 重要文件（README、package.json）优先包含
- **内容截断**: 过长文件智能截断，保留开头和结尾

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `project_path` | 项目文件夹路径 | 必填 |
| `-o, --output` | 输出文件路径 | `project_context.md` |
| `--ignore` | 额外忽略模式 | 无 |
| `--max-size` | 最大总大小(MB) | 10 |
| `--max-files` | 最大文件数量 | 100 |

## 注意事项

- 建议在项目根目录运行，以获得最佳效果
- 大型项目可能需要调整 `--max-size` 参数
- 敏感信息请通过 `--ignore` 参数排除
- 生成的文件可能较大，注意AI模型的输入限制

## 许可证

MIT License
```


### context_packer.py

```python
#!/usr/bin/env python3
"""
Context Packer - 将项目文件夹打包成单个markdown文件，便于AI分析
"""

import os
import argparse
import mimetypes
from pathlib import Path
from typing import List, Set, Dict, Optional
import json
import fnmatch
import sys
from datetime import datetime

class ContextPacker:
    def __init__(self):
        self.default_ignore_patterns = {
            # 版本控制
            '.git', '.svn', '.hg',
            # 依赖管理
            'node_modules', 'venv', 'env', '__pycache__', '.pytest_cache',
            'vendor', 'target', 'build', 'dist', '.next', '.nuxt',
            # IDE和编辑器
            '.vscode', '.idea', '*.swp', '*.swo', '*~',
            # 操作系统
            '.DS_Store', 'Thumbs.db', 'desktop.ini',
            # 日志和缓存
            '*.log', '*.tmp', '.cache', '.temp',
            # 编译产物
            '*.pyc', '*.pyo', '*.class', '*.o', '*.so', '*.dll',
            # 大文件类型
            '*.zip', '*.tar.gz', '*.rar', '*.7z', '*.pdf',
            '*.mp4', '*.avi', '*.mov', '*.mp3', '*.wav',
            '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.svg',
            # 配置文件
            '.env', '.env.local', '.env.production',
            # 避免自循环
            'project_context.md', '*_context.md'
        }
        
        self.text_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.vue', '.svelte',
            '.html', '.htm', '.css', '.scss', '.sass', '.less',
            '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
            '.md', '.txt', '.rst', '.tex',
            '.c', '.cpp', '.h', '.hpp', '.java', '.cs', '.php',
            '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat',
            '.sql', '.r', '.m', '.pl', '.lua', '.dart',
            '.Dockerfile', '.gitignore', '.gitattributes',
            '.editorconfig', '.prettierrc', '.eslintrc'
        }
        
        self.max_file_size = 1024 * 1024  # 1MB
        self.max_total_size = 10 * 1024 * 1024  # 10MB
        self.verbose = False
        
    def should_ignore(self, path: Path, ignore_patterns: Set[str]) -> bool:
        """检查文件/目录是否应该被忽略"""
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(path.name, pattern) or fnmatch.fnmatch(str(path), pattern):
                return True
        return False
    
    def is_text_file(self, file_path: Path) -> bool:
        """判断文件是否为文本文件"""
        if file_path.suffix.lower() in self.text_extensions:
            return True
        
        if file_path.name in ['Makefile', 'Dockerfile', 'LICENSE', 'README']:
            return True
            
        try:
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type and mime_type.startswith('text/'):
                return True
        except:
            pass
            
        return False
    
    def get_file_tree(self, root_path: Path, ignore_patterns: Set[str], 
                      file_status: Dict[Path, str] = None) -> str:
        """生成项目文件树结构并显示文件状态"""
        if file_status is None:
            file_status = {}
        
        def get_file_status_symbol(path: Path) -> str:
            """获取文件状态符号"""
            if path.is_dir():
                return ""
            
            status = file_status.get(path, "unknown")
            symbols = {
                "included_high": " ✅",      # 高优先级，已包含
                "included_medium": " ☑️",    # 中优先级，已包含  
                "included_low": " ✅",       # 低优先级，已包含
                "skipped_ignored": " ⏭️",    # 被忽略
                "skipped_binary": " 💾",    # 二进制文件
                "skipped_large": " 📊",     # 文件过大
                "skipped_limit": " 🚫",     # 超出数量限制
                "unknown": ""
            }
            return symbols.get(status, "")
        
        def build_tree(path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
            if self.should_ignore(path, ignore_patterns):
                return []
            
            lines = []
            connector = "└── " if is_last else "├── "
            status_symbol = get_file_status_symbol(path)
            lines.append(f"{prefix}{connector}{path.name}{status_symbol}")
            
            if path.is_dir():
                try:
                    children = sorted([p for p in path.iterdir() 
                                     if not self.should_ignore(p, ignore_patterns)])
                    for i, child in enumerate(children):
                        is_child_last = (i == len(children) - 1)
                        extension = "    " if is_last else "│   "
                        lines.extend(build_tree(child, prefix + extension, is_child_last))
                except PermissionError:
                    pass
            
            return lines
        
        tree_lines = [root_path.name]
        try:
            children = sorted([p for p in root_path.iterdir() 
                             if not self.should_ignore(p, ignore_patterns)])
            for i, child in enumerate(children):
                is_last = (i == len(children) - 1)
                tree_lines.extend(build_tree(child, "", is_last))
        except PermissionError:
            tree_lines.append("Permission denied")
        
        return "\n".join(tree_lines)
    
    def truncate_content(self, content: str, max_lines: int = 500) -> str:
        """截断过长的文件内容"""
        lines = content.split('\n')
        if len(lines) <= max_lines:
            return content
        
        truncated_lines = lines[:max_lines//2] + \
                         [f"\n... (省略 {len(lines) - max_lines} 行) ...\n"] + \
                         lines[-max_lines//2:]
        return '\n'.join(truncated_lines)
    
    def collect_files(self, root_path: Path, ignore_patterns: Set[str]) -> tuple[List[Dict], Dict[Path, str]]:
        """收集需要打包的文件并返回文件状态信息"""
        files = []
        total_size = 0
        skipped_files = {'too_large': 0, 'ignored': 0, 'binary': 0, 'limit': 0}
        file_status = {}  # 记录每个文件的状态
        
        # 收集所有文件用于统计
        all_files = list(root_path.rglob('*'))
        text_files = [f for f in all_files if f.is_file()]
        
        if self.verbose:
            print(f"📂 扫描项目: {root_path.name}")
            print(f"📄 发现 {len(text_files)} 个文件")
        
        processed = 0
        for file_path in text_files:
            processed += 1
            
            if self.verbose and processed % 50 == 0:
                print(f"⏳ 处理进度: {processed}/{len(text_files)} ({processed/len(text_files)*100:.1f}%)")
            
            if self.should_ignore(file_path, ignore_patterns):
                file_status[file_path] = "skipped_ignored"
                skipped_files['ignored'] += 1
                continue
            
            if not self.is_text_file(file_path):
                file_status[file_path] = "skipped_binary"
                skipped_files['binary'] += 1
                continue
            
            try:
                file_size = file_path.stat().st_size
                if file_size > self.max_file_size:
                    file_status[file_path] = "skipped_large"
                    skipped_files['too_large'] += 1
                    if self.verbose:
                        print(f"⚠️  跳过大文件: {file_path.relative_to(root_path)} ({file_size/1024/1024:.1f}MB)")
                    continue
                
                if total_size + file_size > self.max_total_size:
                    print(f"\n⚠️  达到总大小限制 ({self.max_total_size/1024/1024:.1f}MB)，停止收集文件")
                    print(f"已收集 {len(files)} 个文件，总大小 {total_size/1024/1024:.2f}MB")
                    break
                
                relative_path = file_path.relative_to(root_path)
                files.append({
                    'path': relative_path,
                    'size': file_size,
                    'full_path': file_path
                })
                total_size += file_size
                
            except (OSError, PermissionError) as e:
                if self.verbose:
                    print(f"⚠️  无法读取: {file_path.relative_to(root_path)} ({e})")
                continue
        
        # 按重要性排序
        def get_priority(file_info):
            path = str(file_info['path']).lower()
            if any(name in path for name in ['readme', 'package.json', 'requirements.txt', 'cargo.toml']):
                return 0
            if path.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                return 1
            if path.endswith(('.md', '.txt', '.json', '.yml', '.yaml')):
                return 2
            return 3
        
        files.sort(key=get_priority)
        
        # 设置包含文件的状态和优先级
        for i, file_info in enumerate(files):
            file_path = file_info['full_path']
            priority = get_priority(file_info)
            
            if i < 100:  # 在限制范围内
                if priority == 0:
                    file_status[file_path] = "included_high"
                elif priority <= 1:
                    file_status[file_path] = "included_medium" 
                else:
                    file_status[file_path] = "included_low"
            else:  # 超出限制
                file_status[file_path] = "skipped_limit"
                skipped_files['limit'] += 1
        
        limited_files = files[:100]  # 限制文件数量
        
        # 输出统计信息
        print(f"\n📊 文件统计:")
        print(f"  ✅ 已包含: {len(limited_files)} 个文件 ({total_size/1024/1024:.2f}MB)")
        print(f"  ⏭️  跳过忽略: {skipped_files['ignored']} 个")
        print(f"  ⏭️  跳过二进制: {skipped_files['binary']} 个")
        print(f"  ⏭️  跳过大文件: {skipped_files['too_large']} 个")
        if skipped_files['limit'] > 0:
            print(f"  ⏭️  超出限制: {skipped_files['limit']} 个")
        
        return limited_files, file_status
    
    def pack_project(self, project_path: str, output_path: str = None, 
                    custom_ignore: List[str] = None) -> str:
        """打包项目到markdown文件"""
        root_path = Path(project_path).resolve()
        if not root_path.exists():
            raise FileNotFoundError(f"❌ 项目路径不存在: {project_path}")
        
        # 处理默认输出路径，避免自循环
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{root_path.name}_context_{timestamp}.md"
            # 确保输出到父目录而不是项目内部
            if Path(output_path).parent == Path('.'):
                output_path = root_path.parent / output_path
        
        output_path = Path(output_path).resolve()
        
        # 检查输出文件是否在项目内部
        try:
            output_path.relative_to(root_path)
            print(f"⚠️  输出文件在项目内部，可能导致自循环")
            print(f"建议使用 -o 参数指定项目外的输出路径")
        except ValueError:
            pass  # 输出文件不在项目内部，正常
        
        ignore_patterns = self.default_ignore_patterns.copy()
        if custom_ignore:
            ignore_patterns.update(custom_ignore)
        
        # 添加输出文件到忽略列表
        ignore_patterns.add(output_path.name)
        
        # 检查是否有项目特定的忽略文件
        gitignore_path = root_path / '.gitignore'
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    gitignore_count = 0
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.add(line)
                            gitignore_count += 1
                if self.verbose and gitignore_count > 0:
                    print(f"📋 从 .gitignore 加载 {gitignore_count} 个忽略规则")
            except:
                pass
        
        print(f"\n🚀 开始打包项目: {root_path.name}")
        
        # 生成输出
        markdown_content = self.generate_markdown(root_path, ignore_patterns)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"\n✅ 项目已成功打包到: {output_path}")
            print(f"📄 文件大小: {output_path.stat().st_size / 1024:.1f}KB")
        except Exception as e:
            print(f"\n❌ 写入文件失败: {e}")
            raise
        
        return markdown_content
    
    def generate_markdown(self, root_path: Path, ignore_patterns: Set[str]) -> str:
        """生成markdown格式的项目内容"""
        project_name = root_path.name
        
        # 收集文件和状态信息
        files, file_status = self.collect_files(root_path, ignore_patterns)
        
        # 生成文件树（包含状态标记）
        file_tree = self.get_file_tree(root_path, ignore_patterns, file_status)
        
        # 生成markdown
        content = f"""# {project_name} - 项目上下文

## 项目结构

```
{file_tree}
```

## 项目文件内容

本文档包含了 {len(files)} 个主要文件的内容。

"""
        
        for file_info in files:
            rel_path = file_info['path']
            full_path = file_info['full_path']
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                
                # 截断过长内容
                if len(file_content) > 10000:
                    file_content = self.truncate_content(file_content)
                
                # 确定语言类型
                extension = full_path.suffix.lower()
                lang_map = {
                    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                    '.jsx': 'jsx', '.tsx': 'tsx', '.html': 'html',
                    '.css': 'css', '.scss': 'scss', '.json': 'json',
                    '.yaml': 'yaml', '.yml': 'yaml', '.xml': 'xml',
                    '.sh': 'bash', '.sql': 'sql', '.md': 'markdown'
                }
                lang = lang_map.get(extension, '')
                
                content += f"""
### {rel_path}

```{lang}
{file_content}
```

"""
            except Exception as e:
                content += f"""
### {rel_path}

```
无法读取文件内容: {str(e)}
```

"""
        
        content += f"""
---

*此文档由 Context Packer 自动生成*
*项目路径: {root_path}*
*生成时间: {os.popen('date').read().strip()}*
"""
        
        return content

def main():
    parser = argparse.ArgumentParser(
        description='将项目文件夹打包成单个markdown文件，便于AI分析',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s /path/to/project                    # 基本用法
  %(prog)s . -o my_project.md                  # 指定输出文件
  %(prog)s . --ignore "*.log" "temp/"          # 自定义忽略规则
  %(prog)s . --max-size 20 --verbose          # 调整大小并显示详细信息
        """
    )
    parser.add_argument('project_path', help='项目文件夹路径')
    parser.add_argument('-o', '--output', help='输出文件路径（默认：项目名_context_时间戳.md）')
    parser.add_argument('--ignore', nargs='*', help='额外的忽略模式')
    parser.add_argument('--max-size', type=int, default=10, 
                       help='最大总大小(MB，默认：10)')
    parser.add_argument('--max-files', type=int, default=100,
                       help='最大文件数量（默认：100）')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细处理信息')
    
    args = parser.parse_args()
    
    packer = ContextPacker()
    packer.max_total_size = args.max_size * 1024 * 1024
    packer.verbose = args.verbose
    
    try:
        start_time = datetime.now()
        
        packer.pack_project(
            project_path=args.project_path,
            output_path=args.output,
            custom_ignore=args.ignore or []
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if args.verbose:
            print(f"\\n⏱️  总耗时: {duration:.2f}秒")
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("请检查项目路径是否正确")
        return 1
    except PermissionError as e:
        print(f"❌ 权限错误: {e}")
        print("请检查是否有足够的读写权限")
        return 1
    except KeyboardInterrupt:
        print("\\n⚠️  用户取消操作")
        return 1
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
```


### setup.py

```python
#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="context-packer",
    version="1.0.0",
    author="Context Packer",
    description="将项目文件夹自动打包成单个markdown文件，便于AI模型分析",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["context_packer"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "context-packer=context_packer:main",
            "ctxpack=context_packer:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    keywords="ai, context, markdown, project, packaging, gemini, claude",
    install_requires=[],
)
```


### build/lib/context_packer.py

```python
#!/usr/bin/env python3
"""
Context Packer - 将项目文件夹打包成单个markdown文件，便于AI分析
"""

import os
import argparse
import mimetypes
from pathlib import Path
from typing import List, Set, Dict, Optional
import json
import fnmatch

class ContextPacker:
    def __init__(self):
        self.default_ignore_patterns = {
            # 版本控制
            '.git', '.svn', '.hg',
            # 依赖管理
            'node_modules', 'venv', 'env', '__pycache__', '.pytest_cache',
            'vendor', 'target', 'build', 'dist', '.next', '.nuxt',
            # IDE和编辑器
            '.vscode', '.idea', '*.swp', '*.swo', '*~',
            # 操作系统
            '.DS_Store', 'Thumbs.db', 'desktop.ini',
            # 日志和缓存
            '*.log', '*.tmp', '.cache', '.temp',
            # 编译产物
            '*.pyc', '*.pyo', '*.class', '*.o', '*.so', '*.dll',
            # 大文件类型
            '*.zip', '*.tar.gz', '*.rar', '*.7z', '*.pdf',
            '*.mp4', '*.avi', '*.mov', '*.mp3', '*.wav',
            '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.svg',
            # 配置文件
            '.env', '.env.local', '.env.production'
        }
        
        self.text_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.vue', '.svelte',
            '.html', '.htm', '.css', '.scss', '.sass', '.less',
            '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
            '.md', '.txt', '.rst', '.tex',
            '.c', '.cpp', '.h', '.hpp', '.java', '.cs', '.php',
            '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat',
            '.sql', '.r', '.m', '.pl', '.lua', '.dart',
            '.Dockerfile', '.gitignore', '.gitattributes',
            '.editorconfig', '.prettierrc', '.eslintrc'
        }
        
        self.max_file_size = 1024 * 1024  # 1MB
        self.max_total_size = 10 * 1024 * 1024  # 10MB
        
    def should_ignore(self, path: Path, ignore_patterns: Set[str]) -> bool:
        """检查文件/目录是否应该被忽略"""
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(path.name, pattern) or fnmatch.fnmatch(str(path), pattern):
                return True
        return False
    
    def is_text_file(self, file_path: Path) -> bool:
        """判断文件是否为文本文件"""
        if file_path.suffix.lower() in self.text_extensions:
            return True
        
        if file_path.name in ['Makefile', 'Dockerfile', 'LICENSE', 'README']:
            return True
            
        try:
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type and mime_type.startswith('text/'):
                return True
        except:
            pass
            
        return False
    
    def get_file_tree(self, root_path: Path, ignore_patterns: Set[str]) -> str:
        """生成项目文件树结构"""
        def build_tree(path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
            if self.should_ignore(path, ignore_patterns):
                return []
            
            lines = []
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{path.name}")
            
            if path.is_dir():
                try:
                    children = sorted([p for p in path.iterdir() 
                                     if not self.should_ignore(p, ignore_patterns)])
                    for i, child in enumerate(children):
                        is_child_last = (i == len(children) - 1)
                        extension = "    " if is_last else "│   "
                        lines.extend(build_tree(child, prefix + extension, is_child_last))
                except PermissionError:
                    pass
            
            return lines
        
        tree_lines = [root_path.name]
        try:
            children = sorted([p for p in root_path.iterdir() 
                             if not self.should_ignore(p, ignore_patterns)])
            for i, child in enumerate(children):
                is_last = (i == len(children) - 1)
                tree_lines.extend(build_tree(child, "", is_last))
        except PermissionError:
            tree_lines.append("Permission denied")
        
        return "\n".join(tree_lines)
    
    def truncate_content(self, content: str, max_lines: int = 500) -> str:
        """截断过长的文件内容"""
        lines = content.split('\n')
        if len(lines) <= max_lines:
            return content
        
        truncated_lines = lines[:max_lines//2] + \
                         [f"\n... (省略 {len(lines) - max_lines} 行) ...\n"] + \
                         lines[-max_lines//2:]
        return '\n'.join(truncated_lines)
    
    def collect_files(self, root_path: Path, ignore_patterns: Set[str]) -> List[Dict]:
        """收集需要打包的文件"""
        files = []
        total_size = 0
        
        for file_path in root_path.rglob('*'):
            if not file_path.is_file():
                continue
                
            if self.should_ignore(file_path, ignore_patterns):
                continue
            
            if not self.is_text_file(file_path):
                continue
            
            try:
                file_size = file_path.stat().st_size
                if file_size > self.max_file_size:
                    continue
                
                if total_size + file_size > self.max_total_size:
                    print(f"达到总大小限制，停止收集文件")
                    break
                
                relative_path = file_path.relative_to(root_path)
                files.append({
                    'path': relative_path,
                    'size': file_size,
                    'full_path': file_path
                })
                total_size += file_size
                
            except (OSError, PermissionError):
                continue
        
        # 按重要性排序
        def get_priority(file_info):
            path = str(file_info['path']).lower()
            if any(name in path for name in ['readme', 'package.json', 'requirements.txt', 'cargo.toml']):
                return 0
            if path.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                return 1
            if path.endswith(('.md', '.txt', '.json', '.yml', '.yaml')):
                return 2
            return 3
        
        files.sort(key=get_priority)
        return files[:100]  # 限制文件数量
    
    def pack_project(self, project_path: str, output_path: str = None, 
                    custom_ignore: List[str] = None) -> str:
        """打包项目到markdown文件"""
        root_path = Path(project_path).resolve()
        if not root_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {project_path}")
        
        ignore_patterns = self.default_ignore_patterns.copy()
        if custom_ignore:
            ignore_patterns.update(custom_ignore)
        
        # 检查是否有项目特定的忽略文件
        gitignore_path = root_path / '.gitignore'
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.add(line)
            except:
                pass
        
        # 生成输出
        markdown_content = self.generate_markdown(root_path, ignore_patterns)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"项目已打包到: {output_path}")
        
        return markdown_content
    
    def generate_markdown(self, root_path: Path, ignore_patterns: Set[str]) -> str:
        """生成markdown格式的项目内容"""
        project_name = root_path.name
        
        # 文件树
        file_tree = self.get_file_tree(root_path, ignore_patterns)
        
        # 收集文件
        files = self.collect_files(root_path, ignore_patterns)
        
        # 生成markdown
        content = f"""# {project_name} - 项目上下文

## 项目结构

```
{file_tree}
```

## 项目文件内容

本文档包含了 {len(files)} 个主要文件的内容。

"""
        
        for file_info in files:
            rel_path = file_info['path']
            full_path = file_info['full_path']
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                
                # 截断过长内容
                if len(file_content) > 10000:
                    file_content = self.truncate_content(file_content)
                
                # 确定语言类型
                extension = full_path.suffix.lower()
                lang_map = {
                    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                    '.jsx': 'jsx', '.tsx': 'tsx', '.html': 'html',
                    '.css': 'css', '.scss': 'scss', '.json': 'json',
                    '.yaml': 'yaml', '.yml': 'yaml', '.xml': 'xml',
                    '.sh': 'bash', '.sql': 'sql', '.md': 'markdown'
                }
                lang = lang_map.get(extension, '')
                
                content += f"""
### {rel_path}

```{lang}
{file_content}
```

"""
            except Exception as e:
                content += f"""
### {rel_path}

```
无法读取文件内容: {str(e)}
```

"""
        
        content += f"""
---

*此文档由 Context Packer 自动生成*
*项目路径: {root_path}*
*生成时间: {os.popen('date').read().strip()}*
"""
        
        return content

def main():
    parser = argparse.ArgumentParser(description='将项目文件夹打包成单个markdown文件')
    parser.add_argument('project_path', help='项目文件夹路径')
    parser.add_argument('-o', '--output', help='输出文件路径', 
                       default='project_context.md')
    parser.add_argument('--ignore', nargs='*', help='额外的忽略模式')
    parser.add_argument('--max-size', type=int, default=10, 
                       help='最大总大小(MB)')
    parser.add_argument('--max-files', type=int, default=100,
                       help='最大文件数量')
    
    args = parser.parse_args()
    
    packer = ContextPacker()
    packer.max_total_size = args.max_size * 1024 * 1024
    
    try:
        packer.pack_project(
            project_path=args.project_path,
            output_path=args.output,
            custom_ignore=args.ignore or []
        )
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
```


### .claude/settings.local.json

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 context_packer.py:*)",
      "Bash(chmod:*)",
      "Bash(pip install:*)",
      "Bash(ctxpack:*)"
    ],
    "deny": []
  }
}
```


### context_packer.egg-info/SOURCES.txt

```
README.md
context_packer.py
setup.py
context_packer.egg-info/PKG-INFO
context_packer.egg-info/SOURCES.txt
context_packer.egg-info/dependency_links.txt
context_packer.egg-info/entry_points.txt
context_packer.egg-info/top_level.txt
```


### context_packer.egg-info/entry_points.txt

```
[console_scripts]
context-packer = context_packer:main
ctxpack = context_packer:main

```


### context_packer.egg-info/top_level.txt

```
context_packer

```


### context_packer.egg-info/dependency_links.txt

```


```


### .idea/vcs.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="VcsDirectoryMappings">
    <mapping directory="$PROJECT_DIR$" vcs="Git" />
  </component>
</project>
```


### .idea/workspace.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="SELECTIVE" />
  </component>
  <component name="ChangeListManager">
    <list default="true" id="26230049-b974-4eb3-aac8-fe4f820dc057" name="Changes" comment="">
      <change beforePath="$PROJECT_DIR$/context_packer.py" beforeDir="false" afterPath="$PROJECT_DIR$/context_packer.py" afterDir="false" />
    </list>
    <option name="SHOW_DIALOG" value="false" />
    <option name="HIGHLIGHT_CONFLICTS" value="true" />
    <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />
    <option name="LAST_RESOLUTION" value="IGNORE" />
  </component>
  <component name="Git.Settings">
    <option name="RECENT_GIT_ROOT_PATH" value="$PROJECT_DIR$" />
  </component>
  <component name="ProjectColorInfo"><![CDATA[{
  "associatedIndex": 5
}]]></component>
  <component name="ProjectId" id="2z0jziwUbfT7YmRp66gwiQ39pwW" />
  <component name="ProjectViewState">
    <option name="hideEmptyMiddlePackages" value="true" />
    <option name="showLibraryContents" value="true" />
  </component>
  <component name="PropertiesComponent"><![CDATA[{
  "keyToString": {
    "RunOnceActivity.ShowReadmeOnStart": "true",
    "git-widget-placeholder": "main",
    "last_opened_file_path": "/Users/mark/projects/context-packer",
    "node.js.detected.package.eslint": "true",
    "node.js.detected.package.tslint": "true",
    "node.js.selected.package.eslint": "(autodetect)",
    "node.js.selected.package.tslint": "(autodetect)",
    "nodejs_package_manager_path": "npm",
    "settings.editor.selected.configurable": "ssh.settings",
    "vue.rearranger.settings.migration": "true"
  }
}]]></component>
  <component name="SharedIndexes">
    <attachedChunks>
      <set>
        <option value="bundled-js-predefined-d6986cc7102b-7c0b70fcd90d-JavaScript-PY-242.21829.153" />
        <option value="bundled-python-sdk-464836ebc622-b74155a9e76b-com.jetbrains.pycharm.pro.sharedIndexes.bundled-PY-242.21829.153" />
      </set>
    </attachedChunks>
  </component>
  <component name="SpellCheckerSettings" RuntimeDictionaries="0" Folders="0" CustomDictionaries="0" DefaultDictionary="application-level" UseSingleDictionary="true" transferred="true" />
  <component name="TaskManager">
    <task active="true" id="Default" summary="Default task">
      <changelist id="26230049-b974-4eb3-aac8-fe4f820dc057" name="Changes" comment="" />
      <created>1750875148450</created>
      <option name="number" value="Default" />
      <option name="presentableId" value="Default" />
      <updated>1750875148450</updated>
      <workItem from="1750875149558" duration="1451000" />
    </task>
    <servers />
  </component>
  <component name="TypeScriptGeneratedFilesManager">
    <option name="version" value="3" />
  </component>
</project>
```


### .idea/modules.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/.idea/context-packer.iml" filepath="$PROJECT_DIR$/.idea/context-packer.iml" />
    </modules>
  </component>
</project>
```


### .idea/misc.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" project-jdk-name="Poetry (mita-huawei)" project-jdk-type="Python SDK" />
</project>
```


### .idea/inspectionProfiles/profiles_settings.xml

```xml
<component name="InspectionProjectProfileManager">
  <settings>
    <option name="USE_PROJECT_PROFILE" value="false" />
    <version value="1.0" />
  </settings>
</component>
```


### .idea/inspectionProfiles/Project_Default.xml

```xml
<component name="InspectionProjectProfileManager">
  <profile version="1.0">
    <option name="myName" value="Project Default" />
    <inspection_tool class="Eslint" enabled="true" level="WARNING" enabled_by_default="true" />
  </profile>
</component>
```


---

*此文档由 Context Packer 自动生成*
*项目路径: /Users/mark/projects/context-packer*
*生成时间: 2025年 6月26日 星期四 04时21分17秒 CST*
