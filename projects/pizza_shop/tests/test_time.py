"""
Tests for the time simulation module.
"""

import time
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from pizza_shop.simulation.time import SimulationClock


def test_simulation_clock_initialization() -> None:
    """Test that the simulation clock initializes correctly."""
    clock = SimulationClock()
    assert isinstance(clock.current_time, datetime)
    assert not clock.is_running


def test_simulation_clock_start_stop() -> None:
    """Test starting and stopping the simulation clock."""
    clock = SimulationClock()

    # Test starting the clock
    clock.start()
    assert clock.is_running

    # Test stopping the clock
    clock.stop()
    assert not clock.is_running


def test_simulation_clock_add_time() -> None:
    """Test adding time to the simulation clock."""
    clock = SimulationClock()
    initial_time = clock.current_time

    # Add 5 minutes to the clock
    clock.add_time(timedelta(minutes=5))
    assert clock.current_time == initial_time + timedelta(minutes=5)

    # Test with negative time (should not change the time)
    clock.add_time(timedelta(minutes=-10))
    assert clock.current_time == initial_time + timedelta(minutes=5)


def test_simulation_clock_reset() -> None:
    """Test resetting the simulation clock."""
    clock = SimulationClock()
    initial_time = clock.current_time

    # Add some time and then reset
    clock.add_time(timedelta(hours=1))
    clock.reset()

    # Clock should be back to the initial time
    assert clock.current_time == initial_time


def test_simulation_clock_event_handlers() -> None:
    """Test event handlers are called when time advances."""
    clock = SimulationClock()

    # Create a mock event handler
    mock_handler = MagicMock()

    # Add the event handler
    clock.add_event_handler(mock_handler)

    # Add some time - this should trigger the event handler
    clock.add_time(timedelta(minutes=1))

    # Check the handler was called with the clock instance
    mock_handler.assert_called_once_with(clock)


def test_simulation_clock_time_scale() -> None:
    """Test the time scale functionality."""
    # Create a clock with a time scale of 2 (time passes twice as fast)
    clock = SimulationClock(time_scale=2)
    clock.start()

    # Get the initial time
    start_time = clock.current_time

    # Wait a short time
    time.sleep(0.1)

    # Check that the clock advanced by about 0.2 seconds (0.1 * 2)
    time_diff = (clock.current_time - start_time).total_seconds()
    assert 0.18 <= time_diff <= 0.22  # Allow for some timing variability

    clock.stop()


def test_global_simulation_clock() -> None:
    """Test the global simulation clock instance."""
    from pizza_shop.simulation.time import sim_clock

    # Just verify the global instance exists and has the expected type
    assert isinstance(sim_clock, SimulationClock)
    assert isinstance(sim_clock.current_time, datetime)
