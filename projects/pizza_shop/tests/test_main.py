import io
import sys

import pytest
from pizza_shop.main import main


def test_main_output() -> None:
    """Test that the main function prints the expected output."""
    # Redirect stdout to capture the output
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Call the main function
    main()

    # Get the output and restore stdout
    output = captured_output.getvalue().strip()
    sys.stdout = sys.__stdout__

    # Verify the output
    assert output == "Hello from pizza_shop!"


def test_main_execution() -> None:
    """Test that the main function can be called without errors."""
    # This test just verifies that the function runs without raising exceptions
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() raised {type(e).__name__} unexpectedly: {e}")


def test_main_called_via_module() -> None:
    """Test that the main function can be imported and called."""
    # This test verifies that the main module can be imported
    # and the main() function called
    # We've already tested the output of main() in test_main_output
    # The actual __main__ execution is better tested via integration tests
    from pizza_shop.main import main

    # Just verify main() can be called without errors
    main()
