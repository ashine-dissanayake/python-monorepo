import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

from pizza_shop.pizza.pizza import Pizza
from pizza_shop.simulation.time import sim_clock


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
        order_id: Unique identifier for the order
        name: Name of the customer
        pizzas: List of Pizza objects in the order
        status: Current status of the order
        created_at: Timestamp when the order was created
        updated_at: Timestamp when the order was last updated
    """

    name: str
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pizzas: List[Pizza] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)
    estimated_prep_time: Optional[timedelta] = None
    actual_prep_time: Optional[timedelta] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Initialize timestamps using the simulation clock."""
        self.created_at = sim_clock.current_time
        self.updated_at = self.created_at
        self._calculate_estimated_prep_time()

    def _calculate_estimated_prep_time(self) -> None:
        """Calculate estimated preparation time based on order size and complexity."""
        base_time = timedelta(minutes=10)  # Base time for any order
        pizza_time = timedelta(minutes=3) * len(self.pizzas)
        self.estimated_prep_time = base_time + pizza_time

    def update_status(self, new_status: OrderStatus) -> None:
        """
        Update the order status and set the updated timestamp.

        Args:
            new_status: The new status to set for the order.

        Note:
            If status changes to COMPLETED, records the completion time.
        """
        old_status = self.status
        self.status = new_status
        self.updated_at = sim_clock.current_time

        if new_status == OrderStatus.COMPLETED and old_status != OrderStatus.COMPLETED:
            self.completed_at = self.updated_at
            self.actual_prep_time = self.completed_at - self.created_at

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

    @property
    def time_since_created(self) -> timedelta:
        """Return how long it's been since the order was created."""
        return sim_clock.current_time - self.created_at

    @property
    def time_in_current_status(self) -> timedelta:
        """Return how long the order has been in its current status."""
        return sim_clock.current_time - self.updated_at
