from typing import List

from pizza_shop.pizza.pizza import ExtraTopping, Pizza, PizzaSize


def test_extra_topping_string_representation() -> None:
    """Test the string representation of ExtraTopping enum values."""
    assert str(ExtraTopping.PEPPERONI) == "pepperoni"
    assert str(ExtraTopping.MUSHROOMS) == "mushrooms"
    assert str(ExtraTopping.EXTRA_CHEESE) == "extra cheese"
    assert str(ExtraTopping.BLACK_OLIVES) == "black olives"
    assert str(ExtraTopping.GREEN_PEPPERS) == "green peppers"
    assert str(ExtraTopping.PINEAPPLE) == "pineapple"
    assert str(ExtraTopping.SPINACH) == "spinach"


def test_pizza_creation() -> None:
    """Test basic pizza creation with required attributes."""
    pizza = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    assert pizza.pizza_type == "Margherita"
    assert pizza.size == PizzaSize.MEDIUM
    assert pizza.extra_toppings == []


def test_pizza_with_extra_toppings() -> None:
    """Test pizza creation with extra toppings."""
    pizza = Pizza(
        pizza_type="Pepperoni",
        size=PizzaSize.LARGE,
        extra_toppings=[ExtraTopping.EXTRA_CHEESE, ExtraTopping.MUSHROOMS],
    )
    assert len(pizza.extra_toppings) == 2
    assert ExtraTopping.EXTRA_CHEESE in pizza.extra_toppings
    assert ExtraTopping.MUSHROOMS in pizza.extra_toppings


def test_pizza_base_price() -> None:
    """Test base price calculation for different pizza types and sizes."""
    # Test medium margherita (base price 10.99 + 1.00 for margherita)
    pizza1 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    expected_price1 = 10.99 + 1.00
    assert (
        abs(pizza1.base_price - expected_price1) < 0.001
    ), f"Expected {expected_price1}, got {pizza1.base_price}"

    # Test large meat lovers (base price 12.99 + 2.00 for meat lovers)
    pizza2 = Pizza(pizza_type="meat_lovers", size=PizzaSize.LARGE)
    expected_price2 = 12.99 + 2.00
    assert (
        abs(pizza2.base_price - expected_price2) < 0.001
    ), f"Expected {expected_price2}, got {pizza2.base_price}"


def test_pizza_total_price() -> None:
    """Test total price calculation including extra toppings."""
    # Pizza with no extra toppings
    pizza1 = Pizza(pizza_type="Margherita", size=PizzaSize.SMALL)
    base_price = 8.99 + 1.00  # Small base + margherita base
    assert abs(pizza1.total_price - base_price) < 0.001

    # Pizza with extra toppings
    pizza2 = Pizza(
        pizza_type="Vegetarian",
        size=PizzaSize.MEDIUM,
        extra_toppings=[ExtraTopping.EXTRA_CHEESE, ExtraTopping.ONIONS],
    )
    base_price = 10.99 + 1.25  # Medium base + vegetarian base
    toppings_price = 1.50 + 1.00  # extra cheese + onions
    assert abs(pizza2.total_price - (base_price + toppings_price)) < 0.001


def test_pizza_description() -> None:
    """Test the string representation of the pizza."""
    pizza = Pizza(
        pizza_type="Hawaiian",
        size=PizzaSize.LARGE,
        extra_toppings=[ExtraTopping.EXTRA_CHEESE],
    )
    description = str(pizza).lower()
    assert "hawaiian" in description
    assert "large" in description
    assert "extra cheese" in description
    assert "tomato sauce" in description
    assert "ham" in description
    assert "pineapple" in description
    assert "mozzarella" in description


def test_pizza_equality() -> None:
    """Test that two pizzas with the same attributes are considered equal."""
    pizza1 = Pizza(
        pizza_type="Pepperoni",
        size=PizzaSize.MEDIUM,
        extra_toppings=[ExtraTopping.EXTRA_CHEESE],
    )
    pizza2 = Pizza(
        pizza_type="Pepperoni",
        size=PizzaSize.MEDIUM,
        extra_toppings=[ExtraTopping.EXTRA_CHEESE],
    )
    assert pizza1 == pizza2


