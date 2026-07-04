# iter(), next(), and Generator Expressions

This note explains what Python is doing internally when you use `iter()`,
`next()`, and generator expressions.

Once this clicks, generator expressions stop feeling magical.

---

## Part 1 - How iter() and next() Work

Start with this:

```python
colors = iter(["red", "blue"])
```

The list:

```python
["red", "blue"]
```

is an **iterable**.

An iterable is an object that knows how to create an iterator.

When Python runs:

```python
colors = iter(["red", "blue"])
```

it creates an iterator object.

Conceptually:

```text
List
index 0 -> "red"
index 1 -> "blue"

Iterator
current position -> 0
```

The iterator does **not** copy all the values.

It stores mainly:

- which iterable it belongs to
- the current position

Think of the iterator like a bookmark in a book.

The iterator is not the book. It only remembers where you are.

---

## First next() Call

```python
next(colors)
```

Python does something like:

```text
current position = 0

read element at index 0
return "red"
move current position to 1
```

Visual:

```text
before:

0 -> red
1 -> blue
^
current position

next(colors)

returns "red"

after:

0 -> red
1 -> blue
     ^
     current position
```

The iterator advances as part of producing the value.

---

## Second next() Call

```python
next(colors)
```

Now:

```text
current position = 1
```

Python does:

```text
read element at index 1
return "blue"
move current position to 2
```

Now the iterator is past the end.

---

## Third next() Call

Normally:

```python
next(colors)
```

raises:

```python
StopIteration
```

But this:

```python
next(colors, "green")
```

means:

> If the iterator is exhausted, do not raise `StopIteration`.
> Return `"green"` instead.

So:

```text
current position = 2
no more items
return default value: "green"
```

---

## Important Mental Model

`next()` asks the iterator for one value.

The iterator itself:

```text
reads current item
moves its internal position
returns the item
```

The movement is built into the iterator.

---

## Part 2 - Generator Expression with next()

Now look at this:

```python
first_admin = next(
    u["name"]
    for u in users
    if u["role"] == "admin"
)
```

This part:

```python
u["name"]
for u in users
if u["role"] == "admin"
```

is a **generator expression**.

Written separately:

```python
admins = (
    u["name"]
    for u in users
    if u["role"] == "admin"
)
```

At this moment, Python has not looped through `users` yet.

It only creates a generator object.

Conceptually, the generator stores:

- the iterable: `users`
- the current loop position
- the condition: `u["role"] == "admin"`
- the expression to produce: `u["name"]`

Think of it like a tiny paused function.

```text
generator:

for u in users
    if u["role"] == "admin"
        yield u["name"]
```

Nothing runs until `next()` asks for a value.

---

## Example Data

```python
users = [
    {"name": "Alice", "role": "user"},
    {"name": "Bob", "role": "admin"},
    {"name": "Charlie", "role": "admin"},
]
```

Now:

```python
admins = (
    u["name"]
    for u in users
    if u["role"] == "admin"
)
```

Again, no user has been checked yet.

---

## First next(admins) Call

```python
next(admins)
```

Python starts running the generator.

### Step 1

```python
u = users[0]
```

So:

```python
u = {"name": "Alice", "role": "user"}
```

Now Python checks:

```python
u["role"] == "admin"
```

That means:

```python
"user" == "admin"
```

Result:

```python
False
```

So the generator skips `u["name"]` for Alice and continues.

### Step 2

```python
u = users[1]
```

So:

```python
u = {"name": "Bob", "role": "admin"}
```

Now Python checks:

```python
u["role"] == "admin"
```

That means:

```python
"admin" == "admin"
```

Result:

```python
True
```

Now Python evaluates:

```python
u["name"]
```

which becomes:

```python
"Bob"
```

The generator yields `"Bob"` to `next()`.

So:

```python
first_admin = next(admins)
```

becomes:

```python
first_admin = "Bob"
```

The generator pauses immediately after yielding `"Bob"`.

It does not continue to Charlie unless another `next()` call happens.

---

## Visual Timeline

```text
users[0] -> Alice
role == admin?
False
skip

users[1] -> Bob
role == admin?
True
produce u["name"]
yield "Bob"
pause
```

That is why `next()` returns the first matching admin only.

---

## If You Call next() Again

```python
next(admins)
```

The generator resumes from where it paused.

It does not restart from Alice.

It continues to the next user:

```text
users[2] -> Charlie
role == admin?
True
yield "Charlie"
pause
```

So the second call returns:

```python
"Charlie"
```

If you call `next(admins)` again after that, there are no more users, so Python
raises:

```python
StopIteration
```

---

## Where Does u["name"] Get Stored?

Question:

> When the `if` finds an admin, where does `u["name"]` get stored?

It does not get stored permanently.

The generator simply evaluates:

```python
u["name"]
```

At that moment:

```python
u = {"name": "Bob", "role": "admin"}
```

So:

```python
u["name"]
```

becomes:

```python
"Bob"
```

Then it immediately yields that value.

Flow:

```text
u
-> u["name"]
-> "Bob"
-> yield
-> next()
-> first_admin
```

The value is handed directly to `next()`.

---

## Why next() Is Useful Here

This code:

```python
first_admin = next(
    u["name"]
    for u in users
    if u["role"] == "admin"
)
```

does the same job as:

```python
for u in users:
    if u["role"] == "admin":
        first_admin = u["name"]
        break
```

Both mean:

- loop through users
- find the first admin
- store that admin's name
- stop immediately

The generator version stops because `next()` only asks for one value.

After `"Bob"` is yielded, `next()` returns.

Because there is no second `next()` call, the generator does not continue to
Charlie.

---

## Default Value with next()

If there might be no admin, this version is safer:

```python
first_admin = next(
    (u["name"] for u in users if u["role"] == "admin"),
    None
)
```

The second argument to `next()` is the default value.

So if no admin exists:

```python
first_admin = None
```

instead of raising `StopIteration`.

---

## Generator Expression vs List Comprehension

List comprehension:

```python
admins = [
    u["name"]
    for u in users
    if u["role"] == "admin"
]
```

This builds the whole list immediately:

```python
["Bob", "Charlie"]
```

Generator expression:

```python
admins = (
    u["name"]
    for u in users
    if u["role"] == "admin"
)
```

This builds nothing immediately.

It produces values one at a time when asked:

```python
next(admins)  # "Bob"
next(admins)  # "Charlie"
```

That is why generator expressions are called **lazy**.

They only do work on demand.

---

## Final Mental Model

Think of a generator as a lazy factory.

```text
Need next value?

start or resume loop
check condition
produce one value
pause immediately
wait for another next()
```

Unlike a list comprehension, a generator expression does not build the whole
list first.

It only keeps enough state to produce the next value.

That state includes:

- where the loop currently is
- local variables like `u`
- the condition
- the expression to yield

This is why generators are memory efficient and why they work naturally with
`next()`.

Interview-level mental model:
A generator is not a collection of values like a list. It is a paused function.

- next() → resumes the function.
- yield value → returns one value and freezes the entire function's execution state (local variables, loop position, instruction pointer).
- Another next() → resumes from the exact point where it was frozen, not from the beginning.