# Python Properties Deep Dive

## Understanding @property, _variable Storage, Getter/Setter Interception, and the Recursion Trap

---

# Why Properties Exist

Imagine we have a simple class:

```python
class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
```

Usage:

```python
f = Fraction(1, 2)

print(f.numerator)
print(f.denominator)
```

Everything works.

The problem is that there is no validation.

```python
f.denominator = 0
```

This is mathematically invalid for a fraction, but Python allows it.

To control reads and writes, Python provides **properties**.

---

# What is a Property?

A property allows a method to behave like an attribute.

Without property:

```python
obj.x
```

means:

```python
read attribute x
```

With property:

```python
obj.x
```

means:

```python
call getter method
```

and

```python
obj.x = value
```

means:

```python
call setter method
```

The user still writes normal attribute syntax, but Python secretly executes functions.

---

# Basic Property Example

```python
class Fraction:

    def __init__(self, denominator):
        self.denominator = denominator

    @property
    def denominator(self):
        return self._denominator

    @denominator.setter
    def denominator(self, value):
        if value == 0:
            raise ValueError("Denominator cannot be zero")
        self._denominator = value
```

Usage:

```python
f = Fraction(2)

print(f.denominator)

f.denominator = 5

f.denominator = 0
```

Output:

```python
ValueError: Denominator cannot be zero
```

---

# The Most Important Idea

Properties are not stored on the instance.

They live on the class.

Example:

```python
class Example:

    @property
    def value(self):
        return self._value
```

The property object belongs to the class:

```python
Example.__dict__
```

contains:

```python
'value': <property object>
```

The actual data is stored on the instance.

```python
obj.__dict__
```

contains:

```python
{
    '_value': 10
}
```

---

# The Standard Property Pattern

Almost every Python class follows this structure:

```python
class Example:

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
```

Notice the naming:

```text
value      -> Public interface
_value     -> Internal storage
```

The property acts as a gatekeeper.

The actual data lives in _value.

---

# Why Use _value Instead of value?

Because using value inside the property causes infinite recursion.

Consider:

```python
class Box:

    @property
    def width(self):
        return self.width
```

Looks innocent.

But let's see what happens.

---

# The Infinite Recursion Trap

Execution:

```python
box.width
```

Python sees:

```python
width is a property
```

so it calls:

```python
Box.width.getter(box)
```

Inside the getter:

```python
return self.width
```

Again Python sees:

```python
width is a property
```

so it calls the getter again.

Which again executes:

```python
return self.width
```

This repeats forever.

Visual flow:

```text
box.width
    ↓
getter()
    ↓
return self.width
    ↓
getter()
    ↓
return self.width
    ↓
getter()
    ↓
...
```

Eventually:

```python
RecursionError:
maximum recursion depth exceeded
```

---

# Correct Version

Instead:

```python
class Box:

    @property
    def width(self):
        return self._width
```

Now Python reads:

```python
self._width
```

which is a normal instance attribute.

No property is involved.

No recursion occurs.

---

# Understanding the Underscore

Many beginners think Python automatically creates _value.

It does not.

The underscore is simply a naming convention.

Without properties:

```python
class Example:
    def __init__(self):
        self.value = 10
```

Instance storage:

```python
{
    'value': 10
}
```

---

With properties:

```python
class Example:

    def __init__(self):
        self.value = 10

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
```

Instance storage:

```python
{
    '_value': 10
}
```

Why?

Because the setter explicitly stores the value in _value.

Python does not create it automatically.

The programmer chooses that name.

---

# What Happens Inside **init**?

This is where many people get confused.

Suppose:

```python
class Fraction:

    def __init__(self, x):
        self.denominator = x

    @property
    def denominator(self):
        return self._denominator

    @denominator.setter
    def denominator(self, value):
        self._denominator = value
```

When **init** executes:

```python
self.denominator = x
```

Python does NOT create:

```python
self.__dict__['denominator']
```

Instead it notices:

```python
denominator
```

is a property with a setter.

Therefore Python calls:

```python
denominator.setter(self, x)
```

which executes:

```python
self._denominator = x
```

The actual storage becomes:

```python
{
    '_denominator': 2
}
```

---

# Property Interception

Think of properties as interceptors.

Writing:

```python
obj.value = 5
```

becomes:

```python
setter(obj, 5)
```

Reading:

```python
obj.value
```

becomes:

```python
getter(obj)
```

The attribute syntax is only an illusion.

Functions are running behind the scenes.

---

# Read Flow

```text
obj.denominator
        ↓
Python checks class
        ↓
Finds property
        ↓
Calls getter
        ↓
Returns self._denominator
```

---

# Write Flow

```text
obj.denominator = 5
        ↓
Python checks class
        ↓
Finds property setter
        ↓
Calls setter
        ↓
Validation runs
        ↓
Stores self._denominator = 5
```

---

# Why Not Directly Modify _denominator?

Suppose:

```python
f.denominator = 0
```

Setter executes:

```python
ValueError
```

Great.

Now suppose:

```python
f._denominator = 0
```

Python bypasses the property completely.

No validation runs.

The object is now invalid.

This is why Python developers treat _variable as internal implementation details.

---

# Property vs Storage

Think of a bank.

```text
Customer
   ↓
Bank Counter (Property)
   ↓
Vault (_variable)
```

Customers never interact directly with the vault.

They go through the counter.

The counter performs checks and validation.

Similarly:

```text
obj.value
```

is the public interface.

```text
obj._value
```

is internal storage.

---

# Complete Mental Model

Without Property

```python
obj.value
```

↓

```python
instance attribute lookup
```

↓

```python
return value
```

---

With Property

```python
obj.value
```

↓

```python
find property on class
```

↓

```python
call getter
```

↓

```python
return self._value
```

---

Writing

```python
obj.value = 10
```

↓

```python
find property setter
```

↓

```python
validation
```

↓

```python
self._value = 10
```

---

# Interview Summary

1. `@property` lets methods behave like attributes.

2. Properties live on the class, not the instance.

3. Actual data is usually stored in `_variable`.

4. Reading `obj.var` triggers the getter.

5. Writing `obj.var = x` triggers the setter.

6. Inside a getter/setter, never use `self.var`.

7. Use `self._var` for storage.

8. `self.var` inside a getter causes infinite recursion.

9. `_var` is not private, it is a convention indicating internal storage.

10. The property is the public interface, `_var` is the implementation detail.
