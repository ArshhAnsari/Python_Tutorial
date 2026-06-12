# OOP Relationships, Inheritance, Aggregation, MRO & super()

---

# Why Relationships Exist

Objects rarely work alone.

In real-world software, classes interact with each other through relationships.

The two most important relationships are:

```text
1. HAS-A Relationship
   → Aggregation / Composition

2. IS-A Relationship
   → Inheritance
```

Understanding these two relationships is the foundation of Object-Oriented Programming.

---

# 1. HAS-A Relationship (Aggregation)

## Definition

A class contains or uses an object of another class.

```text
Customer HAS-A Address

Car HAS-A Engine

Restaurant HAS-A Menu
```

The object being used is called a component or dependency.

---

## Example

```python
class Address:
    def __init__(self, city):
        self.city = city


class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address
```

Usage:

```python
addr = Address("Mumbai")
cust = Customer("Arsh", addr)
```

Memory:

```text
Address Object
--------------
city = Mumbai


Customer Object
---------------
name = Arsh
address ───────► Address Object
```

Customer stores a reference to an Address object.

Therefore:

```text
Customer HAS-A Address
```

---

## Important Rule

Aggregation does NOT give inheritance.

Customer cannot suddenly become an Address.

```python
cust.city
```

❌ Invalid

Because Customer is not an Address.

Instead:

```python
cust.address.city
```

✅ Valid

---

## Accessing Private Members

```python
class Address:
    def __init__(self):
        self.__pin = 12345
```

Private members cannot be accessed directly:

```python
cust.address.__pin
```

❌

Use a getter:

```python
def get_pin(self):
    return self.__pin
```

---

## Aggregation Mental Model

Think:

```text
Car
 └── Engine

Customer
 └── Address

University
 └── Department
```

One object contains or uses another.

---

# 2. IS-A Relationship (Inheritance)

## Definition

Inheritance means a child class derives from a parent class.

```text
Dog IS-A Animal

Car IS-A Vehicle

Student IS-A Person
```

The child automatically gets access to the parent's public interface.

---

### Example

```python
class Animal:
    def speak(self):
        print("...")

class Dog(Animal):
    pass
```

Usage:

```python
d = Dog()
d.speak()
```

Output:

```text
...
```

Dog inherited the method from Animal.

---

# What Actually Gets Inherited

Python does not copy methods.

Instead, Python stores a link to the parent.

```python
class Animal:
    pass

class Dog(Animal):
    pass
```

Check parent:

```python
print(Dog.__bases__)
```

Output:

```python
(<class 'Animal'>,)
```

Python remembers who the parent is.

---

### Lookup Chain

```python
Dog
  ↓
Animal
  ↓
object
```

If Dog cannot find something:

```python
dog.some_method()
```

Python searches:

```text
Dog
 ↓
Animal
 ↓
object
```

This search order becomes very important later.

---

# Types of Inheritance

### Single

```python
Animal
   ↑
  Dog
```

```python
class Dog(Animal):
    pass
```

---

### Multilevel

```python
Animal
   ↑
  Dog
   ↑
GuideDog
```

```python
class GuideDog(Dog):
    pass
```

---

### Hierarchical

```python
       Animal
       /    \
     Dog    Cat
```

---

### Multiple

```python
Flyable      Swimmable
      \      /
         Duck
```

```python
class Duck(Flyable, Swimmable):
    pass
```

This introduces a new problem.

---

## The Problem Multiple Inheritance Creates

Suppose:

```python
class A:
    def greet(self):
        print("A")

class B(A):
    def greet(self):
        print("B")

class C(A):
    def greet(self):
        print("C")

class D(B, C):
    pass
```

Question:

```python
D().greet()
```

Should Python call:

```text
B.greet()
```

or

```text
C.greet()
```

Both exist.

This ambiguity is called:

```text
The Diamond Problem
```

---

# MRO (Method Resolution Order)

## Definition

MRO is the order Python follows when searching for attributes and methods.

```text
Method Resolution Order
```

Python computes it once when the class is created.

---

### Example

```python
class D(B, C):
    pass

print(D.__mro__)
```

Output:

```text
(D, B, C, A, object)
```

Python searches in exactly this order.

```text
D
↓
B
↓
C
↓
A
↓
object
```

---

## Therefore

```python
D().greet()
```

Search:

```text
D → not found

B → found
```

Stop.

Output:

```text
B
```

---

## MRO Rules

Python uses C3 Linearization.

You don't need to memorize the algorithm.

Remember these rules:

### Rule 1

A class appears before its parents.

### Rule 2

Parent order matters.

```python
class D(B, C)
```

means:

```text
B preferred before C
```

### Rule 3

object is always last.

---

# Understanding super()

Most beginners think:

```python
super()
```

means:

```text
Go to my parent.
```

Wrong.

---

## Real Meaning

```text
super()
=
Go to the NEXT class in the current MRO.
```

This is the most important thing to remember.

