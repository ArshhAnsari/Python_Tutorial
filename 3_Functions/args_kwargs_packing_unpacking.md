# Python `*args` and `**kwargs`

## Packing, Unpacking, and Function Call Mechanics

---

# Why `*args` and `**kwargs` Exist

Normally, Python functions expect a fixed number of arguments.

```python
def add(a, b):
    return a + b

add(1, 2)      # ✓
add(1, 2, 3)   # TypeError
```

Sometimes we don't know beforehand how many arguments a caller may provide.

Examples:

* Logging systems
* Decorators
* Framework internals (Django, FastAPI)
* Wrapper functions
* Utility functions

To support variable numbers of arguments, Python provides:

```python
*args
**kwargs
```

---

# The Golden Rule

The meaning of `*` and `**` depends on where they appear.

| Location            | Operator    | Meaning                                   |
| ------------------- | ----------- | ----------------------------------------- |
| Function Definition | `*args`     | Pack positional arguments into a tuple    |
| Function Definition | `**kwargs`  | Pack keyword arguments into a dictionary  |
| Function Call       | `*iterable` | Unpack iterable into positional arguments |
| Function Call       | `**dict`    | Unpack dictionary into keyword arguments  |

Think:

```text
Definition Side
↓
PACKING

Call Side
↓
UNPACKING
```

Same symbols.

Opposite operation.

---

# 3. Understanding Packing

Packing means:

```text
Many arguments
        ↓
One container
```

---

# *args (Packing Positional Arguments)

## Definition

When Python sees:

```python
def func(*args):
```

it collects all extra positional arguments into a tuple.

---

## Example

```python
def show(*args):
    print(args)

show(1, 2, 3)
```

Python internally does:

```python
args = (1, 2, 3)
```

Output:

```python
(1, 2, 3)
```

---

## More Examples

```python
show("a", "b")
```

becomes:

```python
args = ("a", "b")
```

---

```python
show()
```

becomes:

```python
args = ()
```

Output:

```python
()
```

No error.

Just an empty tuple.

---

## Important

`args` is not a keyword.

This is valid:

```python
def show(*values):
    print(values)
```

```python
def show(*numbers):
    print(numbers)
```

The special part is the `*`.

The name is your choice.

---

# 5. Example: Multiply Function

```python
def multiply(*args):
    result = 1

    for num in args:
        result *= num

    return result
```

Call:

```python
multiply(2, 3, 4)
```

Python packs:

```python
args = (2, 3, 4)
```

Execution:

```python
result = 1

1 * 2 = 2
2 * 3 = 6
6 * 4 = 24
```

Returns:

```python
24
```

---

# **kwargs (Packing Keyword Arguments)

## Definition

When Python sees:

```python
def func(**kwargs):
```

it collects all extra keyword arguments into a dictionary.

---

## Example

```python
def show(**kwargs):
    print(kwargs)
```

Call:

```python
show(name="Arsh", role="Engineer")
```

Python packs:

```python
kwargs = {
    "name": "Arsh",
    "role": "Engineer"
}
```

Output:

```python
{'name': 'Arsh', 'role': 'Engineer'}
```

---

## Empty Case

```python
show()
```

becomes:

```python
kwargs = {}
```

Empty dictionary.

---

# Packing Visualized

```text
show(1, 2, 3)

1
2
3
 ↓
Packing
 ↓

args = (1, 2, 3)
```

---

```text
show(name="Arsh", role="Engineer")

name="Arsh"
role="Engineer"
      ↓
Packing
      ↓

kwargs = {
    "name": "Arsh",
    "role": "Engineer"
}
```

---
# Example: 

## * Unpacking

```python
def demo(*args):
    print(args)

nums = [4, 5, 6]
```

Call:
```python
demo(*nums)
```

Python first unpacks:

```python
demo(4, 5, 6)
```

Then function receives:

```python
args = (4, 5, 6)
```

Output:

```python
(4, 5, 6)
```

## ** Unpacking

```python
def greet(name, role):
    print(name, role)

config = {
    "name": "Arsh",
    "role": "Engineer"
}
```
Call:

```python
greet(**config)
```

Python converts:

```python
greet(
    name="Arsh",
    role="Engineer"
)
```

Output:

```python
Arsh Engineer
```
---

# Combining Everything

```python
def fn(a, b, *args, flag=False, **kwargs):
    print(a)
    print(b)
    print(args)
    print(flag)
    print(kwargs)
```

Call:

```python
fn(
    1,
    2,
    3,
    4,
    flag=True,
    x=10,
    y=20
)
```

Result:

```python
a = 1

b = 2

args = (3, 4)

flag = True

kwargs = {
    "x": 10,
    "y": 20
}
```

---

# Forwarding Arguments

One of the most common real-world uses.

```python
def log(message, level="INFO"):
    print(f"[{level}] {message}")
```

Wrapper:

```python
def wrapper(*args, **kwargs):
    print("Before")

    log(*args, **kwargs)

    print("After")
```

Call:

```python
wrapper(
    "Server Started",
    level="DEBUG"
)
```

Output:

```python
Before
[DEBUG] Server Started
After
```

## Why Forwarding Matters

This is the foundation of:

* Decorators
* Django middleware
* FastAPI dependency wrappers
* Logging wrappers
* Retry mechanisms
* Performance monitors

Pattern:

```python
def wrapper(*args, **kwargs):
    ...
    original(*args, **kwargs)
    ...
```

You will see this everywhere.

---

# Common Pitfalls

## Pitfall 1

Confusing packing with unpacking.

```python
def fn(*args):
```

Packing.

---

```python
fn(*nums)
```

Unpacking.

---

## Pitfall 2

Thinking these are the same:

```python
nums = [1, 2, 3]
```

```python
fn(nums)
```

and

```python
fn(*nums)
```

They are NOT.

---

### Call A

```python
fn(nums)
```

Function receives:

```python
args = ([1, 2, 3],)
```

Tuple length:

```python
1
```

Contains:

```python
One list
```

---

### Call B

```python
fn(*nums)
```

Python converts:

```python
fn(1, 2, 3)
```

Function receives:

```python
args = (1, 2, 3)
```

Tuple length:

```python
3
```

Contains:

```python
Three integers
```

This distinction is extremely important.

---

# Final Revision Sheet

| Concept         | Meaning                                        |
| --------------- | ---------------------------------------------- |
| `*args`         | Pack extra positional arguments into a tuple   |
| `**kwargs`      | Pack extra keyword arguments into a dictionary |
| `*iterable`     | Unpack iterable into positional arguments      |
| `**mapping`     | Unpack dictionary into keyword arguments       |
| Definition Side | Packing                                        |
| Call Side       | Unpacking                                      |
| `args`          | Convention, not keyword                        |
| `kwargs`        | Convention, not keyword                        |
| Forwarding      | `func(*args, **kwargs)`                        |
| Decorators      | Built heavily on forwarding                    |

---

# One Sentence Summary

```text
Function definitions PACK arguments into containers.

Function calls UNPACK containers into arguments.

* works with positional values and tuples.

** works with keyword values and dictionaries.
```
---