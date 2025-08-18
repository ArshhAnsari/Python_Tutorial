---

## Quick one-line summary

* **Class method** (`@classmethod`) is a method that gets the **class** (`cls`) as its first argument — use it to work with class-wide data or make alternative constructors.
* **Static method** (`@staticmethod`) is a plain function placed inside a class — it does **not** get `self` or `cls` and is used for utility functions logically related to the class.

---

## The three kinds (so you don’t mix them up)

### 1. Instance method (usual)

* Signature: `def foo(self, ...)`
* Gets the **instance** as `self`.
* Use when you need or change instance data (`self.x`).

```python
class A:
    def inst(self):
        print("I am an instance method", self)
```

Call: `obj.inst()`

### 2. Class method

* Decorator: `@classmethod`
* Signature: `def foo(cls, ...)`
* Gets the **class** as `cls` (not an instance).
* Use when you need to read/change class variables, or implement alternative constructors.

```python
class Employee:
    raise_amt = 1.05

    @classmethod
    def set_raise(cls, amount):
        cls.raise_amt = amount

    @classmethod
    def from_string(cls, s):
        first, last, pay = s.split("-")
        return cls(first, last, int(pay))
```

Call: `Employee.set_raise(1.06)` or `Employee.from_string("A-B-5000")`

**Important:** `cls` respects subclassing — calling the classmethod on a subclass will use that subclass as `cls`.

### 3. Static method

* Decorator: `@staticmethod`
* Signature: `def foo(... )` (no `self` or `cls`)
* It’s just a function grouped inside the class namespace.
* Use when you need a helper that is related to the class but doesn’t access class/instance data.

```python
class MathHelpers:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

# call:
MathHelpers.is_even(4)   # True
```

Call: `ClassName.method()` or `instance.method()` — both work.

---

## When to use which? (practical rules)

* If the method needs instance data → **instance method**.
* If the method needs class data or should construct an instance differently → **class method**.
* If the method is a utility that doesn’t touch class or instance data → **static method**.

---

## Small examples showing differences

```python
class C:
    count = 0

    def __init__(self):         # instance method used by constructor
        C.count += 1

    @classmethod
    def how_many(cls):          # class method reads class var
        return cls.count

    @staticmethod
    def greet(name):            # static method is just a helper
        return f"Hello, {name}"
```

Usage:

```python
c1 = C()
c2 = C()
print(C.how_many())         # 2
print(C.greet("Arsh"))      # "Hello, Arsh"
```

---

## Common pitfalls

* A static method **cannot** access `self` or `cls`. If you find yourself doing that, use a classmethod or instance method.
* Class methods change shared state — be cautious if many subclasses or threads interact with that state.
* `@classmethod` is handy for alternative constructors (`from_string`, `from_dict`), return `cls(...)` so callers get an instance.

---

**Q: What’s the simple difference between `@classmethod` and `@staticmethod` — and when should I use each?**

**A:** A `@classmethod` automatically receives the **class** (`cls`) as its first argument, so use it when you need to read or change class-wide data (class variables) or build alternative constructors (factories) that should create instances of the calling class or its subclasses; because it gets `cls`, it respects subclassing. A `@staticmethod` gets **no** automatic argument — it’s just a regular function placed inside the class namespace for organizational clarity, so use it for small helper utilities that are related to the class conceptually but don’t need access to `self` or `cls`. In short: if you need the class, use `@classmethod`; if you need nothing special, use `@staticmethod`.

---

**Q: How do I *access* or *call* class methods and static methods?**

**A:**

* **Class methods** (`@classmethod`) are called either on the class or on an instance, and Python will automatically pass the class as the first argument (`cls`). That means you can write `MyClass.my_classmethod(...)` or `my_obj.my_classmethod(...)` — both work, and inside the method `cls` will be the calling class (if called on a subclass, `cls` becomes that subclass). Use the class form to make your intent clear (e.g. `Employee.from_string(...)`), and remember classmethods are typically used as factories or to operate on class-level data.

```python
class A:
    @classmethod
    def show_cls(cls):
        print("cls is", cls)

A.show_cls()        # cls is <class '__main__.A'>
a = A()
a.show_cls()        # cls is still <class '__main__.A'>

class B(A): pass
B.show_cls()        # cls is <class '__main__.B'>  (respects subclassing)
```

* **Static methods** (`@staticmethod`) are also callable from the class or an instance, but they receive **no** automatic `self` or `cls`. They behave like plain functions stored on the class. Call them as `MyClass.my_staticmethod(...)` (preferred) or `my_obj.my_staticmethod(...)` (allowed). Because they’re unbound functions, `MyClass.sm is my_obj.sm` is `True` — there’s no special binding.

```python
class Util:
    @staticmethod
    def greet(name):
        return f"Hello, {name}"

print(Util.greet("Arsh"))   # "Hello, Arsh"
u = Util()
print(u.greet("Arsh"))      # same result, but calling via class is clearer
```

**Memory aid:**

* *Call class methods on the class (or instance) — they get `cls`.*
* *Call static methods on the class — they get nothing automatically.*

Use the class name to call either one for clarity: `Class.method(...)`.

---
