# Pizza Shop Simulation

A Python-based simulation of a pizza shop's order management system, featuring customer handling, order processing, and kitchen operations.

## Features

- **Customer Management**: Create and manage customer orders
- **Order Processing**: Handle order lifecycle from creation to completion
- **Kitchen Operations**: Manage pizza preparation with cooks
- **Payment Processing**: Handle transactions and order completion
- **Type Annotated**: Fully type-annotated code for better development experience

## Project Structure

```
pizza_shop/
├── src/
│   └── pizza_shop/
│       ├── cashier/         # Cashier operations and customer handling
│       ├── cook/            # Kitchen operations and pizza preparation
│       ├── customer/        # Customer entity and management
│       ├── order/           # Order processing and status tracking
│       └── pizza/           # Pizza definitions and pricing
└── tests/                   # Test files
```

## Installation

This project is part of a monorepo. To install it in development mode:

```bash
# From the root of the monorepo
pip install -e ./projects/pizza_shop
```

## Usage Examples

### Creating a New Order

```python
from pizza_shop.cashier import Cashier
from pizza_shop.cook import Cook
from pizza_shop.order import OrderStatus

# Initialize staff
cashier = Cashier(cashier_id="c1", name="Alice")
cook = Cook(cook_id="k1", name="Bob")

# Take an order
order, customer = cashier.take_order(
    customer_name="John Doe",
    pizzas=[
        {"name": "Margherita", "size": "large", "toppings": ["olives"]},
        {"name": "Pepperoni", "size": "medium"}
    ]
)

# Process payment
if order:
    payment = cashier.process_payment(order, customer, amount_paid=30.0)
    print(f"Payment successful! Change: ${payment['change']:.2f}" if payment['success'] else "Payment failed")

# Assign to cook
if order and cook.assign_order(order):
    print(f"{cook.name} is now preparing the order")
```

### Managing Orders

```python
# Check order status
print(f"Order status: {order.status.value}")

# Update order status
order.update_status(OrderStatus.PREPARING)
```

## Development

### Running Tests

```bash
# From the project directory
cd projects/pizza_shop
pytest
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- Flake8 for linting
- Mypy for static type checking

Run all checks:

```bash
black .
isort .
flake8 .
mypy .
```

## License

MIT
