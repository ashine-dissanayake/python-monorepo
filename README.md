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

   When you're done working on the project, you can deactivate the virtual environment:
   ```bash
   deactivate
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Adding a New Project

Use the `create_project.py` script to create a new project with the standard structure:

```bash
./scripts/create_project.py project-name --description "Project description"
```

This will create a new directory under `projects/` with the following structure:

```
project-name/
├── pyproject.toml
├── README.md
├── src/
│   └── project_name/
│       ├── __init__.py
│       └── main.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

## Development Workflow

1. **Install a project in development mode**:
   ```bash
   cd projects/project-name
   pip install -e .
   ```

2. **Run tests**:
   ```bash
   # Run all tests
   pytest -v

   # Run tests with coverage
   pytest --cov=src --cov-report=term-missing
   ```

3. **Code quality checks**:
   ```bash
   # Format code
   black .
   isort .

   # Lint code
   flake8 .
   mypy .
   ```

## Development Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Write docstrings following [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Add type hints to all functions and methods
- Write tests for new features
- Run tests before committing
- Update documentation when making changes

## Tools Used

- [Pytest](https://docs.pytest.org/) - Testing framework
- [Black](https://black.readthedocs.io/) - Code formatting
- [isort](https://pycqa.github.io/isort/) - Import sorting
- [Flake8](https://flake8.pycqa.org/) - Linting
- [Mypy](http://mypy-lang.org/) - Static type checking
- [pre-commit](https://pre-commit.com/) - Git hooks
- [GitHub Actions](https://github.com/features/actions) - CI/CD