def test_pizza_inequality() -> None:
    """Test that pizzas with different attributes are not equal."""
    base_pizza = Pizza(pizza_type="Margherita", size=PizzaSize.SMALL)

    # Different type
    pizza1 = Pizza(pizza_type="Pepperoni", size=PizzaSize.SMALL)
    assert base_pizza != pizza1

    # Different size
    pizza2 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    assert base_pizza != pizza2

    # Different toppings
    pizza3 = Pizza(
        pizza_type="Margherita",
        size=PizzaSize.SMALL,
        extra_toppings=[ExtraTopping.MUSHROOMS],
    )
    assert base_pizza != pizza3

    # Different toppings (order shouldn't matter)
    pizza4 = Pizza(
        pizza_type="Margherita",
        size=PizzaSize.SMALL,
        extra_toppings=[ExtraTopping.MUSHROOMS, ExtraTopping.ONIONS],
    )
    pizza5 = Pizza(
        pizza_type="Margherita",
        size=PizzaSize.SMALL,
        extra_toppings=[ExtraTopping.ONIONS, ExtraTopping.MUSHROOMS],
    )
    assert pizza4 == pizza5  # Order of toppings shouldn't matter


def test_add_topping() -> None:
    """Test adding toppings to a pizza."""
    # Create a basic pizza with no extra toppings
    pizza = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    assert len(pizza.extra_toppings) == 0

    # Add one topping
    pizza.add_topping(ExtraTopping.MUSHROOMS)
    assert ExtraTopping.MUSHROOMS in pizza.extra_toppings
    assert len(pizza.extra_toppings) == 1

    # Add another topping
    pizza.add_topping(ExtraTopping.BACON)
    assert ExtraTopping.BACON in pizza.extra_toppings
    assert len(pizza.extra_toppings) == 2

    # Adding the same topping again should not create duplicates
    pizza.add_topping(ExtraTopping.MUSHROOMS)
    assert len(pizza.extra_toppings) == 2  # Still only 2 unique toppings

    # Verify the price was updated correctly
    expected_price = (
        pizza.base_price + ExtraTopping.MUSHROOMS.price + ExtraTopping.BACON.price
    )
    assert abs(pizza.total_price - expected_price) < 0.001


def test_remove_topping() -> None:
    """Test removing toppings from a pizza."""
    # Create a pizza with some toppings
    pizza = Pizza(
        pizza_type="Pepperoni",
        size=PizzaSize.LARGE,
        extra_toppings=[
            ExtraTopping.EXTRA_CHEESE,
            ExtraTopping.ONIONS,
            ExtraTopping.MUSHROOMS,
        ],
    )

    # Remove an existing topping
    assert pizza.remove_topping(ExtraTopping.ONIONS) is True
    assert ExtraTopping.ONIONS not in pizza.extra_toppings
    assert len(pizza.extra_toppings) == 2

    # Try to remove a topping that's not on the pizza
    assert pizza.remove_topping(ExtraTopping.BACON) is False
    assert len(pizza.extra_toppings) == 2  # No change

    # Remove another topping
    assert pizza.remove_topping(ExtraTopping.EXTRA_CHEESE) is True
    assert ExtraTopping.EXTRA_CHEESE not in pizza.extra_toppings
    assert len(pizza.extra_toppings) == 1

    # Verify the price was updated correctly
    expected_price = pizza.base_price + ExtraTopping.MUSHROOMS.price
    assert abs(pizza.total_price - expected_price) < 0.001


