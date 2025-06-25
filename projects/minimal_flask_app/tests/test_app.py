"""Tests for the Flask application."""

from typing import Generator

import pytest
from flask.testing import FlaskClient
from minimal_flask_app.main import create_app


@pytest.fixture  # type: ignore[misc]
def client() -> Generator[FlaskClient, None, None]:
    """Create a test client for the Flask application.

    Yields:
        FlaskClient: A test client for the Flask application.
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_index_route(client: FlaskClient) -> None:
    """Test the index route.

    Args:
        client: Test client for the Flask application.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<p>Hello, World!</p>" in response.data


def test_health_check_route(client: FlaskClient) -> None:
    """Test the health check route.

    Args:
        client: Test client for the Flask application.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_nonexistent_route(client: FlaskClient) -> None:
    """Test a non-existent route returns 404.

    Args:
        client: Test client for the Flask application.
    """
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_create_app() -> None:
    """Test the create_app factory function."""
    app = create_app()
    assert app is not None
    assert app.name == "minimal_flask_app.main"
