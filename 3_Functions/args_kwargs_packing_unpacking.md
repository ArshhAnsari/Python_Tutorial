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
| ------------------- | ----------- | ------------------------------------------ |
| Function Definition | `*args`     | Pack positional arguments into a tuple    |
| Function Definition | `**kwargs`  | Pack keyword arguments into a dictionary  |
| Function Call       | `*iterable` | Unpack iterable into positional arguments |
| Function Call       | `**dict`    | Unpack dictionary into keyword arguments  |
| Assignment          | `*name`     | Collect leftover values into a list       |

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

# A Third Location for `*`: Assignment

Two locations covered so far — definition (packing) and call (unpacking).

There's a third: **plain assignment.**

```python
a, b, c = [1, 2, 3]
```

This only works if the count matches exactly. Three names, three values.

`*` removes that restriction — one name absorbs whatever's left over,
packed into a list, while every other name still takes exactly one value.

---

## Example

```python
first, *others, last = input("Enter values separated by space: ").split()
```

Input:

```text
10 20 30 40 50
```

Python packs:

```python
first  = "10"
others = ["20", "30", "40"]
last   = "50"
```

`input().split()` just produces the list — that part has nothing to do
with `*`. The star is doing the same job it always does: **absorb
whatever isn't claimed by a plain name, pack it into a container.**

---

## Position Determines What Gets Collected

```python
leader, *followers = ["John", "Alex", "Sara", "Mike"]
# leader = "John"
# followers = ["Alex", "Sara", "Mike"]     <- everything AFTER leader
```

```python
*items, total = ["Apple", "Banana", "Orange", 15]
# items = ["Apple", "Banana", "Orange"]    <- everything BEFORE total
# total = 15
```

```python
first, *mid, last = [10, 20, 30, 40, 50]
# first = 10, mid = [20, 30, 40], last = 50   <- everything IN BETWEEN
```

Only one `*` allowed per assignment. Its position — start, end, or
middle — decides which stretch it collects.

---

## Converting to Integers Along the Way

`split()` always returns strings. Convert before unpacking, in one pass:

```python
first, *mid, last = [int(x) for x in input("Enter numbers: ").split()]
```

Input:

```text
10 20 30 40 50
```

Result:

```python
first = 10
mid   = [20, 30, 40]
last  = 50
```

### What `[int(x) for x in ...]` is — in short

That's a **list comprehension**: a compact way to build a list by running an
expression (`int(x)`) once for every item an iterable produces (`for x in
input(...).split()`), and collecting every result into a new list, in order.
`[int(x) for x in ["10", "20", "30"]]` is a shorter way of writing:

```python
result = []
for x in ["10", "20", "30"]:
    result.append(int(x))
```

The square brackets are what make it a list — the whole thing runs eagerly and
the entire list exists in memory as soon as the line finishes executing, which
is exactly why it can be unpacked immediately on the same line above.

That's the short version — just enough to read the line above. The full
picture — what changes if you swap `[ ]` for `( )` instead (a generator
expression), why that changes *when* the values get computed, and what that
costs or saves in memory — is covered in depth here:

```text
5_OOPs\8_Generator_Decorator\1_Generators_decorators.py — section 1.6
```

---

## Why `*numbers = ...` Alone Is a `SyntaxError`

```python
*numbers = [10, 20, 30]   # SyntaxError
```

`*name` means: **collect what's left over, after every other name has
claimed its one value.** If `*numbers` is the only name, there's nothing
else present to define "leftover relative to what." Python has no way to
tell "assign the whole thing here" apart from a typo, so it refuses.

---

## Three Fixes

**1. Drop the star — you don't need unpacking for a plain list:**

```python
numbers = [int(x) for x in input("Enter numbers: ").split()]
# numbers = [10, 20, 30]
```

**2. Keep the star, add a trailing comma:**

```python
*numbers, = [int(x) for x in input("Enter numbers: ").split()]
# numbers = [10, 20, 30]
```

The comma turns this into valid unpacking syntax with a single target.
(This isn't `*`-specific — `x, = [5]` alone is already valid, unpacking
a one-element list into `x`. Adding `*` before it changes "must match
exactly" into "collect everything.")

**3. Use the star for what it's actually for — separating out one value:**

```python
first_num, *numbers = [int(x) for x in input("Enter numbers: ").split()]
# first_num = 10, numbers = [20, 30]
```

Option 1 is almost always the right call in practice. Reach for `*` only
when you specifically need to peel off one or two fixed positions —
a header, a total, a leader — from the rest.

---

## Same Symbol, Three Jobs

```text
Definition:   def func(*args):        ->  PACK incoming arguments
Call:         func(*some_list)        ->  UNPACK a list into arguments
Assignment:   first, *rest = values   ->  COLLECT leftovers into a list
```

All three are the same underlying idea — `*` means "the many, treated
as one container" — just applied on whichever side of the operation it
sits.

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

| Concept               | Meaning                                                |
| ---------------------- | ------------------------------------------------------- |
| `*args`               | Pack extra positional arguments into a tuple           |
| `**kwargs`            | Pack extra keyword arguments into a dictionary         |
| `*iterable`           | Unpack iterable into positional arguments              |
| `**mapping`           | Unpack dictionary into keyword arguments               |
| `*name` (assignment)  | Collect leftover values into a list during unpacking   |
| Definition Side       | Packing                                                |
| Call Side             | Unpacking                                              |
| `args`                | Convention, not keyword                                |
| `kwargs`              | Convention, not keyword                                |
| Forwarding            | `func(*args, **kwargs)`                                |
| Decorators            | Built heavily on forwarding                            |

---

# One Sentence Summary

```text
Function definitions PACK arguments into containers.

Function calls UNPACK containers into arguments.

Assignment lets * collect leftover values into a list — same packing idea, third location.

* works with positional values and tuples.

** works with keyword values and dictionaries.
```
---