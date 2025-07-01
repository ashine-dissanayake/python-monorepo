"""
Pizza Shop Demo

This script demonstrates how to use the PizzaShop class to manage a pizza shop's
operations.
"""

import os
import sys

from pizza_shop.cashier.cashier import Cashier

# from pizza_shop.cook import Cook  # Temporarily commented out
from pizza_shop.customer.customer import Customer
from pizza_shop.pizza.pizza import ExtraTopping, Pizza, PizzaSize
from pizza_shop.shop import PizzaShop

# Add the project root to the Python path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)


def main() -> None:
    # Create a new pizza shop
    print("=== Setting up the Pizza Shop ===")
    shop = PizzaShop(
        name="Mario's Pizzeria", opening_time="10:00", closing_time="22:00"
    )

    # Hire some staff
    cashier1 = Cashier("C001", "Alice")
    # cook1 = Cook("K001", "Bob")  # Temporarily commented out

    shop.add_cashier(cashier1)
    # shop.add_cook(cook1)  # Temporarily commented out

    # Open the shop
    shop.open_shop()

    # Create some customers
    customer1 = Customer("CUST001", "John Doe")
    customer2 = Customer("CUST002", "Jane Smith")

    # Create some pizzas
    margherita = Pizza("Margherita", PizzaSize.MEDIUM)
    pepperoni = Pizza("Pepperoni", PizzaSize.LARGE)
    pepperoni.add_topping(ExtraTopping.EXTRA_CHEESE)

    veggie = Pizza("Veggie", PizzaSize.MEDIUM)
    veggie.add_topping(ExtraTopping.MUSHROOMS)
    veggie.add_topping(ExtraTopping.GREEN_PEPPERS)

    # Place some orders
    print("\n=== Placing Orders ===")
    order1 = shop.create_order(customer1, [margherita, pepperoni])
    order2 = shop.create_order(customer2, [veggie])

    print(f"Order #{order1.order_id} created for {customer1.name}")
    print(f"Order #{order2.order_id} created for {customer2.name}")

    # Show order status
    print("\n=== Order Status ===")
    print(f"Order #{order1.order_id} status: {order1.status.value}")
    print(f"Order #{order2.order_id} status: {order2.status.value}")

    # Complete an order
    print("\n=== Completing Order ===")
    completed_order = shop.complete_order(order1.order_id)
    if completed_order:
        print(f"Completed order #{completed_order.order_id}")
        print(f"Total: ${completed_order.total_price:.2f}")

    # Show shop statistics
    print("\n=== Shop Statistics ===")
    stats = shop.get_shop_statistics()
    print(f"Active Orders: {stats['active_orders']}")
    print(f"Completed Orders: {stats['completed_orders']}")
    print(f"Total Revenue: ${stats['total_revenue']:.2f}")

    # Close the shop
    print("\n=== Closing Time ===")
    shop.close_shop()

    # Final shop status
    print("\n=== Final Shop Status ===")
    print(shop)


if __name__ == "__main__":
    main()
