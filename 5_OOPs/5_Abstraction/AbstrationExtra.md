## Short idea of `register()`

`register()` makes a class be treated **as if it were a subclass** of an abstract base class (ABC) for the purposes of `isinstance()` and `issubclass()` checks — **without** changing actual inheritance. That’s why it’s called **virtual subclassing**.

* It does **not** make the registered class inherit code, attributes, or methods from the ABC.
* It does **not** enforce that the registered class actually implements the ABC’s abstract methods.
* It simply says: “For type-checking questions, consider this class a kind of the ABC.”

---

## Why this exists (intuition)

Imagine you have an old class written before you introduce an ABC interface. You want that class to be recognized as providing the expected behavior, but you don’t want or cannot change its inheritance. `register()` lets you declare that relationship externally, so libraries or code that check `isinstance(obj, MyABC)` will accept it.

Use cases:

* Retro-fitting old code to a new interface.
* Declaring that C-extension types or third-party classes conform to an ABC.
* Plugin or adapter systems where structural compatibility is enough.

---

## Minimal example

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class OldCircle:
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r * self.r

# Before registering:
print(issubclass(OldCircle, Shape))   # False
print(isinstance(OldCircle(2), Shape))# False

# Register OldCircle as a virtual subclass of Shape
Shape.register(OldCircle)

print(issubclass(OldCircle, Shape))    # True
print(isinstance(OldCircle(2), Shape)) # True
```

Important: `OldCircle` still doesn’t *inherit* from `Shape`, and nothing about its behavior changes. It simply *claims* to be a `Shape` for the checking APIs.

---

## What `register()` does (technical view, simplified)

* Internally, ABCs maintain a registry of classes that have been registered as virtual subclasses.
* `issubclass(X, ABC)` and `isinstance(x, ABC)` consult:

  1. Normal inheritance (MRO) checks,
  2. The registry of virtual subclasses,
  3. Cached results.
* `register()` adds the class to that registry. No MRO updates happen.

---

## Important caveats & gotchas

1. **No method enforcement**
   `register()` does not check whether the registered class actually implements the ABC’s abstract methods. You can register a class that lacks required methods, and `isinstance()` will still return `True`. This can hide bugs if code expects the methods to exist.

2. **No attribute/method inheritance**
   Registering does not copy methods. Calling `Shape.some_method()` on the registered class will fail unless that class actually has `some_method`.

3. **Not visible in MRO**
   `OldCircle.__mro__` (method resolution order) does not include `Shape`. Virtual subclassing is only for `isinstance`/`issubclass` checks.

4. **Decorator order for abstract methods**
   Registering doesn’t influence whether abstract methods are satisfied. If a real subclass (one that inherits from the ABC) fails to implement abstract methods, it remains abstract and cannot be instantiated. Registered classes are exempt from that check — they’re separate classes being *recognized* as conforming by the ABC.

5. **No official `unregister()`**
   There’s no public API to unregister; removing entries from the internal registry is possible but hacky and discouraged.

6. **Use with caution for API contracts**
   Because it doesn’t enforce structure, prefer explicit inheritance or Python `typing.Protocol` (structural typing) for stronger guarantees, especially in large codebases.

---

## Practical example showing differences

```python
from abc import ABC, abstractmethod

class Serializable(ABC):
    @abstractmethod
    def to_dict(self): ...
    
class OldUser:
    def __init__(self, name): self.name = name
    def to_dict(self): return {"name": self.name}

# OldUser behaves like Serializable (has to_dict)
print(isinstance(OldUser("A"), Serializable))   # False

# Register it
Serializable.register(OldUser)
print(isinstance(OldUser("A"), Serializable))   # True

# But registration doesn't add methods or check them:
class Broken:
    pass

Serializable.register(Broken)
print(isinstance(Broken(), Serializable))  # True  <-- dangerous if you expect to_dict to exist
# Broken().to_dict()  # AttributeError at runtime
```

This demonstrates the biggest pitfall: `isinstance()` can report `True`, but the object may not actually provide the required API.

---

## Alternatives & modern best practices

* **Prefer structural typing with `typing.Protocol`** (PEP 544) for static analysis and clearer intent in new code. Protocols are checked by static type checkers (mypy) and support duck-typing-like interfaces without runtime registration.
* Use **`register()`** when you need to integrate legacy or external classes into an ABC-based runtime check, and you *know* those classes actually implement the behavior — or as a pragmatic bridge.

Example with Protocol (simple):

```python
from typing import Protocol

# Declare a Protocol, which is a structural type hinting
# interface that is checked by static type checkers like mypy
class SerializableProto(Protocol):
    # A Protocol is a class that defines the methods or
    # properties that a class must have to be considered
    # a match for this type hint
    def to_dict(self) -> dict: ...

# A function that takes an object that is a subtype of
# SerializableProto and saves it to wherever
def save(obj: SerializableProto):
    # The type checker will enforce that the object passed
    # has a to_dict method, so you can be sure it's there
    print(obj.to_dict())  # static type checkers will enforce availability
```

---
## Key differences from `ABC.register()`:
* **Structural typing**: Protocols check for the actual presence of methods/properties, while ABCs rely on runtime registration (which doesn't verify the class actually implements the interface).
* **Static checkers**: Protocols are enforced by static type checkers like mypy, while ABCs are only checked at runtime.
* **No runtime impact**: Protocols don't affect the MRO, method lookup, or runtime checks; they only affect static type checking.

---

## Final summary (one-paragraph)

`ABC.register()` performs **virtual subclassing**: it marks a class as a subclass of an ABC for `isinstance`/`issubclass` tests without changing inheritance, MRO, or enforcing method implementation. It’s a pragmatic tool for compatibility and retrofitting, but because it does not verify that the registered class actually implements the ABC interface, use it carefully — prefer explicit inheritance or modern `Protocol`-based structural typing when you need stronger guarantees.

---
