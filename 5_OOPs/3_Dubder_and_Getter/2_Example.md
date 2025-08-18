Let’s walk through that `InventoryItem` class step by step, seeing how each magic (dunder) method hooks into Python’s syntax and operators to give your custom class rich, predictable behavior.

---

## 1. Class Definition & Initialization

```python
class InventoryItem:
    """A class to demonstrate operator overloading for inventory management."""
    def __init__(self, name, quantity):
        self.name     = name      # e.g. "Widget"
        self.quantity = quantity  # e.g. 10
```

* **`__init__`** is called when you write `InventoryItem("Widget", 10)`.
* It simply stores the two attributes: `name` and `quantity`.

---

## 2. Developer-Friendly Representation

```python
    def __repr__(self):
        return f"InventoryItem(name='{self.name}', quantity={self.quantity})"
```

* **`__repr__`** defines how the object looks in the REPL, logs, or debugging.
* Returning this string makes it clear what object you have and its internal state.

---

## 3. Arithmetic Operators

### Addition: `+`

```python
    def __add__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem(self.name, self.quantity + other.quantity)
        raise ValueError("Cannot add items of different types.")
```

* **Called by**: `item1 + item2`.
* **Type check**: Ensures you only combine items of the *same* kind (`self.name == other.name`).
* **Result**: Returns a **new** `InventoryItem` whose `quantity` is the sum.
* **Error**: If you try to add apples to oranges, you get a clear `ValueError`.

### Subtraction: `-`

```python
    def __sub__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            if self.quantity >= other.quantity:
                return InventoryItem(self.name, self.quantity - other.quantity)
            raise ValueError("Cannot subtract more than the available quantity.")
        raise ValueError("Cannot subtract items of different types.")
```

* **Called by**: `item1 - item2`.
* **Extra logic**: Ensures you don’t go negative—good inventory hygiene!
* **Error**: Two distinct errors—one for mismatched names and one for insufficient stock.

### Multiplication: `*`

```python
    def __mul__(self, factor):
        if isinstance(factor, (int, float)):
            return InventoryItem(self.name, int(self.quantity * factor))
        raise ValueError("Multiplication factor must be a number.")
```

* **Called by**: `item * 3` or `3 * item` (thanks to Python’s commutative dispatch, the latter works if you also implement `__rmul__`).
* **Type check**: Only numeric factors.
* **Behavior**: Scales the quantity, returns a brand-new `InventoryItem`.

### True Division: `/`

```python
    def __truediv__(self, factor):
        if isinstance(factor, (int, float)) and factor != 0:
            return InventoryItem(self.name, int(self.quantity / factor))
        raise ValueError("Division factor must be a non-zero number.")
```

* **Called by**: `item / 2`.
* **Zero check**: Guards against division by zero.
* **Conversion**: Casts to `int` so you don’t end up with fractional items.

---

## 4. Comparison Operators

### Equality: `==`

```python
    def __eq__(self, other):
        if isinstance(other, InventoryItem):
            return (self.name == other.name and
                    self.quantity == other.quantity)
        return False
```

* **Called by**: `item1 == item2`.
* Only returns `True` if *both* name and quantity match exactly.
* Returns `False` (rather than error) when comparing to something else entirely.

### Less-Than: `<`

```python
    def __lt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity < other.quantity
        raise ValueError("Cannot compare items of different types.")
```

* **Called by**: `item1 < item2`.
* Only valid if the two items share the same `name`.
* Uses the natural numeric ordering on `quantity`.

### Greater-Than: `>`

```python
    def __gt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity > other.quantity
        raise ValueError("Cannot compare items of different types.")
```

* **Called by**: `item1 > item2`.
* Mirror of `__lt__`, comparing in the other direction.

---

## 5. Putting It All Together: Flow Example

```python
widgets_a = InventoryItem("Widget", 10)
widgets_b = InventoryItem("Widget", 5)

# Addition
widgets_c = widgets_a + widgets_b
# Internally: widgets_a.__add__(widgets_b)
# → returns InventoryItem("Widget", 15)

# Subtraction
widgets_d = widgets_c - InventoryItem("Widget", 3)
# Internally: widgets_c.__sub__(InventoryItem("Widget",3))
# → returns InventoryItem("Widget", 12)

# Comparison
print(widgets_d > InventoryItem("Widget", 10))  # True

# Multiplication
bulk = widgets_d * 2
# → InventoryItem("Widget", 24)

# Division
single = bulk / 4
# → InventoryItem("Widget", 6)
```

At each step, Python dispatches the operator to your magic method, performs your checks, and hands you back a fresh object (or raises an error), just as if you were working with built-ins like `int` or `list`.

---

## 6. Why This Matters

1. **Intuitive syntax**: `a + b` reads naturally, even for domain objects.
2. **Strong invariants**: Type and value checks inside each method keep your data consistent (no negative stock, no mixing of types).
3. **Immutability of operations**: Rather than mutating an existing object, each operator returns a new instance—safer in many applications.
4. **Polymorphism**: Code that works with any “+” or “<” stays generic, and your objects plug right in.

By mastering these dunder methods, you make your classes integrate seamlessly with Python’s own operators and functions, yielding code that’s both powerful and readable.
