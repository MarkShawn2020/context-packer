#!/usr/bin/env python3
"""
Basic tests for context_packer module.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import context_packer
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import context_packer


def test_context_packer_initialization():
    """Test ContextPacker initialization."""
    packer = context_packer.ContextPacker()
    assert packer.max_file_size == 1024 * 1024  # 1MB
    assert packer.max_total_size == 10 * 1024 * 1024  # 10MB
    assert packer.follow_symlinks == True
    assert packer.verbose == False


def test_is_text_file():
    """Test text file detection."""
    packer = context_packer.ContextPacker()
    
    # Test known text extensions
    assert packer.is_text_file(Path("test.py")) == True
    assert packer.is_text_file(Path("test.js")) == True
    assert packer.is_text_file(Path("test.md")) == True
    assert packer.is_text_file(Path("README")) == True
    assert packer.is_text_file(Path("Makefile")) == True
    
    # Test non-text extensions
    assert packer.is_text_file(Path("test.jpg")) == False
    assert packer.is_text_file(Path("test.mp4")) == False
    assert packer.is_text_file(Path("test.zip")) == False


def test_should_ignore():
    """Test ignore pattern matching."""
    packer = context_packer.ContextPacker()
    ignore_patterns = {"*.log", "node_modules", ".git"}
    
    # Test patterns that should be ignored
    assert packer.should_ignore(Path("test.log"), ignore_patterns) == True
    assert packer.should_ignore(Path("node_modules"), ignore_patterns) == True
    assert packer.should_ignore(Path(".git"), ignore_patterns) == True
    
    # Test patterns that should not be ignored
    assert packer.should_ignore(Path("test.py"), ignore_patterns) == False
    assert packer.should_ignore(Path("src"), ignore_patterns) == False


def test_pack_simple_project():
    """Test packing a simple project."""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure
        test_dir = Path(tmpdir) / "test_project"
        test_dir.mkdir()
        
        # Create some test files
        (test_dir / "README.md").write_text("# Test Project\n\nThis is a test.")
        (test_dir / "main.py").write_text("def main():\n    print('Hello')")
        (test_dir / "config.json").write_text('{"name": "test"}')
        
        # Create subdirectory
        sub_dir = test_dir / "src"
        sub_dir.mkdir()
        (sub_dir / "utils.py").write_text("def helper():\n    pass")
        
        # Pack the project
        packer = context_packer.ContextPacker()
        output_file = Path(tmpdir) / "output.md"
        
        packer.pack_project(
            project_path=str(test_dir),
            output_path=str(output_file)
        )
        
        # Verify output file was created
        assert output_file.exists()
        
        # Verify content
        content = output_file.read_text()
        assert "Test Project" in content
        assert "README.md" in content
        assert "main.py" in content
        assert "config.json" in content
        assert "utils.py" in content
        assert "def main():" in content
        assert "def helper():" in content


def test_symlink_handling():
    """Test symlink handling functionality."""
    # Skip this test on Windows
    if sys.platform.startswith('win'):
        return
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure with symlinks
        test_dir = Path(tmpdir) / "test_project"
        test_dir.mkdir()
        
        # Create a file and directory
        (test_dir / "file.txt").write_text("Original file")
        sub_dir = test_dir / "subdir"
        sub_dir.mkdir()
        (sub_dir / "sub_file.txt").write_text("Subdirectory file")
        
        # Create symlinks
        link_dir = test_dir / "link_to_subdir"
        link_dir.symlink_to(sub_dir)
        
        link_file = test_dir / "link_to_file.txt"
        link_file.symlink_to(test_dir / "file.txt")
        
        # Test with symlink following enabled
        packer = context_packer.ContextPacker()
        packer.follow_symlinks = True
        output_file = Path(tmpdir) / "with_symlinks.md"
        
        packer.pack_project(
            project_path=str(test_dir),
            output_path=str(output_file)
        )
        
        content = output_file.read_text()
        assert "link_to_subdir" in content
        assert "link_to_file.txt" in content
        
        # Test with symlink following disabled
        packer.follow_symlinks = False
        output_file_no_follow = Path(tmpdir) / "no_symlinks.md"
        
        packer.pack_project(
            project_path=str(test_dir),
            output_path=str(output_file_no_follow)
        )
        
        # The content should still show symlinks in tree but not follow them
        content_no_follow = output_file_no_follow.read_text()
        assert "link_to_subdir" in content_no_follow or "link_to_file" in content_no_follow


if __name__ == "__main__":
    # Run tests manually
    test_context_packer_initialization()
    print("✓ Initialization test passed")
    
    test_is_text_file()
    print("✓ Text file detection test passed")
    
    test_should_ignore()
    print("✓ Ignore pattern test passed")
    
    test_pack_simple_project()
    print("✓ Simple project packing test passed")
    
    test_symlink_handling()
    print("✓ Symlink handling test passed")
    
    print("\n✅ All tests passed!")