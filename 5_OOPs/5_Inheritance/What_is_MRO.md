## What is MRO? (one-line)

**MRO is the order Python follows when it looks for a method or attribute on a class or instance in multiple-inheritance situations.** It decides *which* parent’s method runs when more than one parent provides the same method.

Think: when you call `obj.foo()`, Python asks, “Which class should I check first for `foo`?” MRO is the rulebook that answers that.

---

## Tiny analogy

Imagine a family tree where a child asks, “Who tells me how to make breakfast?” You check the child first, then parents in a particular order. If both mom and dad offer different recipes, you follow the family’s agreed order (MRO) to pick whose recipe to use.

---

## Single inheritance (easy)

If `B` inherits from `A`:

```python
class A: ...
class B(A): ...
```

MRO for `B` is: `B -> A -> object`.
So Python checks `B` first, then `A`, then `object`.

You can see it with `B.mro()`.

---

## Multiple inheritance & why MRO matters

With two parents, which parent comes first?

```python
class A: ...
class B(A): ...
class C(A): ...
class D(B, C): ...
```

Now D’s MRO is not just `D, B, C, A` by accident — Python computes a consistent linear order so methods are found predictably and so `super()` works in a cooperative way.

Python uses the **C3 linearization** algorithm (a principled way) to compute MRO. You don’t need the details to use it, but know it guarantees:

* A class appears before its parents.
* The order respects the order you list base classes (`class D(B, C)` means prefer `B` before `C`).
* The MRO is conflict-free when possible; if it isn’t, Python will raise an error.

Check it with `.mro()`:

```python
print(D.mro())  # shows the exact lookup order
```

---

## The diamond problem (classic example)

```python
class A:
    def who(self): print("A")

class B(A):
    def who(self): print("B")

class C(A):
    def who(self): print("C")

class D(B, C):
    pass

d = D()
d.who()            # Which who() runs?
print(D.mro())     # See order
```

Output:

* `d.who()` prints `B` if MRO is `D -> B -> C -> A -> object`.
* The MRO ensures `B` is checked before `C`, avoiding ambiguity.

---

## `super()` and MRO — why they’re friends

`super()` doesn’t just call the immediate parent. It calls the *next class in the MRO*. That’s what allows cooperative multiple inheritance.

Example pattern:

```python
class A:
    def do(self): print("A")

class B(A):
    def do(self):
        print("B")
        super().do()

class C(A):
    def do(self):
        print("C")
        super().do()

class D(B, C):
    def do(self):
        print("D")
        super().do()

D().do()
print(D.mro())
```

This will call `D.do() -> B.do() -> C.do() -> A.do()`, following the MRO. Each class does its part and calls `super()` so the chain continues.

That cooperative pattern is why `super()` is preferred over explicitly calling `A.method(self, ...)` — it keeps behavior consistent across complex hierarchies.

---

## How to inspect MRO

Use:

```python
print(ClassName.mro())
# or
import inspect
print(inspect.getmro(ClassName))
```

This prints the exact search order Python will use.

---

## Practical rules / things to remember

* `class X(B, C)` means prefer `B` before `C` when computing MRO, but the algorithm can interleave bases to preserve consistency and avoid contradictions.
* Use `super()` for cooperative methods so multiple inheritance composes nicely.
* If you get a weird error about “Cannot create a consistent method resolution order (MRO)”, your inheritance graph is ambiguous (Python can’t linearize it) — simplify the design.
* For most code, keep inheritance simple (single inheritance or shallow multiple inheritance). Use composition if things get messy.

---

## Summary

*   Inheritance is a mechanism in OOP to create a new class from an existing class.
*   The new class is the derived class or subclass or child class.
*   The existing class from which the derived class is created is called the base class or superclass or parent class.
*   MRO (Method Resolution Order) is the order in which the classes are searched for a member during lookup.

---