"""
Time Simulation Demo for Pizza Shop

This script demonstrates how to use the time simulation features in the pizza shop.
It shows how to create orders, advance time, and track order status changes.
"""

import os
import sys
import time
from datetime import timedelta

from pizza_shop.order.order import Order, OrderStatus
from pizza_shop.pizza.pizza import ExtraTopping, Pizza, PizzaSize
from pizza_shop.simulation.time import SimulationClock

# Add the project root to the Python path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)


def print_order_status(order: Order) -> None:
    """Print the current status of an order with timing information."""
    print(f"\n=== Order for {order.name} ===")
    print(f"Status: {order.status.value.upper()}")
    print(f"Created: {order.created_at}")
    print(f"Last updated: {order.updated_at}")
    print(f"Time since created: {order.time_since_created}")
    print(f"Time in current status: {order.time_in_current_status}")

    if order.estimated_prep_time:
        print(f"Estimated prep time: {order.estimated_prep_time}")
    if order.actual_prep_time:
        print(f"Actual prep time: {order.actual_prep_time}")
    if order.completed_at:
        print(f"Completed at: {order.completed_at}")


class TimeAdvanceCallback:
    """Callback class to handle time advancement events."""

    def __init__(self) -> None:
        self.last_second = -1  # Initialize to -1 to trigger first print

    def __call__(self, clock: SimulationClock) -> None:
        """Handle time advancement events."""
        current_time = clock.current_time
        current_second = int(current_time.timestamp())

        if current_second > self.last_second:
            self.last_second = current_second
            print(f"\n[Simulation Time: {current_time.strftime('%H:%M:%S')}")


# Create the callback instance
time_advance_callback = TimeAdvanceCallback()


def main() -> None:
    # Set up the simulation clock
    # 1 second real time = 1 minute simulation time
    sim_clock = SimulationClock(
        time_scale=60
    )  # 1 real second = 60 simulation seconds (1 minute)
    sim_clock.add_event_handler(time_advance_callback)
    sim_clock.start()

    print("=== Pizza Shop Time Simulation ===")
    print("Starting simulation...")
    print(f"Simulation start time: {sim_clock.current_time}")

    # Create an order
    print("\n=== Creating a new order ===")
    order = Order(name="John Doe")

    # Add some pizzas to the order
    margherita = Pizza("Margherita", PizzaSize.MEDIUM)
    pepperoni = Pizza("Pepperoni", PizzaSize.LARGE)
    pepperoni.add_topping(ExtraTopping.EXTRA_CHEESE)

    order.add_pizza(margherita)
    order.add_pizza(pepperoni)

    print(f"Created order with {order.total_items} pizzas")
    print(f"Estimated prep time: {order.estimated_prep_time}")

    # Simulate order processing
    print("\n=== Processing order ===")
    print("Order received and queued for preparation...")
    order.update_status(OrderStatus.PREPARING)
    print_order_status(order)

    # Simulate time passing (5 minutes)
    print("\n=== Time passing (5 minutes) ===")
    sim_clock.add_time(timedelta(minutes=5))
    # Add a small delay to let the clock update
    time.sleep(0.1)
    print_order_status(order)

    # Complete the order
    print("\n=== Completing order ===")
    order.update_status(OrderStatus.COMPLETED)
    print_order_status(order)

    # Show final simulation time
    print("\n=== Simulation Complete ===")
    print(f"Total simulation time: {sim_clock.current_time - sim_clock.current_time}")
    print(f"Real time elapsed: {time.monotonic():.1f} seconds")

    # Stop the simulation clock
    sim_clock.stop()


if __name__ == "__main__":
    main()
