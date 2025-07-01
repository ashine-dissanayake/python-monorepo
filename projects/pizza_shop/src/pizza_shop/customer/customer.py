from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from pizza_shop.order.order import Order, OrderStatus


@dataclass
class Customer:
    """
    Represents a customer in the pizza shop system.

    Attributes:
        customer_id: Unique identifier for the customer
        name: Customer's name
        arrival_time: When the customer arrived at the shop
        order: The customer's current order (None if they haven't ordered yet)
    """

    customer_id: str
    name: str
    arrival_time: datetime = field(default_factory=datetime.now)
    order: Optional[Order] = None

    def place_order(self, order: Order) -> None:
        """
        Assign an order to the customer.

        Args:
            order: The order to be assigned to the customer
        """
        self.order = order

    def cancel_order(self) -> bool:
        """
        Cancel the customer's current order if it's not already being prepared
        or completed.

        Returns:
            bool: True if the order was cancelled, False otherwise
        """
        if self.order is None:
            return False

        if self.order.status in [OrderStatus.PENDING, OrderStatus.PREPARING]:
            self.order.update_status(OrderStatus.CANCELLED)
            return True
        return False

    @property
    def has_active_order(self) -> bool:
        """Check if the customer has an active (not completed or cancelled) order."""
        if self.order is None:
            return False
        return self.order.status not in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]

    @property
    def order_size(self) -> int:
        """Get the number of pizzas in the customer's current order."""
        if self.order is None:
            return 0
        return self.order.order_size

    @property
    def total_price(self) -> float:
        """Get the total price of the customer's current order."""
        if self.order is None:
            return 0
        return self.order.total_price

    def __str__(self) -> str:
        status = "with order" if self.order else "without order"
        return f"Customer {self.name} ({status})"
