# shopping_list

A Python project

## Description

A Python project in the monorepo.

## Installation

This project is part of a monorepo. To install it in development mode:

```bash
# From the root of the monorepo
pip install -e ./projects/shopping_list
```

## Usage

```python
from shopping_list.main import main

if __name__ == "__main__":
    main()
```

## Development

### Running Tests

```bash
# From the project directory
cd projects/shopping_list
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
