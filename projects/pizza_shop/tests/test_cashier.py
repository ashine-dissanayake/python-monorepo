from datetime import datetime
from unittest.mock import patch

from pizza_shop.cashier.cashier import Cashier
from pizza_shop.customer.customer import Customer
from pizza_shop.order.order import Order


def test_cashier_creation() -> None:
    """Test basic cashier creation with default and custom values."""
    # Test with minimal required fields
    cashier = Cashier(cashier_id="1", name="John Doe")
    assert cashier.cashier_id == "1"
    assert cashier.name == "John Doe"
    assert cashier.is_available is True
    assert cashier.current_customer is None

    # Test with all fields
    customer = Customer(customer_id="123", name="Jane Customer")
    cashier = Cashier(
        cashier_id="2",
        name="Jane Cashier",
        is_available=False,
        current_customer=customer,
    )
    assert cashier.cashier_id == "2"
    assert cashier.name == "Jane Cashier"
    assert cashier.is_available is False
    assert cashier.current_customer is customer


def test_create_customer() -> None:
    """Test creating a new customer through the cashier."""
    cashier = Cashier(cashier_id="1", name="John Doe")

    # Test creating a customer
    with patch("pizza_shop.cashier.cashier.datetime") as mock_datetime:
        # Mock the timestamp to a fixed value
        mock_datetime.now.return_value.timestamp.return_value = 1625000000.0
        customer = cashier.create_customer("New Customer")

    # Verify the customer was created with expected values
    assert customer.customer_id == "cust_1625000000"
    assert customer.name == "New Customer"
    assert customer.order is None
    assert isinstance(customer.arrival_time, datetime)

    # Verify the cashier's current_customer is not set by create_customer
    assert cashier.current_customer is None


def test_cashier_string_representation() -> None:
    """Test the string representation of the cashier."""
    # Test available cashier
    cashier = Cashier(cashier_id="1", name="John Doe")
    assert str(cashier) == "Cashier John Doe (available)"

    # Test unavailable cashier with a customer
    customer = Customer(customer_id="123", name="Jane Customer")
    cashier = Cashier(
        cashier_id="2",
        name="Jane Cashier",
        is_available=False,
        current_customer=customer,
    )
    assert str(cashier) == f"Cashier Jane Cashier (serving {customer})"

    # Test unavailable cashier with no customer (edge case)
    cashier.current_customer = None
    assert str(cashier) == "Cashier Jane Cashier (serving None)"


def test_cashier_availability() -> None:
    """Test the is_available property and its interaction with current_customer."""
    cashier = Cashier(cashier_id="1", name="John Doe")
    customer = Customer(customer_id="123", name="Jane Customer")

    # Initially available
    assert cashier.is_available is True

    # Assign a customer
    cashier.current_customer = customer

    # Should still be available (the property is independent of current_customer)
    assert cashier.is_available is True

    # Explicitly set to unavailable
    cashier.is_available = False
    assert cashier.is_available is False

    # Remove customer, should stay unavailable
    cashier.current_customer = None
    assert cashier.is_available is False


def test_cashier_with_order_management() -> None:
    """Test cashier interactions with customer orders."""
    # Create a cashier and customer
    cashier = Cashier(cashier_id="1", name="John Doe")
    customer = cashier.create_customer("Ordering Customer")

    # Create an order for the customer
    order = Order("Pizza Order")
    customer.place_order(order)

    # Assign customer to cashier and make cashier unavailable
    cashier.current_customer = customer
    cashier.is_available = False

    # Test cashier's string representation shows serving customer
    assert str(customer) in str(cashier)

    # Test cashier availability is independent of customer's order status
    assert cashier.current_customer is customer
    cashier.is_available = True
    assert str(cashier) == "Cashier John Doe (available)"
