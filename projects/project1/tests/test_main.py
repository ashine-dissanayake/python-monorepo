"""Tests for the main module."""

from src.main import greet


def test_greet() -> None:
    """Test the greet function with default argument."""
    assert greet() == "Hello, World!"


def test_greet_with_name() -> None:
    """Test the greet function with a custom name."""
    assert greet("Alice") == "Hello, Alice!"
