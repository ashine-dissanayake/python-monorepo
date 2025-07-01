"""
Tests for the PizzaShop class.
"""

from typing import List

import pytest
from pizza_shop.cashier.cashier import Cashier
from pizza_shop.customer.customer import Customer
from pizza_shop.order.order import OrderStatus
from pizza_shop.pizza.pizza import ExtraTopping, Pizza, PizzaSize
from pizza_shop.shop.shop import PizzaShop
from pizza_shop.simulation.time import sim_clock


@pytest.fixture  # type: ignore[misc]
def sample_pizza_shop() -> PizzaShop:
    """Create a sample PizzaShop instance for testing."""
    shop = PizzaShop("Test Pizza Shop", "10:00", "22:00")
    # Add a cashier
    cashier = Cashier("John Doe", "C001")
    shop.add_cashier(cashier)
    return shop


@pytest.fixture  # type: ignore[misc]
def sample_customer() -> Customer:
    """Create a sample customer for testing."""
    return Customer("Test Customer", "test@example.com")


@pytest.fixture  # type: ignore[misc]
def sample_pizzas() -> List[Pizza]:
    """Create sample pizzas for testing."""
    return [
        Pizza("Margherita", PizzaSize.MEDIUM),
        Pizza("Pepperoni", PizzaSize.LARGE, [ExtraTopping.EXTRA_CHEESE]),
    ]


