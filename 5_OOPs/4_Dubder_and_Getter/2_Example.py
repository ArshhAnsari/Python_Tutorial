'''
InventoryItem: a class demonstrating Python magic methods for operator overloading,
string representation, and comparison, enabling intuitive inventory management.
'''

class InventoryItem:
    """
    Represents a single type of inventory item with a name and quantity.
    Supports:
      - Arithmetic: +, -, *, /
      - Comparison: ==, <, >
      - String conversion: str(), repr()
    """

    def __init__(self, name: str, quantity: int):
        """
        Initialize an inventory item.
        :param name: The item name (e.g. 'Widget')
        :param quantity: Number of items in stock
        """
        self.name = name
        self.quantity = quantity

    def __repr__(self) -> str:
        """
        Developer-friendly representation:
        invoked by repr(item) or in interactive shell.
        """
        return f"InventoryItem(name='{self.name}', quantity={self.quantity})"

    def __str__(self) -> str:
        """
        User-friendly representation:
        invoked by str(item) or print(item).
        """
        return f"{self.quantity} x {self.name}"

    # -----------------------------
    # Arithmetic Operators
    # -----------------------------
    def __add__(self, other):
        """
        Add two InventoryItem objects with the same name.
        Returns a new InventoryItem; original objects are unchanged.
        """
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem(self.name, self.quantity + other.quantity)
        raise ValueError("Cannot add items of different types or names.")

    def __sub__(self, other):
        """
        Subtract quantity of another InventoryItem from this one.
        Quantity cannot go below zero; returns new InventoryItem.
        """
        if isinstance(other, InventoryItem) and self.name == other.name:
            if self.quantity >= other.quantity:
                return InventoryItem(self.name, self.quantity - other.quantity)
            raise ValueError("Cannot subtract more than the available quantity.")
        raise ValueError("Cannot subtract items of different types.")

    def __mul__(self, factor):
        """
        Scale quantity by a numeric factor; returns new InventoryItem.
        """
        if isinstance(factor, (int, float)):
            return InventoryItem(self.name, int(self.quantity * factor))
        raise ValueError("Multiplication factor must be a number.")

    def __truediv__(self, factor):
        """
        Divide quantity by a numeric factor; returns new InventoryItem.
        Division by zero is prohibited.
        """
        if isinstance(factor, (int, float)) and factor != 0:
            return InventoryItem(self.name, int(self.quantity / factor))
        raise ValueError("Division factor must be a non-zero number.")

    # -----------------------------
    # Comparison Operators
    # -----------------------------
    def __eq__(self, other) :
        """
        Equality: same type, name, and quantity.
        """
        if isinstance(other, InventoryItem):
            return (self.name == other.name and
                    self.quantity == other.quantity)
        return False

    def __lt__(self, other) :
        """
        Less-than: only valid between items of the same name.
        """
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity < other.quantity
        raise ValueError("Cannot compare items of different types.")

    def __gt__(self, other) :
        """
        Greater-than: only valid between items of the same name.
        """
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity > other.quantity
        raise ValueError("Cannot compare items of different types.")


# ------------------------------------------------
# Example Usage
# ------------------------------------------------
# Create two widget items
widgets_a = InventoryItem("Widget", 10)
widgets_b = InventoryItem("Widget", 5)

# Addition
widgets_c = widgets_a + widgets_b
print("Addition:", widgets_c) 
# Internally: widgets_a.__add__(widgets_b)
# → returns InventoryItem("Widget", 15)


# Subtraction
widgets_d = widgets_c - InventoryItem("Widget", 3)
print("Subtraction:", widgets_d)  # 12 x Widget
# Internally: widgets_c.__sub__(InventoryItem("Widget",3))
# → returns InventoryItem("Widget", 12)
    
# Comparison
print("Is widgets_d > widgets_b?", widgets_d > widgets_b)

# Multiplication
bulk = widgets_d * 2
print("Multiplication:", bulk)  # 24 x Widget
# Division
single = bulk / 4
print("Division:", single)  # 6 x Widget

# Equality
print("Are widgets_d and widgets_b equal?", widgets_d == widgets_b)