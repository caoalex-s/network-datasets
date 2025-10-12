#!/usr/bin/env python3
"""
Build script for Network Datasets documentation.

This script provides a convenient way to build the Sphinx documentation
with proper dependency management and error handling.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        return False
    return True

def main():
    """Build the documentation."""
    # Get the project root directory
    project_root = Path(__file__).parent
    docs_dir = project_root / "docs"
    
    print("Building Network Datasets Documentation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not (project_root / "ndtools").exists():
        print("Error: ndtools directory not found. Are you in the project root?")
        sys.exit(1)
    
    # Install the package in development mode
    print("Installing package in development mode...")
    if not run_command("pip install -e .", cwd=project_root):
        print("Failed to install package")
        sys.exit(1)
    
    # Install documentation dependencies
    print("Installing documentation dependencies...")
    if not run_command("pip install -r docs/requirements.txt", cwd=project_root):
        print("Failed to install documentation dependencies")
        sys.exit(1)
    
    # Clean previous build
    print("Cleaning previous build...")
    build_dir = docs_dir / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Build documentation
    print("Building documentation...")
    if not run_command("make html", cwd=docs_dir):
        print("Failed to build documentation")
        sys.exit(1)
    
    print("\nDocumentation built successfully!")
    print(f"Open {docs_dir / '_build' / 'html' / 'index.html'} in your browser to view the documentation.")
    
    # Check for warnings
    print("\nChecking for documentation warnings...")
    result = subprocess.run(
        "sphinx-build -W -b html . _build/html",
        shell=True,
        cwd=docs_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Warnings or errors found in documentation:")
        print(result.stderr)
    else:
        print("No warnings found in documentation.")

if __name__ == "__main__":
    main()
