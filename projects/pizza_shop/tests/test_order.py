from datetime import datetime

from pizza_shop.order.order import Order, OrderStatus
from pizza_shop.pizza.pizza import ExtraTopping, Pizza, PizzaSize


def test_order_creation() -> None:
    """Test basic order creation."""
    order = Order(name="John Doe")
    assert order.name == "John Doe"
    assert order.status == OrderStatus.PENDING
    assert order.pizzas == []
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)


def test_add_pizza() -> None:
    """Test adding pizzas to an order."""
    order = Order(name="Jane Smith")
    pizza1 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    pizza2 = Pizza(pizza_type="Pepperoni", size=PizzaSize.LARGE)

    order.add_pizza(pizza1)
    assert len(order.pizzas) == 1
    assert pizza1 in order.pizzas

    order.add_pizza(pizza2)
    assert len(order.pizzas) == 2
    assert pizza2 in order.pizzas


def test_update_status() -> None:
    """Test updating order status and timestamps."""
    # Setup
    order = Order(name="Bob Johnson")

    # Store initial timestamp
    initial_updated = order.updated_at

    # Update status
    order.update_status(OrderStatus.PREPARING)

    # Verify the status was updated
    assert (
        order.status == OrderStatus.PREPARING
    ), "Status should be updated to PREPARING"

    # Verify the timestamp was updated
    assert (
        order.updated_at > initial_updated
    ), "Updated timestamp should be after initial timestamp"


def test_multiple_status_updates() -> None:
    """Test multiple status updates to verify timestamp updates."""
    # Setup
    order = Order(name="Jane Smith")

    # First update
    order.update_status(OrderStatus.PREPARING)
    first_update_time = order.updated_at

    # Second update
    order.update_status(OrderStatus.READY)

    # Verify
    assert order.status == OrderStatus.READY
    assert (
        order.updated_at > first_update_time
    ), "Timestamp should be updated after second status change"


def test_total_items() -> None:
    """Test total items in the order."""
    order = Order(name="Alice Brown")
    assert order.total_items == 0

    order.add_pizza(Pizza(pizza_type="Margherita", size=PizzaSize.SMALL))
    assert order.total_items == 1

    order.add_pizza(Pizza(pizza_type="Pepperoni", size=PizzaSize.MEDIUM))
    assert order.total_items == 2


def test_total_price() -> None:
    """Test total price calculation."""
    order = Order(name="Charlie Davis")

    # Add a small margherita (8.99 + 1.00)
    order.add_pizza(Pizza(pizza_type="Margherita", size=PizzaSize.SMALL))
    assert abs(order.total_price - 9.99) < 0.001

    # Add a medium pepperoni with extra cheese (10.99 + 1.50 + 1.50)
    pizza = Pizza(pizza_type="Pepperoni", size=PizzaSize.MEDIUM)
    pizza.add_topping(ExtraTopping.EXTRA_CHEESE)
    order.add_pizza(pizza)

    expected_total = 9.99 + (10.99 + 1.50 + 1.50)
    assert abs(order.total_price - expected_total) < 0.001


def test_order_size() -> None:
    """Test order_size property (should be same as total_items)."""
    order = Order(name="Eve Wilson")
    assert order.order_size == 0

    order.add_pizza(Pizza(pizza_type="Margherita", size=PizzaSize.SMALL))
    assert order.order_size == 1

    order.add_pizza(Pizza(pizza_type="Pepperoni", size=PizzaSize.MEDIUM))
    assert order.order_size == 2
