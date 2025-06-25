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