---

### Single Inheritance Example

```python
class Animal:
    def __init__(self):
        print("Animal")

class Dog(Animal):
    def __init__(self):
        print("Dog")
        super().__init__()
```

Output:

```text
Dog
Animal
```

MRO:

```text
Dog → Animal → object
```

Without super():

```python
class Dog(Animal):
    def __init__(self):
        Animal.__init__(self)
```

Works. But hardcodes Animal.

---

# Understanding Hardcoded Parent Calls vs MRO

Consider this code:

```python
class A:
    def __init__(self):
        print("A init")

class B(A):
    def __init__(self):
        print("B init")
        A.__init__(self)

class C(A):
    def __init__(self):
        print("C init")
        A.__init__(self)

class D(B, C):
    def __init__(self):
        print("D init")
        B.__init__(self)

D()
```

Many people expect:

```text
D init
B init
C init
A init
```

because D inherits from both B and C.

But the actual output is:

```text
D init
B init
A init
```

C never runs.

---

## Step-by-Step Trace

### Step 1

Object creation begins:

```python
D()
```

Python calls:

```python
D.__init__()
```

Output:

```text
D init
```

### Step 2

Inside D:

```python
B.__init__(self)
```

This is a hardcoded call.

Meaning:

```text
"Ignore everything else.
Go directly to B."
```

Python executes:

```python
B.__init__()
```

Output:

```text
B init
```

### Step 3

Inside B:

```python
A.__init__(self)
```

Another hardcoded call.

Meaning:

```text
"Ignore everything else.
Go directly to A."
```

Python executes:

```python
A.__init__()
```

Output:

```text
A init
```

### Step 4

A finishes.

```python
class A:
    def __init__(self):
        print("A init")
```

A does not call anything further.

Execution ends.

## Complete Trace

```text
D()
│
├── D.__init__()
│      prints "D init"
│
└── B.__init__()
       prints "B init"

       └── A.__init__()
              prints "A init"

END
```

Output:

```text
D init
B init
A init
```
---

## The Big Misconception

Many beginners think:

```text
D inherits from B and C

Therefore Python should automatically run both.
```

This is wrong.

Inheritance does NOT automatically execute parent constructors.

Inheritance only creates relationships and lookup paths.

---

## What D(B, C) Actually Means

```python
class D(B, C):
    pass
```

means:

```text
D can look in B
D can look in C
D can look in A
```

for methods and attributes.

It does NOT mean:

```text
Automatically execute B.__init__()
Automatically execute C.__init__()
Automatically execute A.__init__()
```

Python never does that.

Someone must explicitly call those methods.

## Reachable ≠ Called

This is the key idea.

Because of inheritance:

```python
print(D.__mro__)
```

Output:

```text
(D, B, C, A, object)
```

C is reachable.

Python knows about C.

Python can search C.

But nobody actually calls:

```python
C.__init__()
```

Therefore C never executes.

## The One Sentence To Remember

```text
D(B, C) only makes C reachable through method lookup.

It does NOT automatically execute C.__init__().

A class constructor runs only if some code explicitly calls it, either directly or through super().
```

## This is how super() solves multiple inheritance problem [Cooperative Inheritance] Correct version:

```python
class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()
```

MRO:

```text
D → B → C → A → object
```

Execution:

```text
D
↓
B
↓
C
↓
A
```

Output:

```text
D
B
C
A
```

Every class runs exactly once.

---

# Relay Race Mental Model

Imagine:

```text
MRO = running order

super() = pass baton to next runner
```

Example:

```text
D → B → C → A
```

D receives baton.

```text
D
 ↓ super()
B
 ↓ super()
C
 ↓ super()
A
```

Everyone gets a turn.

---

# Aggregation vs Inheritance

The most important interview distinction.

## Aggregation

```python
class Car:
    def __init__(self):
        self.engine = Engine()
```

```text
Car HAS-A Engine
```

---

## Inheritance

```python
class Dog(Animal):
    pass
```

```text
Dog IS-A Animal
```

---

# Final Revision Sheet

| Concept                 | Meaning                        |
| ----------------------- | ------------------------------ |
| Aggregation             | HAS-A relationship             |
| Inheritance             | IS-A relationship              |
| `__bases__`             | Direct parent classes          |
| `__mro__`               | Complete lookup order          |
| MRO                     | Method Resolution Order        |
| Diamond Problem         | Multiple inheritance ambiguity |
| `super()`               | Next class in current MRO      |
| Hardcoded Parent Call   | Ignores MRO                    |
| Cooperative Inheritance | Every class calls `super()`    |
| Composition/Aggregation | Object contains another object |
| Inheritance             | Child specializes parent       |

### One sentence to remember everything

```text
Aggregation answers:
"What objects does this class HAVE?"

Inheritance answers:
"What type of thing IS this class?"

MRO answers:
"Where should Python look next?"

super() answers:
"Who is next in the MRO?"
```
