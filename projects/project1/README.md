# Project 1

A sample Python project in the monorepo.

## Description

This is a sample project that demonstrates the structure and organization of Python projects within this monorepo.

## Installation

This project is part of a monorepo. To install it in development mode:

```bash
# From the root of the monorepo
pip install -e ./projects/project1
```

## Usage

```python
from project1.main import greet

print(greet("Python Developer"))  # Output: Hello, Python Developer!
```

## Development

### Running Tests

```bash
# From the project directory
cd projects/project1
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
