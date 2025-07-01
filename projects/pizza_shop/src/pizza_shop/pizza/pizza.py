from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Dict, List, Optional


class PizzaSize(Enum):
    """Available pizza sizes with their base prices."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    @property
    def base_price(self) -> float:
        """Get the base price for this pizza size."""
        prices = {
            PizzaSize.SMALL: 8.99,
            PizzaSize.MEDIUM: 10.99,
            PizzaSize.LARGE: 12.99,
        }
        return prices[self]


class ExtraTopping(Enum):
    """Available extra toppings with their prices."""

    PEPPERONI = "pepperoni"
    MUSHROOMS = "mushrooms"
    ONIONS = "onions"
    SAUSAGE = "sausage"
    BACON = "bacon"
    EXTRA_CHEESE = "extra cheese"
    BLACK_OLIVES = "black olives"
    GREEN_PEPPERS = "green peppers"
    PINEAPPLE = "pineapple"
    SPINACH = "spinach"

    @property
    def price(self) -> float:
        """Get the price for this extra topping."""
        prices = {
            ExtraTopping.PEPPERONI: 2.50,
            ExtraTopping.MUSHROOMS: 1.50,
            ExtraTopping.ONIONS: 1.00,
            ExtraTopping.SAUSAGE: 2.50,
            ExtraTopping.BACON: 2.00,
            ExtraTopping.EXTRA_CHEESE: 1.50,
            ExtraTopping.BLACK_OLIVES: 1.50,
            ExtraTopping.GREEN_PEPPERS: 1.00,
            ExtraTopping.PINEAPPLE: 1.50,
            ExtraTopping.SPINACH: 1.50,
        }
        return prices[self]

    def __str__(self) -> str:
        return self.value


@dataclass(init=False)
class Pizza:
    """
    Represents a pizza in the pizza shop system.

    Attributes:
        pizza_type: Name of the pizza (e.g., "Margherita", "Pepperoni")
        size: Size of the pizza (PizzaSize enum value)
        extra_toppings: List of extra toppings on the pizza
    """

    def __init__(
        self,
        pizza_type: str,
        size: "PizzaSize",
        extra_toppings: Optional[List["ExtraTopping"]] = None,
    ) -> None:
        self._pizza_type = pizza_type
        self._size = size
        self._extra_toppings: List[ExtraTopping] = (
            extra_toppings if extra_toppings is not None else []
        )

    @property
    def pizza_type(self) -> str:
        """Get the pizza type."""
        return self._pizza_type

    @property
    def size(self) -> "PizzaSize":
        """Get the pizza size."""
        return self._size

    @property
    def extra_toppings(self) -> List["ExtraTopping"]:
        """Get the list of extra toppings."""
        return (
            self._extra_toppings.copy()
        )  # Return a copy to prevent external modifications

    # Base prices and toppings for different pizza types
    PIZZA_TYPE_INFO: ClassVar[Dict[str, Dict]] = {
        "margherita": {
            "base_price": 1.00,
            "base_toppings": ["tomato sauce", "mozzarella", "basil"],
        },
        "pepperoni": {
            "base_price": 1.50,
            "base_toppings": ["tomato sauce", "mozzarella", "pepperoni"],
        },
        "vegetarian": {
            "base_price": 1.25,
            "base_toppings": [
                "tomato sauce",
                "mozzarella",
                "mushrooms",
                "bell peppers",
                "onions",
                "olives",
            ],
        },
        "hawaiian": {
            "base_price": 1.75,
            "base_toppings": ["tomato sauce", "mozzarella", "ham", "pineapple"],
        },
        "meat_lovers": {
            "base_price": 2.00,
            "base_toppings": [
                "tomato sauce",
                "mozzarella",
                "pepperoni",
                "sausage",
                "bacon",
                "ham",
            ],
        },
    }

    @property
    def base_price(self) -> float:
        """Calculate the base price of the pizza based on size and type."""
        # Convert pizza_type to lowercase and replace spaces with underscores
        type_key = self.pizza_type.lower().replace(" ", "_")
        default_price: Dict[str, float] = {"base_price": 1.00}
        type_info = self.PIZZA_TYPE_INFO.get(type_key, default_price)
        base_price: float = type_info.get("base_price", 1.00)
        return float(self.size.base_price + base_price)

    @property
    def all_toppings(self) -> List[str]:
        """Get a list of all toppings including base and extra toppings."""
        # Convert pizza_type to lowercase and replace spaces with underscores
        type_key = self.pizza_type.lower().replace(" ", "_")
        default_toppings: Dict[str, List[str]] = {"base_toppings": []}
        type_info = self.PIZZA_TYPE_INFO.get(type_key, default_toppings)
        base_toppings: List[str] = type_info.get("base_toppings", [])
        extra_toppings: List[str] = [t.value for t in self.extra_toppings]
        return base_toppings + extra_toppings

    @property
    def toppings_price(self) -> float:
        """Calculate the total price of all extra toppings."""
        return sum(topping.price for topping in self.extra_toppings)

    @property
    def total_price(self) -> float:
        """Calculate the total price of the pizza including all toppings."""
        return self.base_price + self.toppings_price

    def add_topping(self, topping: ExtraTopping) -> None:
        """Add an extra topping to the pizza."""
        if topping not in self._extra_toppings:
            self._extra_toppings.append(topping)

    def remove_topping(self, topping: ExtraTopping) -> bool:
        """
        Remove a topping from the pizza.

        Returns:
            bool: True if topping was removed, False if not found
        """
        if topping in self._extra_toppings:
            self._extra_toppings.remove(topping)
            return True
        return False

    def __eq__(self, other: object) -> bool:
        """Two pizzas are equal if they have the same type, size, and toppings."""
        if not isinstance(other, Pizza):
            return False
        return (
            self.pizza_type.lower() == other.pizza_type.lower()
            and self.size == other.size
            and set(self.extra_toppings) == set(other.extra_toppings)
        )

    def __hash__(self) -> int:
        """Make Pizza hashable so it can be used in sets and as dictionary keys."""
        return hash(
            (self.pizza_type.lower(), self.size, frozenset(self.extra_toppings))
        )

    def __str__(self) -> str:
        base_str = f"{self.pizza_type.title()} ({self.size.value})"
        all_toppings = self.all_toppings
        if all_toppings:
            return f"{base_str} with {', '.join(all_toppings)}"
        return base_str
