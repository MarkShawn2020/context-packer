.PHONY: help install install-dev test lint format clean build publish publish-test release

# Default version bump type
VERSION ?= patch

help:
	@echo "Available commands:"
	@echo "  make install       Install the package"
	@echo "  make install-dev   Install with development dependencies"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linting checks"
	@echo "  make format        Format code with black"
	@echo "  make clean         Clean build artifacts"
	@echo "  make build         Build distribution packages"
	@echo "  make publish-test  Publish to Test PyPI"
	@echo "  make publish       Publish to PyPI"
	@echo "  make release       Complete release (bump version, tag, publish)"
	@echo ""
	@echo "Examples:"
	@echo "  make release                # Release with patch version bump"
	@echo "  make release VERSION=minor   # Release with minor version bump"
	@echo "  make release VERSION=major   # Release with major version bump"

install:
	pip install -e .

install-dev:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	python tests/test_context_packer.py
	@echo "\nFor full pytest run: pytest tests/"

lint:
	ruff check context_packer.py
	mypy context_packer.py --ignore-missing-imports

format:
	black context_packer.py
	ruff check --fix context_packer.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*_context*.md" -delete

build: clean
	python -m build

publish-test: build
	twine check dist/*
	twine upload -r testpypi dist/*

publish: build
	twine check dist/*
	twine upload dist/*

release: test format
	@echo "📦 Starting release process with $(VERSION) version bump..."
	@python bump_version.py $(VERSION)
	@echo "\n📝 Creating git commit..."
	@git add -A
	@git commit -m "Release: bump version ($(VERSION))" || echo "No changes to commit"
	@VERSION=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2) && \
		echo "\n🏷️  Creating tag v$$VERSION..." && \
		git tag -a "v$$VERSION" -m "Release version $$VERSION" && \
		echo "\n🚀 Pushing to GitHub..." && \
		git push origin main --follow-tags && \
		echo "\n📤 Publishing to PyPI..." && \
		make publish && \
		echo "\n✅ Release v$$VERSION completed successfully!" && \
		echo "\n📦 Install with: pip install context-packer==$$VERSION" && \
		echo "🔗 View release: https://github.com/MarkShawn2020/context-packer/releases/tag/v$$VERSION"