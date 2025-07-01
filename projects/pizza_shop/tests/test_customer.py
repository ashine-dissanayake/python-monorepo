from datetime import datetime, timedelta

from pizza_shop.customer.customer import Customer
from pizza_shop.order.order import Order, OrderStatus
from pizza_shop.pizza.pizza import Pizza, PizzaSize


def test_customer_creation() -> None:
    """Test basic customer creation with required attributes."""
    # Test with minimal required fields
    customer = Customer(customer_id="123", name="John Doe")
    assert customer.customer_id == "123"
    assert customer.name == "John Doe"
    assert customer.order is None
    assert isinstance(customer.arrival_time, datetime)

    # Test with all fields
    order_time = datetime.now() - timedelta(minutes=10)
    order = Order(name="Jane Smith's Order")
    customer = Customer(
        customer_id="456", name="Jane Smith", arrival_time=order_time, order=order
    )
    assert customer.customer_id == "456"
    assert customer.name == "Jane Smith"
    assert customer.arrival_time == order_time
    assert customer.order is order


def test_place_order() -> None:
    """Test assigning an order to a customer."""
    # Setup
    customer = Customer(customer_id="123", name="John Doe")
    order = Order(name="John's Order")

    # Test initial state
    assert customer.order is None

    # Test placing first order
    customer.place_order(order)
    assert customer.order is order


def test_replace_order() -> None:
    """Test replacing an existing order with a new one."""
    # Setup
    customer = Customer(customer_id="124", name="Jane Doe")
    first_order = Order(name="First Order")

    # Place first order
    customer.place_order(first_order)
    assert customer.order is first_order

    # Replace with new order
    new_order = Order(name="New Order")
    customer.place_order(new_order)
    assert customer.order is new_order


def test_cancel_order() -> None:
    """Test canceling a customer's order."""
    # Create a customer with a pending order
    customer = Customer(customer_id="123", name="John Doe")
    order = Order(name="John's Order")
    customer.place_order(order)

    # Cancel the order (should succeed for PENDING status)
    assert customer.cancel_order() is True
    assert customer.order is not None  # Add None check
    assert customer.order.status == OrderStatus.CANCELLED

    # Try to cancel again (should fail as it's already cancelled)
    assert customer.cancel_order() is False

    # Test with a PREPARING order (should be cancellable according to implementation)
    preparing_order = Order(name="Preparing Order")
    preparing_order.update_status(OrderStatus.PREPARING)
    customer.place_order(preparing_order)
    assert customer.cancel_order() is True  # Should be able to cancel PREPARING orders
    assert customer.order is not None  # Add None check
    assert customer.order.status == OrderStatus.CANCELLED  # Status should be updated

    # Test with no order
    customer = Customer(customer_id="789", name="No Order")
    assert customer.order is None  # Verify no order exists
    assert customer.cancel_order() is False  # No order to cancel


def test_has_no_active_order_initially() -> None:
    """Test that a new customer has no active order."""
    customer = Customer(customer_id="123", name="John Doe")
    assert customer.has_active_order is False


def test_has_active_order_with_pending() -> None:
    """Test that a customer with a pending order has an active order."""
    customer = Customer(customer_id="124", name="Jane Doe")
    order = Order(name="Jane's Order")
    customer.place_order(order)
    assert customer.has_active_order is True


def test_has_active_order_with_preparing() -> None:
    """Test that a customer with a preparing order has an active order."""
    customer = Customer(customer_id="125", name="Jim Doe")
    order = Order(name="Jim's Order")
    customer.place_order(order)
    order.update_status(OrderStatus.PREPARING)
    assert customer.has_active_order is True


def test_has_active_order_with_ready() -> None:
    """Test that a customer with a ready order has an active order."""
    customer = Customer(customer_id="126", name="Jill Doe")
    order = Order(name="Jill's Order")
    customer.place_order(order)
    order.update_status(OrderStatus.READY)
    assert customer.has_active_order is True


def test_has_no_active_order_after_completion() -> None:
    """Test that a customer with a completed order has no active order."""
    customer = Customer(customer_id="127", name="Jack Doe")
    order = Order(name="Jack's Order")
    customer.place_order(order)
    order.update_status(OrderStatus.COMPLETED)
    assert customer.has_active_order is False


def test_has_no_active_order_after_cancellation() -> None:
    """Test that a customer with a cancelled order has no active order."""
    customer = Customer(customer_id="128", name="Jill Smith")
    order = Order(name="Jill's Cancelled Order")
    customer.place_order(order)
    order.update_status(OrderStatus.CANCELLED)
    assert customer.has_active_order is False


def test_order_size() -> None:
    """Test getting the number of pizzas in the customer's order."""
    customer = Customer(customer_id="123", name="John Doe")

    # No order
    assert customer.order_size == 0

    # Create an order with pizzas
    order = Order(name="John's Order")
    pizza1 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    pizza2 = Pizza(pizza_type="Pepperoni", size=PizzaSize.LARGE)
    order.add_pizza(pizza1)
    order.add_pizza(pizza2)

    # Add order to customer
    customer.place_order(order)
    assert customer.order_size == 2

    # Remove a pizza
    order.pizzas.remove(
        pizza1
    )  # Using direct list operation since remove_pizza doesn't exist
    assert customer.order_size == 1


def test_total_price() -> None:
    """Test getting the total price of the customer's order."""
    customer = Customer(customer_id="123", name="John Doe")

    # No order
    assert customer.total_price == 0

    # Create an order with a pizza
    order = Order(name="John's Order")
    pizza = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    order.add_pizza(pizza)

    # Add order to customer
    customer.place_order(order)
    expected_price = pizza.total_price
    assert abs(customer.total_price - expected_price) < 0.001

    # Add another pizza
    pizza2 = Pizza(pizza_type="Pepperoni", size=PizzaSize.LARGE)
    order.add_pizza(pizza2)
    expected_price += pizza2.total_price
    assert abs(customer.total_price - expected_price) < 0.001


def test_string_representation() -> None:
    """Test the string representation of a customer."""
    # Customer without order
    customer1 = Customer(customer_id="123", name="John Doe")
    assert str(customer1) == "Customer John Doe (without order)"

    # Customer with order
    customer2 = Customer(customer_id="456", name="Jane Smith")
    order = Order(name="Jane's Order")
    customer2.place_order(order)
    assert str(customer2) == "Customer Jane Smith (with order)"

    # Test name with special characters
    customer3 = Customer(customer_id="789", name="O'Conner")
    assert str(customer3) == "Customer O'Conner (without order)"
