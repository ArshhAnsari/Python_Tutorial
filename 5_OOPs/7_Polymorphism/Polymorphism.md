
# What is polymorphism (simple)

**Polymorphism** means “many forms.” In object-oriented programming it lets different object types be used *through the same interface*. You write code that calls the same method name (like `speak`) and each object responds in its own way. The caller doesn’t care what the actual type is — it only cares the object can do the operation.

---

# Walkthrough of your code (step-by-step)

### 1) Base class — the common interface

```python
class Animal:
    def speak(self):
        raise NotImplementedError("Subclass must implement this method")
```

* `Animal` defines the *interface*: all animals should have a `speak()` method.
* The base method raises `NotImplementedError` so if someone forgets to implement `speak` in a subclass and you call it, you get a clear runtime error.
* (Alternative: make `Animal` an `ABC` with `@abstractmethod` — we’ll mention that later.)

### 2) Subclasses — concrete implementations

```python
class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Duck(Animal):
    def speak(self):
        return "Quack!"
```

* Each subclass **overrides** `speak()` and provides its own behavior.
* This is *method overriding*: the subclass method replaces the base behavior for instances of that subclass.

### 3) Using polymorphism

```python
animals = [Dog(), Cat(), Duck()]

for animal in animals:
    print(f"The animal says: {animal.speak()}")
```

* The list `animals` contains different types, but you treat them uniformly.
* On each loop iteration, `animal.speak()` invokes the `speak` implementation bound to that object’s class — *dynamic dispatch* happens at runtime.
* Python finds the method by attribute lookup on the instance’s class and calls it, automatically passing the instance as `self`.

### 4) Generic function that accepts any “speakable”

```python
def make_animal_speak(animal_object):
    print(animal_object.speak())

make_animal_speak(Dog())  # Woof!
make_animal_speak(Cat())  # Meow!
```

* This function demonstrates polymorphism: it accepts any object that has a `speak()` method.
* It doesn’t check the type — it relies on **the object providing the required behavior**.

---

# What actually happens when you call `animal.speak()` (runtime mechanics)

1. Python evaluates `animal.speak` → performs attribute lookup:

   * checks `animal.__dict__`, then `animal.__class__.__dict__`, then base classes.
2. It finds the `speak` function on the class (e.g., `Dog.speak`) and **binds** it to the instance (creates a bound method).
3. Calling that bound method executes the function with `self` set to the instance.

This is why `Dog().speak()` runs `Dog.speak` with `self` pointing to that `Dog` object.

---

# Key concepts related to this example

* **Subtype polymorphism**: `Dog`, `Cat`, `Duck` are all subtypes of `Animal`. You can treat them as `Animal`.
* **Duck typing**: Python is flexible — it is enough that an object *has* a `speak()` method. It doesn’t need to inherit from `Animal`.
* **Dynamic dispatch**: Method selection happens at runtime, so the correct `speak` executes for each object.
* **Liskov Substitution Principle (LSP)**: Any object of a subtype should be usable where the base type is expected. Your `Dog`, `Cat`, `Duck` follow that: they all implement `speak()`.

---

# Variants & practical tips

### A. If a subclass forgets `speak()`

If you define:

```python
class SilentAnimal(Animal):
    pass

a = SilentAnimal()
a.speak()   # raises NotImplementedError
```

You get a clear error telling you the subclass didn’t implement the required method.

### B. Enforce implementation at class-creation time (better)

Use an Abstract Base Class to force subclasses to implement `speak()`:

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self): ...
```

Now trying to instantiate a subclass that doesn’t implement `speak()` raises a `TypeError` immediately.

### C. Duck-typed object (not inheriting from `Animal`) still works

```python
class Robot:
    def speak(self):
        return "Beep boop!"

make_animal_speak(Robot())  # prints "Beep boop!"
```

Because `make_animal_speak` just calls `.speak()`, any object that has it will work — that's duck typing.

---
# Why polymorphism is useful (practical benefits)

* **Simple, clean code**: one loop over animals, no `if isinstance(...)` chains.
* **Extensible**: add `Pig(Animal)` and it just works with existing functions.
* **Separation of concerns**: callers don’t need to know internal details — they just use the interface.

---

# Short checklist for robust polymorphic design

* Define a clear interface (docstring, ABC, or informal convention).
* Ensure subclasses implement required methods (use `@abstractmethod` if enforcement is needed).
* Prefer composition or delegation when appropriate (inheritance isn’t always required).
* Use duck typing when you want flexible, lightweight code. Use Protocols or ABCs when you want stronger guarantees.

---