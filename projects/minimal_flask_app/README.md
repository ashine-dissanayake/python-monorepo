# Minimal Flask App

A lightweight Flask web application with health check endpoint.

## Features

- Simple "Hello, World!" endpoint
- Health check endpoint
- Test coverage
- Pre-commit hooks for code quality

## Installation

This project is part of a monorepo. To install it in development mode:

```bash
# From the root of the monorepo
pip install -e ./projects/minimal_flask_app

# Install development dependencies
pip install -e "./projects/minimal_flask_app[dev]"
```

## Running the Application

### Development Server

To start the development server:

```bash
# From the project root
python -m projects.minimal_flask_app.src.minimal_flask_app.main
```

The server will start on `http://localhost:5000` by default.

### Available Endpoints

- `GET /` - Returns a "Hello, World!" message
- `GET /health` - Health check endpoint

### Stopping the Server

To stop the server, press `Ctrl+C` in the terminal where it's running.

If the server was started in the background, you can stop it by finding and killing the process:

```bash
# Find the process ID (PID)
lsof -i :5000

# Kill the process (replace PID with the actual process ID)
kill -9 PID

# Or kill all Python processes (be careful with this in shared environments)
pkill -f "python -m projects.minimal_flask_app"
```

## Development

### Running Tests

Run the test suite with coverage:

```bash
# From the project root
cd projects/minimal_flask_app
pytest -v --cov=src --cov-report=term-missing
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- Flake8 for linting
- Mypy for static type checking

Run all code quality checks:

```bash
black .
isort .
flake8 .
mypy .
mypy .
```

## License

MIT
