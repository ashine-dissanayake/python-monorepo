"""
Time simulation for the pizza shop.

This module provides a simulated clock that can be used to track time in the pizza shop
simulation. The clock can be run in real-time or accelerated mode.
"""

import time
from datetime import datetime, timedelta
from typing import Callable, List, Optional


class SimulationClock:
    """
    A simulated clock for the pizza shop simulation.

    The clock can run in two modes:
    - Real-time mode: 1 second = 1 second
    - Accelerated mode: 1 second = N seconds (specified by time_scale)
    """

    def __init__(self, start_time: Optional[datetime] = None, time_scale: int = 1):
        """
        Initialize the simulation clock.

        Args:
            start_time: The starting time for the simulation. If None, uses current
                        time.
            time_scale: How many simulation seconds pass for each real second.
                        e.g., time_scale=60 means 1 real second = 1 simulation minute.
        """
        self._start_time = start_time or datetime.now()
        self._current_time = self._start_time
        self._time_scale = time_scale
        self._is_running = False
        self._event_handlers: List[Callable[["SimulationClock"], None]] = []
        self._last_update = time.monotonic()

    @property
    def current_time(self) -> datetime:
        """Get the current simulation time."""
        self._update_time()
        return self._current_time

    @property
    def is_running(self) -> bool:
        """Check if the simulation clock is running."""
        return self._is_running

    def start(self) -> None:
        """Start the simulation clock."""
        if not self._is_running:
            self._last_update = time.monotonic()
            self._is_running = True

    def stop(self) -> None:
        """Stop the simulation clock."""
        if self._is_running:
            self._update_time()
            self._is_running = False

    def reset(self) -> None:
        """Reset the simulation clock to the start time."""
        self._current_time = self._start_time
        self._last_update = time.monotonic()

    def add_time(self, delta: timedelta) -> None:
        """
        Add time to the simulation clock.

        Args:
            delta: The amount of time to add to the simulation.
        """
        if delta.total_seconds() > 0:
            self._current_time += delta
            self._trigger_events()

    def add_event_handler(self, handler: Callable[["SimulationClock"], None]) -> None:
        """
        Add an event handler that will be called when time advances.

        Args:
            handler: A function that takes the SimulationClock as an argument.
        """
        self._event_handlers.append(handler)

    def _update_time(self) -> None:
        """Update the current time based on real time passed."""
        if not self._is_running:
            return

        now = time.monotonic()
        elapsed = now - self._last_update
        if elapsed > 0:
            # Store the old time to check if it changed
            old_time = self._current_time
            self._current_time += timedelta(seconds=elapsed * self._time_scale)
            self._last_update = now

            # Only trigger events if time actually advanced
            if self._current_time > old_time:
                self._trigger_events()

    def _trigger_events(self) -> None:
        """Trigger all registered event handlers."""
        for handler in self._event_handlers:
            handler(self)


# Global simulation clock instance
sim_clock = SimulationClock()
