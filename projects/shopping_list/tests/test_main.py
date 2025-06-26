"""Tests for the main module."""

import pytest
from shopping_list.main import main


def test_main(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "Hello from shopping_list!" in captured.out
