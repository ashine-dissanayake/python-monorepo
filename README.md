# Python Monorepo

This repository contains multiple Python projects organized in a monorepo structure.

## Structure

```
python-monorepo/
├── .github/               # GitHub workflows and templates
├── .vscode/               # VSCode settings
├── docs/                  # Documentation
├── projects/              # Individual Python projects
│   ├── project1/          # Example project 1
│   │   ├── src/           # Source code
│   │   ├── tests/         # Unit and integration tests
│   │   ├── pyproject.toml # Project-specific dependencies
│   │   └── README.md      # Project documentation
│   └── project2/          # Example project 2
├── scripts/               # Utility scripts
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml         # Root project configuration
├── README.md              # This file
└── requirements-dev.txt    # Development dependencies
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-monorepo
   ```

2. **Set up the development environment**
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Adding a New Project

1. Create a new directory under `projects/`
2. Set up a standard Python project structure
3. Add a `pyproject.toml` for project-specific dependencies
4. Document the project in its `README.md`

## Development Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Write docstrings following [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Add type hints to all functions and methods
- Write tests for new features
- Run tests before committing
- Update documentation when making changes

## Tools Used

- [Poetry](https://python-poetry.org/) - Dependency management
- [Pytest](https://docs.pytest.org/) - Testing framework
- [Black](https://black.readthedocs.io/) - Code formatting
- [isort](https://pycqa.github.io/isort/) - Import sorting
- [Flake8](https://flake8.pycqa.org/) - Linting
- [Mypy](http://mypy-lang.org/) - Static type checking
- [pre-commit](https://pre-commit.com/) - Git hooks
