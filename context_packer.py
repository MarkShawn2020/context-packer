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