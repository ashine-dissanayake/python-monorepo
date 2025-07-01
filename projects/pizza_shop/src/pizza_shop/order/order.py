from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from pizza_shop.pizza.pizza import Pizza


class OrderStatus(Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Order:
    """
    Represents a customer's pizza order.

    Attributes:
        name: Name of the customer
        pizzas: List of Pizza objects in the order
        status: Current status of the order
        created_at: Timestamp when the order was created
        updated_at: Timestamp when the order was last updated
    """

    name: str
    pizzas: List[Pizza] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_status(self, new_status: OrderStatus) -> None:
        """Update the order status and set the updated timestamp."""
        self.status = new_status
        self.updated_at = datetime.now()

    def add_pizza(self, pizza: Pizza) -> None:
        """Add a pizza to the order."""
        self.pizzas.append(pizza)
        self.updated_at = datetime.now()

    @property
    def total_items(self) -> int:
        """Return the total number of pizzas in the order."""
        return len(self.pizzas)

    @property
    def order_size(self) -> int:
        """Return the number of pizzas in the order."""
        return self.total_items

    @property
    def total_price(self) -> float:
        """Return the total price of the order."""
        return sum(pizza.total_price for pizza in self.pizzas)
