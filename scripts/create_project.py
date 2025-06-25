#!/usr/bin/env python3
"""
Script to create a new Python project in the monorepo.

This script creates a new project directory with the standard structure:
  project_name/
    src/
      __init__.py
    tests/
      __init__.py
    pyproject.toml
    README.md
"""

import argparse
import sys
from pathlib import Path
from string import Template
from typing import Optional

# Template for pyproject.toml
PYPROJECT_TEMPLATE = """[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "${project_name}"
version = "0.1.0"
description = "${description}"
authors = [
    {name = "${author}", email = "${author_email}"}
]
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
python_classes = "Test*"
addopts = "-v -s --cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
omit = ["**/__init__.py"]

[tool.coverage.report]
show_missing = true
skip_covered = true

[metadata]
license_files = ["LICENSE"]
"""

# Template for README.md
README_TEMPLATE = """# ${project_name}

${description}

## Description

A Python project in the monorepo.

## Installation

This project is part of a monorepo. To install it in development mode:

```bash
# From the root of the monorepo
pip install -e ./projects/${project_name}
```

## Usage

```python
from ${project_name}.main import main

if __name__ == "__main__":
    main()
```

## Development

### Running Tests

```bash
# From the project directory
cd projects/${project_name}
pytest
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- Flake8 for linting
- Mypy for static type checking

Run all checks:

```bash
black .
isort .
flake8 .
mypy .
```

## License

MIT
"""

# Template for __init__.py
INIT_TEMPLATE = '''"""
{project_name} - {project_description}
"""

__version__ = "0.1.0"
'''

# Template for main.py
MAIN_TEMPLATE = '''"""
Main module for {project_name}.
"""


def main() -> None:
    """Run the main function."""
    print("Hello from {project_name}!")


if __name__ == "__main__":
    main()
'''

# Template for test_main.py
TEST_TEMPLATE = '''"""Tests for the main module."""

from {project_name}.main import main


def test_main(capsys):
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "Hello from {project_name}!" in captured.out
'''


def create_project(
    project_dir: Path,
    project_name: str,
    description: str,
    author_name: str,
    author_email: str,
) -> None:
    """Create a new Python project with standard structure.

    Args:
        project_dir: Directory where the project will be created
        project_name: Name of the project (in snake_case)
        description: Project description
        author_name: Author's name
        author_email: Author's email
    """
    # Create project directories
    src_dir = project_dir / "src" / project_name
    tests_dir = project_dir / "tests"

    src_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    init_content = INIT_TEMPLATE.format(
        project_name=project_name, project_description=description
    )
    (src_dir / "__init__.py").write_text(init_content)
    (tests_dir / "__init__.py").write_text("")

    # Create main.py
    main_content = MAIN_TEMPLATE.format(project_name=project_name)
    (src_dir / "main.py").write_text(main_content)

    # Create test_main.py
    test_content = TEST_TEMPLATE.format(project_name=project_name)
    (tests_dir / "test_main.py").write_text(test_content)

    # Create README.md
    readme_content = Template(README_TEMPLATE).substitute(
        project_name=project_name,
        description=description,
        author=author_name,
    )
    (project_dir / "README.md").write_text(readme_content)

    # Create pyproject.toml
    pyproject_content = Template(PYPROJECT_TEMPLATE).substitute(
        project_name=project_name,
        description=description,
        author=author_name,
        author_email=author_email,
    )
    (project_dir / "pyproject.toml").write_text(pyproject_content)

    print(f"✅ Created project: {project_name}")
    print(f"📁 Location: {project_dir}")


def get_git_config_value(key: str) -> Optional[str]:
    """Get a value from git config.

    Args:
        key: The git config key to get

    Returns:
        The value of the git config key, or None if not found
    """
    try:
        import subprocess

        result = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def main() -> None:
    """Main entry point for the script."""
    # Get default values from git config
    default_author = get_git_config_value("user.name") or "Your Name"
    default_email = get_git_config_value("user.email") or "your.email@example.com"

    parser = argparse.ArgumentParser(
        description=(
            "Create a new Python project in the monorepo with standard "
            "structure and configuration."
        )
    )
    parser.add_argument(
        "name",
        type=str,
        help="Name of the project (will be converted to snake_case)",
    )
    parser.add_argument(
        "--description",
        type=str,
        default="A Python project",
        help="Project description",
    )
    parser.add_argument(
        "--author",
        type=str,
        default=default_author,
        help="Author name",
    )
    parser.add_argument(
        "--email",
        type=str,
        default=default_email,
        help="Author email",
    )

    args = parser.parse_args()

    # Convert project name to snake_case
    project_name = args.name.lower().replace("-", "_").replace(" ", "_")

    # Define project directory
    projects_dir = Path(__file__).parent.parent / "projects"
    project_dir = projects_dir / project_name

    # Check if project already exists
    if project_dir.exists():
        print(f"❌ Error: Project '{project_name}' already exists " f"at {project_dir}")
        sys.exit(1)

    # Create the project
    try:
        create_project(
            project_dir=project_dir,
            project_name=project_name,
            description=args.description,
            author_name=args.author,
            author_email=args.email,
        )
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        if project_dir.exists():
            import shutil

            shutil.rmtree(project_dir)
        sys.exit(1)


if __name__ == "__main__":
    main()
