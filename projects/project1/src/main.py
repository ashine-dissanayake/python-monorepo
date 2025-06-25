"""Main module for Project 1.

This module demonstrates a simple Python package structure.
"""


def greet(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: Name to include in the greeting. Defaults to "World".

    Returns:
        A greeting message.
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet())  # pragma: no cover
