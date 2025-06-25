"""Minimal Flask application."""

from typing import Tuple

from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route("/")  # type: ignore[misc]
def index() -> str:
    """Return a simple greeting."""
    return "<p>Hello, World!</p>"


@app.route("/health")  # type: ignore[misc]
def health_check() -> Tuple[Response, int]:
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application
    """
    return app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
