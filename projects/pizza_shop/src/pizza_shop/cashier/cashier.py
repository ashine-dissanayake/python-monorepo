from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pizza_shop.customer.customer import Customer


@dataclass
class Cashier:
    """
    Represents a cashier in the pizza shop who handles orders and payments.

    Attributes:
        cashier_id: Unique identifier for the cashier
        name: Name of the cashier
        is_available: Whether the cashier is available to take new customers
        current_customer: The customer currently being served
    """

    cashier_id: str
    name: str
    is_available: bool = True
    current_customer: Optional[Customer] = None

    def create_customer(self, name: str) -> Customer:
        """
        Create a new customer.

        Args:
            name: The name of the customer

        Returns:
            Customer: The newly created customer
        """
        # In a real application, you'd want to generate a unique customer ID
        customer_id = f"cust_{int(datetime.now().timestamp())}"
        return Customer(customer_id=customer_id, name=name)

    def __str__(self) -> str:
        status = (
            "available" if self.is_available else f"serving {self.current_customer}"
        )
        return f"Cashier {self.name} ({status})"
