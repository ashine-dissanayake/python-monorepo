"""Minimal Flask application."""

from typing import Tuple

from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Return a simple greeting.

    Returns:
        str: A simple HTML greeting.
    """
    return "<p>Hello, World!</p>"


@app.route("/health")
def health_check() -> Tuple[Response, int]:
    """Health check endpoint.

    Returns:
        Tuple[Response, int]: A JSON response with status and HTTP status code.
    """
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
