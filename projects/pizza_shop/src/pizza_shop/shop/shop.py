"""
Pizza Shop module.

This module contains the main PizzaShop class that manages the entire pizz
shop's operations, including orders, staff, and shop state.
"""

from typing import Any, Dict, List, Optional

from pizza_shop.cashier.cashier import Cashier
from pizza_shop.customer.customer import Customer
from pizza_shop.order.order import Order, OrderStatus
from pizza_shop.simulation.time import SimulationClock


class PizzaShop:
    """
    Main class representing the Pizza Shop.

    This class manages the entire pizza shop's operations, including:
    - Order management
    - Staff management
    - Customer management
    - Shop state and statistics
    """

    def __init__(
        self,
        name: str,
        opening_time: str = "10:00",
        closing_time: str = "22:00",
    ):
        """
        Initialize the pizza shop.

        Args:
            name: Name of the pizza shop
            opening_time: Shop opening time in "HH:MM" format
            closing_time: Shop closing time in "HH:MM" format
        """
        self.name = name
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.is_open = False

        # Staff
        self.cashiers: List[Cashier] = []
        # self.cooks: List[Cook] = []  # Temporarily commented out

        # Orders
        self.active_orders: Dict[str, Order] = {}
        self.completed_orders: List[Order] = []
        self.cancelled_orders: List[Order] = []

        # Customers
        self.customers: Dict[str, Customer] = {}

        # Simulation
        self.clock = SimulationClock()

    def open_shop(self) -> None:
        """Open the pizza shop for business."""
        self.is_open = True
        self.clock.start()
        print(f"{self.name} is now open! ({self.opening_time} - {self.closing_time})")

    def close_shop(self) -> None:
        """Close the pizza shop."""
        self.is_open = False
        self.clock.stop()
        print(f"{self.name} is now closed!")

    def add_cashier(self, cashier: Cashier) -> None:
        """Add a cashier to the shop."""
        self.cashiers.append(cashier)

    # def add_cook(self, cook: Cook) -> None:
    #     """
    #     Add a cook to the shop.
    #
    #     Args:
    #         cook: The Cook to add
    #     """
    #     self.cooks.append(cook)

    def create_order(self, customer: Customer, pizzas: List) -> Order:
        """
        Create a new order.

        Args:
            customer: The customer placing the order
            pizzas: List of Pizza objects in the order

        Returns:
            The created Order object with a generated order_id
        """
        order = Order(name=customer.name, pizzas=pizzas)
        self.active_orders[order.order_id] = order
        customer.place_order(order)
        # Add customer to customers dict if not already present
        if customer.customer_id not in self.customers:
            self.customers[customer.customer_id] = customer
        return order

    def complete_order(self, order_id: str) -> Optional[Order]:
        """
        Mark an order as completed.

        Args:
            order_id: ID of the order to complete

        Returns:
            The completed Order if found, None otherwise
        """
        if order_id in self.active_orders:
            order = self.active_orders.pop(order_id)
            order.update_status(OrderStatus.COMPLETED)
            self.completed_orders.append(order)
            return order
        return None

    def cancel_order(self, order_id: str) -> Optional[Order]:
        """
        Cancel an active order.

        Args:
            order_id: ID of the order to cancel

        Returns:
            The cancelled Order if found, None otherwise
        """
        if order_id in self.active_orders:
            order = self.active_orders.pop(order_id)
            order.update_status(OrderStatus.CANCELLED)
            self.cancelled_orders.append(order)
            return order
        return None

    def get_order_status(self, order_id: str) -> Optional[OrderStatus]:
        """
        Get the status of an order.

        Args:
            order_id: ID of the order to check

        Returns:
            The OrderStatus if found, None otherwise
        """
        # Check active orders first
        if order_id in self.active_orders:
            return self.active_orders[order_id].status

        # Check completed orders
        for order in self.completed_orders:
            if order.order_id == order_id:
                return order.status

        # Check cancelled orders
        for order in self.cancelled_orders:
            if order.order_id == order_id:
                return order.status

        return None

    def get_shop_statistics(self) -> Dict[str, Any]:
        """
        Get shop statistics.

        Returns:
            Dictionary containing various shop statistics
        """
        total_revenue = sum(order.total_price for order in self.completed_orders)

        return {
            "total_orders": len(self.completed_orders) + len(self.cancelled_orders),
            "active_orders": len(self.active_orders),
            "completed_orders": len(self.completed_orders),
            "cancelled_orders": len(self.cancelled_orders),
            "total_revenue": total_revenue,
            "average_order_value": (
                total_revenue / len(self.completed_orders)
                if self.completed_orders
                else 0
            ),
            "total_customers": len(self.customers),
            "current_time": self.clock.current_time,
        }

    def __str__(self) -> str:
        """String representation of the pizza shop."""
        stats = self.get_shop_statistics()
        return (
            f"Pizza Shop: {self.name}\n"
            f"Status: {'OPEN' if self.is_open else 'CLOSED'}\n"
            f"Active Orders: {stats['active_orders']} | "
            f"Completed: {stats['completed_orders']} | "
            f"Cancelled: {stats['cancelled_orders']}\n"
            f"Total Revenue: ${stats['total_revenue']:.2f}\n"
            f"Current Time: {self.clock.current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
