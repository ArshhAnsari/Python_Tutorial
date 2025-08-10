# What is abstraction — the big idea (quick, practical intro)

**Abstraction** is an OOP principle that means *showing only what’s necessary and hiding the rest.* You work with a simplified interface and don’t need to know the internal details.

Real-world analogies:

* Driving a car: you use the steering wheel, pedals and indicators — you don’t need to know how the engine pistons move.
* Using a phone app: you tap buttons and see results — you don’t see the network calls, parsing, or database logic.

Why it matters in code:

* It keeps code easier to understand and reason about (you see the *what*, not the *how*).
* It separates *interface* from *implementation*, which helps multiple developers work together safely.
* It enables polymorphism: different objects can be used interchangeably if they follow the same abstract contract.

Use a simple rule of thumb: if you want to *require* subclasses to implement specific methods (so mistakes are caught early), use an ABC. If you only need optional compatibility and flexibility, favor duck typing or protocols.

---

An **abstract base class (ABC)** module says: *“Any concrete child must implement these methods.”*
If a subclass **does not** implement *all* the `@abstractmethod`s from its ABC, Python treats that subclass itself as **abstract**, and you **cannot create** (instantiate) objects from it. You must implement the required methods to make it a **concrete** class.

---

## Why this happens

* `@abstractmethod` marks methods as required.
* The ABC machinery (`ABCMeta`) tracks which abstract methods remain unimplemented.
* If a class still has abstract methods, trying to do `MyClass()` raises a `TypeError` telling you which abstract methods are missing.

---

## Minimal proof — example showing the error

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...
    @abstractmethod
    def perimeter(self): ...

# Subclass that forgets perimeter
class BadCircle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius * self.radius

# Try to instantiate
obj = BadCircle(2)
```

**Result:**
`TypeError: Can't instantiate abstract class BadCircle with abstract methods perimeter`

This is Python protecting you: `BadCircle` is still abstract because `perimeter` is missing.

---

## Fix: implement the missing methods

```python
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius ** 2
    def perimeter(self):
        return 2 * 3.14 * self.radius

c = Circle(2)
print(c.area(), c.perimeter())   # works
```

Now `Circle` is **concrete** and you can instantiate it.

---

## Subclass can still be abstract

If a subclass implements some but **not all** abstract methods, it remains abstract:

```python
class Partial(Shape):
    def area(self): return 0.0
# Partial still has abstract perimeter → cannot instantiate
```

So implementing **every** abstract method (directly or via some ancestor) is required.

---

## A few extra, important details

### 1. `@abstractmethod` can have an implementation

You can write:

```python
class A(ABC):
    @abstractmethod
    def f(self):
        print("default thing")
```

This still makes `f` abstract — subclass must override `f` before instantiation. The base implementation can be called by the subclass via `super().f()`.

### 2. You can declare abstract `@property`, `@classmethod`, `@staticmethod`

Examples:

```python
class X(ABC):
    @property
    @abstractmethod
    def value(self): ...
```

or

```python
class Y(ABC):
    @classmethod
    @abstractmethod
    def create(cls, data): ...
```

The decorator order matters for some combinations (put `@abstractmethod` *after* the other decorator as shown).

### 3. `register()` — virtual subclassing

You can make a class be treated as a virtual subclass:

```python
class Old:
    def area(self): ...
    def perimeter(self): ...

Shape.register(Old)
isinstance(Old(), Shape)  # True
```

**Note:** `register()` does not require `Old` to explicitly inherit from `Shape`; it also does not enforce method presence — it simply registers the class as a virtual subclass. Use carefully.

### 4. When are abstract checks enforced?

* The check that prevents instantiation happens at *instantiation time* (when you do `C()`) — but the class is flagged as abstract at class creation time if it has unimplemented abstract methods.

### 5. Why use ABCs?

* **Enforce an interface** so other developers (and your future self) can rely on methods being present.
* **Early failure**: you get a clear error rather than a runtime `AttributeError` later.
* **Documentation & tooling**: ABCs clarify the intended design and work well with type checkers and IDEs.

---

## Quick checklist for writing concrete subclasses of an ABC

1. List all `@abstractmethod` names in the base class.
2. Implement every one in your subclass (method signature must be compatible).
3. If your subclass does not implement all, it remains abstract — you cannot instantiate it.
4. If you need a default behavior, you can provide it in the ABC, but mark it `@abstractmethod` (still requires override).
5. Use `@property/@classmethod/@staticmethod` with `@abstractmethod` where appropriate.

---
