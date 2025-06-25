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