def test_pizza_string_representation() -> None:
    """Test the string representation of the pizza."""
    # Test with no extra toppings
    pizza1 = Pizza(pizza_type="Margherita", size=PizzaSize.SMALL)
    description1 = str(pizza1).lower()
    assert "margherita" in description1
    assert "small" in description1
    assert "tomato sauce" in description1
    assert "mozzarella" in description1
    assert "basil" in description1

    # Test with extra toppings
    pizza2 = Pizza(
        pizza_type="Hawaiian",
        size=PizzaSize.MEDIUM,
        extra_toppings=[ExtraTopping.EXTRA_CHEESE, ExtraTopping.BACON],
    )
    description2 = str(pizza2).lower()
    assert "hawaiian" in description2
    assert "medium" in description2
    assert "tomato sauce" in description2
    assert "mozzarella" in description2
    assert "ham" in description2
    assert "pineapple" in description2
    assert "extra cheese" in description2
    assert "bacon" in description2

    # Test string representation after modifying toppings
    pizza2.remove_topping(ExtraTopping.BACON)
    description3 = str(pizza2).lower()
    assert "bacon" not in description3  # Should no longer be in the description
    assert "extra cheese" in description3  # Should still be there


def test_pizza_equality_edge_cases() -> None:
    """Test edge cases for pizza equality comparison."""
    # Test equality with non-Pizza object (line 159)
    pizza = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    assert not pizza == "not a pizza"  # This tests line 159

    # Test case-insensitive comparison of pizza types
    pizza1 = Pizza(pizza_type="margherita", size=PizzaSize.MEDIUM)
    pizza2 = Pizza(pizza_type="MARGHERITA", size=PizzaSize.MEDIUM)
    assert pizza1 == pizza2  # Should be equal despite case difference

    # Test with empty toppings
    pizza3 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM, extra_toppings=[])
    pizza4 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    assert pizza3 == pizza4  # Should be equal (None vs empty list for toppings)


def test_pizza_hashing() -> None:
    """Test that Pizza objects can be used in sets and as dict keys."""
    # Create some pizzas
    pizza1 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    pizza2 = Pizza(pizza_type="Margherita", size=PizzaSize.MEDIUM)
    pizza3 = Pizza(pizza_type="Pepperoni", size=PizzaSize.LARGE)

    # Test that equal pizzas have the same hash
    assert hash(pizza1) == hash(pizza2)

    # Test that different pizzas have different hashes
    # Note: Small chance of hash collision, but very unlikely
    assert hash(pizza1) != hash(pizza3)

    # Test using Pizza as dictionary key (tests both __hash__ and __eq__)
    menu = {}
    menu[pizza1] = "First pizza"
    menu[pizza2] = "Second pizza"  # Should overwrite the first one
    menu[pizza3] = "Third pizza"

    assert len(menu) == 2  # pizza1 and pizza2 are equal, so they count as one key
    assert menu[pizza1] == "Second pizza"
    assert menu[pizza3] == "Third pizza"

    # Test using Pizza in a set (tests both __hash__ and __eq__)
    pizza_set = {pizza1, pizza2, pizza3}
    assert len(pizza_set) == 2  # pizza1 and pizza2 are equal
    assert pizza1 in pizza_set
    assert pizza3 in pizza_set


def test_pizza_string_representation_edge_cases() -> None:
    """Test edge cases for string representation (line 173)."""
    # Test with a pizza type that has no base toppings in PIZZA_TYPE_INFO
    # This tests the fallback case in all_toppings property
    pizza = Pizza(pizza_type="NonexistentPizza", size=PizzaSize.SMALL)
    description = str(pizza).lower()
    assert "nonexistentpizza" in description
    assert "small" in description

    # Test with a pizza that has no toppings at all (shouldn't happen in practice,
    # but good to test). This tests the case where all_toppings returns an empty
    # list (line 173)
    class TestPizza(Pizza):
        @property
        def all_toppings(self) -> List[str]:
            return []

    test_pizza = TestPizza(pizza_type="Test", size=PizzaSize.MEDIUM)
    assert (
        str(test_pizza) == "Test (medium)"
    )  # Should not include "with" when there are no toppings
