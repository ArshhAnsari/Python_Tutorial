# Encapsulation

**Encapsulation** is the principle of bundling data (attributes) and behavior (methods) inside a class while controlling access to that data to enforce rules, maintain invariants, and allow internal changes without affecting external code.

---

Imagine a toy robot:

* The robot’s **insides** (battery, circuits) are delicate.
* You interact with the robot via buttons and commands (its **methods**) — you don’t open the robot and poke at wires.
* The robot’s case prevents accidental damage and provides a stable, simple interface.

In Python:

* The **class** is the robot case.
* **Attributes** = the robot’s internal state (battery level).
* **Methods** = the robot’s buttons (charge(), move()).
* Encapsulation ensures other code interacts with the robot correctly.

---

## Public vs Protected vs “Private” in Python

Python uses conventions rather than strict access modifiers:

* `public_attr` — accessible by everyone (normal attribute).
* `_protected_attr` — single underscore: a convention indicating “internal; don’t touch outside this class or module.” Subclasses can access it.
* `__private_attr` — double underscore: name-mangling makes it harder to access from outside. Python rewrites `__x` to `_ClassName__x`.

**Important:** name-mangling is not true privacy — it’s a safety/namespace mechanism.

Example:

```python
class A:
    def __init__(self):
        self._internal = 1        # convention: internal
        self.__very_private = 2   # name-mangled to _A__very_private

a = A()
print(a._internal)          # works (but you shouldn't in normal code)
print(a._A__very_private)   # also works if necessary (not recommended)
```

---

## Encapsulation in practice — use `@property` to control access

A common pattern: create a public, computed attribute backed by an internal value. This allows changes to internals without altering the public interface.

**Example — Car with an odometer:**

```python
class Car:
    def __init__(self, make, model, year):
        self.make = make                  # public
        self.model = model                # public
        self.year = year                  # public
        self._odometer_km = 0.0           # protected internal representation

    @property
    def odometer_km(self) -> float:
        """Read-only view in kilometers."""
        return self._odometer_km

    @property
    def odometer_miles(self) -> float:
        # computed attribute - converts km to miles on access
        return self._odometer_km * 0.621371

    def drive_km(self, km: float):
        if km < 0:
            raise ValueError("Cannot drive negative kilometers")
        self._odometer_km += km
```

**Why this is beneficial:**

* External code can easily read `car.odometer_miles`.
* Modifications are controlled through `drive_km()`, allowing validation.
* Internal changes (e.g., storing odometer as meters) can be made without affecting callers.

---

## Getters / Setters / Deleters: when to use them

* Use a **property getter** for computed values or when read access requires laziness or formatting.
* Use a **setter** when assignment requires validation, normalization, or side effects.
* Use a **deleter** for meaningful cleanup with `del obj.x`.

Example with setter:

```python
class Person:
    def __init__(self, first, last):
        self._first = first
        self._last = last

    @property
    def fullname(self):
        return f"{self._first} {self._last}"

    @fullname.setter
    def fullname(self, val):
        first, last = val.split(" ", 1)
        self._first, self._last = first, last
```

This maintains the `p.fullname = "A B"` syntax while controlling name storage.

---

## Why encapsulation matters — benefits

1. **Invariants**: Maintain valid object state. Example: bank accounts shouldn’t go negative unless allowed — check in `withdraw()` method.
2. **Safe internal changes**: Change representation (e.g., km to meters, caching) without breaking callers.
3. **Clear interface**: Users interact via a simple set of methods/attributes.
4. **Testing & reasoning**: Small, protected internal surfaces reduce complexity and make bugs easier to find.
5. **Security & safety**: Minimizes accidental misuse.

---

## Common mistakes & pitfalls

* **Over-encapsulation**: Hiding everything makes the class awkward to use. Provide sensible, small interfaces.
* **Relying on `__private` for security**: Name-mangling is not security—it's convenience. Do not store secrets expecting them to be truly private.
* **Exposing internals directly**: `obj._data = external_list` can lead to callers mutating internal lists. Instead, return copies or use tuples, or provide controlled operations.

Example pitfall:

```python
class Bad:
    def __init__(self, items):
        self.items = items   # direct ref to caller's list

lst = [1,2]
b = Bad(lst)
lst.append(3)   # mutates b.items unexpectedly
```

Better:

```python
self._items = list(items)   # copy
def get_items(self):
    return tuple(self._items)  # immutable view
```

---

## Encapsulation patterns

* **Read-only property**:

```python
@property
def id(self):
    return self._id   # no setter -> read-only
```

* **Validated setter**:

```python
@age.setter
def age(self, value):
    if value < 0: raise ValueError
    self._age = value
```

* **Lazy property (cache result on first call)**:

```python
@property
def expensive(self):
    if self._expensive is None:
        self._expensive = compute()
    return self._expensive
```

* **Immutable public interface with controlled mutation**: provide methods like `add()`, `remove()` instead of exposing underlying structure.

---

## Final example — improved Car with full encapsulation

```python
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self._odometer_m = 0.0   # internal meters

    @property
    def odometer_km(self):
        return self._odometer_m / 1000.0

    @odometer_km.setter
    def odometer_km(self, km):
        if km < 0:
            raise ValueError("odometer cannot be negative")
        self._odometer_m = float(km) * 1000.0

    def drive_km(self, km):
        if km < 0:
            raise ValueError("Cannot drive negative kilometers")
        self._odometer_m += km * 1000.0

    def __repr__(self):
        return f"Car({self.make!r}, {self.model!r}, {self.year!r}, {self.odometer_km:.1f} km)"
```

This class:

* Stores odometer in meters internally (`_odometer_m`) — internal detail.
* Exposes `odometer_km` as the public interface (read/write) with validation.
* Provides `drive_km()` for controlled mutation.
* Uses `__repr__` to display the class in a useful way.

---