class TestPizzaShop:
    """Test cases for the PizzaShop class."""

    def test_initialization(self) -> None:
        """Test that a PizzaShop is initialized correctly."""
        shop = PizzaShop("Test Shop", "09:00", "23:00")

        assert shop.name == "Test Shop"
        assert shop.opening_time == "09:00"
        assert shop.closing_time == "23:00"
        assert not shop.is_open
        assert len(shop.cashiers) == 0
        assert len(shop.active_orders) == 0
        assert len(shop.completed_orders) == 0
        assert len(shop.cancelled_orders) == 0
        assert len(shop.customers) == 0

    def test_open_shop(self, sample_pizza_shop: PizzaShop) -> None:
        """Test opening the shop."""
        shop = sample_pizza_shop
        shop.open_shop()
        assert shop.is_open
        assert shop.clock.is_running
        # Clean up
        shop.close_shop()
        sim_clock.reset()

    def test_close_shop(self, sample_pizza_shop: PizzaShop) -> None:
        """Test closing the shop."""
        shop = sample_pizza_shop
        shop.open_shop()  # Need to be open first to close
        shop.close_shop()
        assert not shop.is_open
        assert not shop.clock.is_running
        # Clean up
        sim_clock.reset()

    def test_add_cashier(self) -> None:
        """Test adding cashiers to the shop."""
        shop = PizzaShop("Test Shop")
        cashier1 = Cashier("Cashier One", "C001")
        cashier2 = Cashier("Cashier Two", "C002")

        shop.add_cashier(cashier1)
        assert len(shop.cashiers) == 1
        assert cashier1 in shop.cashiers

        shop.add_cashier(cashier2)
        assert len(shop.cashiers) == 2
        assert cashier2 in shop.cashiers

    def test_create_order(
        self,
        sample_pizza_shop: PizzaShop,
        sample_customer: Customer,
        sample_pizzas: List[Pizza],
    ) -> None:
        """Test creating a new order."""
        shop = sample_pizza_shop
        shop.open_shop()

        # Create an order
        order = shop.create_order(sample_customer, sample_pizzas)

        # Verify the order was created correctly
        assert order is not None
        assert order.order_id in shop.active_orders
        assert shop.active_orders[order.order_id] == order
        assert len(order.pizzas) == 2
        assert order.status == OrderStatus.PENDING

        # Verify customer association
        assert sample_customer.order == order

        # Clean up
        shop.close_shop()
        sim_clock.reset()

    def test_complete_order(
        self,
        sample_pizza_shop: PizzaShop,
        sample_customer: Customer,
        sample_pizzas: List[Pizza],
    ) -> None:
        """Test completing an order."""
        shop = sample_pizza_shop
        shop.open_shop()

        # Create and complete an order
        order = shop.create_order(sample_customer, sample_pizzas)
        completed_order = shop.complete_order(order.order_id)

        # Verify the order was completed
        assert completed_order is not None
        assert completed_order.status == OrderStatus.COMPLETED
        assert order.order_id not in shop.active_orders
        assert completed_order in shop.completed_orders

        # Clean up
        shop.close_shop()
        sim_clock.reset()

    def test_cancel_order(
        self,
        sample_pizza_shop: PizzaShop,
        sample_customer: Customer,
        sample_pizzas: List[Pizza],
    ) -> None:
        """Test cancelling an order."""
        shop = sample_pizza_shop
        shop.open_shop()

        # Create and cancel an order
        order = shop.create_order(sample_customer, sample_pizzas)
        cancelled_order = shop.cancel_order(order.order_id)

        # Verify the order was cancelled
        assert cancelled_order is not None
        assert cancelled_order.status == OrderStatus.CANCELLED
        assert order.order_id not in shop.active_orders
        assert cancelled_order in shop.cancelled_orders

        # Clean up
        shop.close_shop()
        sim_clock.reset()

    def test_get_order_status(
        self,
        sample_pizza_shop: PizzaShop,
        sample_customer: Customer,
        sample_pizzas: List[Pizza],
    ) -> None:
        """Test getting the status of an order."""
        shop = sample_pizza_shop
        shop.open_shop()

        # Test with non-existent order
        assert shop.get_order_status("nonexistent") is None

        # Test with active order
        order = shop.create_order(sample_customer, sample_pizzas)
        assert shop.get_order_status(order.order_id) == OrderStatus.PENDING

        # Test with completed order
        shop.complete_order(order.order_id)
        assert shop.get_order_status(order.order_id) == OrderStatus.COMPLETED

        # Clean up
        shop.close_shop()
        sim_clock.reset()

    def test_shop_statistics(
        self,
        sample_pizza_shop: PizzaShop,
        sample_customer: Customer,
        sample_pizzas: List[Pizza],
    ) -> None:
        """Test getting shop statistics."""
        shop = sample_pizza_shop
        shop.open_shop()

        # Create some orders
        order1 = shop.create_order(sample_customer, sample_pizzas)
        order2 = shop.create_order(sample_customer, sample_pizzas[:1])  # Only one pizza

        # Complete one order, cancel the other
        shop.complete_order(order1.order_id)
        shop.cancel_order(order2.order_id)

        # Get statistics
        stats = shop.get_shop_statistics()

        # Verify statistics
        assert stats["total_orders"] == 2
        assert stats["active_orders"] == 0
        assert stats["completed_orders"] == 1
        assert stats["cancelled_orders"] == 1
        assert stats["total_revenue"] > 0
        # Verify customer tracking
        assert (
            stats["total_customers"] == 1
        )  # Should be 1 since we used the same customer for both orders

        # Clean up
        shop.close_shop()
        sim_clock.reset()

    def test_string_representation(self, sample_pizza_shop: PizzaShop) -> None:
        """Test the string representation of the shop."""
        shop = sample_pizza_shop
        shop_str = str(shop)

        assert shop.name in shop_str
        assert "CLOSED" in shop_str  # Shop starts closed

        # Test with shop open
        shop.open_shop()
        shop_str_open = str(shop)
        assert "OPEN" in shop_str_open

        # Clean up
        shop.close_shop()
        sim_clock.reset()

    def test_cancel_nonexistent_order(self, sample_pizza_shop: PizzaShop) -> None:
        """Test cancelling an order that doesn't exist."""
        shop = sample_pizza_shop
        result = shop.cancel_order("nonexistent_order_id")
        assert result is None

    def test_complete_nonexistent_order(self, sample_pizza_shop: PizzaShop) -> None:
        """Test completing an order that doesn't exist."""
        shop = sample_pizza_shop
        result = shop.complete_order("nonexistent_order_id")
        assert result is None

    def test_get_order_status_nonexistent(self, sample_pizza_shop: PizzaShop) -> None:
        """Test getting status of an order that doesn't exist."""
        shop = sample_pizza_shop
        result = shop.get_order_status("nonexistent_order_id")
        assert result is None
