# Decorators & Generators — How They Actually Work

---

## §1 — HOW WRAPPER GETS CALLED (The Most Important Question)

### The Confusion
> "When I call add(), how does wrapper run? I never called wrapper. I never called logger a second time."

### The Answer: Name Rebinding (The Robbery)

The answer is: **`add` IS `wrapper`. They are the same object.**

When Python reads `@logger`, it does exactly this:

```python
# What @ does — one line:
add = logger(add)
```

After this line runs:
- The name `add` no longer points to the original function
- The name `add` now points to `wrapper`
- The original function is only reachable through wrapper's closure

```
BEFORE @logger:
'add' ──────────────────────────────► [original function: a+b]

AFTER @logger:
'add' ──────────────────────────────► [wrapper function]
                                           │
                                   closure:└── func ──► [original function: a+b]
```

So when you write `add(2, 3)`:

```
add(2, 3)
    ↓
Python: add points to wrapper, so this is wrapper(2, 3)
    ↓
wrapper runs — because you called add, which IS wrapper
```

Nobody wakes up wrapper. Nobody calls logger again.
`add` literally is `wrapper`. Calling `add` is calling `wrapper`.
They share the same memory address.

### Proof

```python
def logger(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def add(a, b): return a + b

print(id(add))      # address 1 — original add

add = logger(add)   # THE ROBBERY — add is rebound to wrapper

print(id(add))      # address 2 — different! add is now wrapper
```

### Phone Number Analogy

```
Original add    = restaurant at number 555-0001
logger          = call centre (runs once, sets things up, retires)
wrapper         = call centre agent who takes the number

After setup:
  Anyone dials 555-0001 → reaches the AGENT (wrapper), not the restaurant
  Agent logs the call (before behavior)
  Agent calls restaurant on private line (func in closure)
  Restaurant answers → food returned (return value)
  Agent passes food to customer (return result)
  Customer got 555-0001, but talked to the agent. Number was reassigned.
```

---

## §2 — WHAT IS A CLOSURE (Really)

### The Confusion
> "Does closure mean `result = func()` and `return result`? Is it a line of code?"

### The Answer: A Memory Mechanism, Not a Line

A closure is **a function that remembers variables from its enclosing scope, even after that scope has finished and its stack frame is gone.**

Normally when a function finishes, everything inside it is destroyed:

```python
def logger(func):
    # func lives here in logger's scope
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # func used here
        return result
    return wrapper
    # logger returns here — normally func would be destroyed
    # BUT wrapper is still using func
    # so Python keeps func alive, attached to wrapper
```

Python says:
> "I cannot destroy `func`. `wrapper` still needs it.
> I will keep `func` alive, attached to `wrapper`, even after `logger` is gone."

**That attachment = the closure.**

### Factory Worker Analogy

```
logger  = factory worker
wrapper = robot the worker builds

Before retiring, the factory worker installs a memory chip into the robot.
The chip contains: func = original add, level = "INFO"

Factory worker retires (logger returns, stack frame gone).
Robot (wrapper) carries the memory chip forever.
Every time the robot runs, it opens the chip and reads func and level.
```

### Inspecting a Closure

```python
def logger(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def add(a, b): return a + b
add = logger(add)

# The original add is literally sitting inside wrapper's closure:
print(add.__closure__)                    # (<cell object>,)
print(add.__closure__[0].cell_contents)   # <function add> — alive inside wrapper
```

### What Each Closure Contains After `@logger(level="INFO")`

```python
def logger(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

@logger(level="INFO")
def add(a, b): return a + b
```

```
3 function objects exist in memory:

1. logger         → plain function, no closure (takes level as normal parameter)

2. decorator      → closure contains: {level: "INFO"}
                    (inherited from logger's scope — LEGB E rule)

3. wrapper        → closure contains: {func: original_add, level: "INFO"}
                    (func from decorator's scope, level inherited further)

name 'add'        → points to wrapper
original add      → only reachable via wrapper.__closure__
```

---

## §3 — WHY WRAPPER TAKES *args/**kwargs NOT a, b

### The Confusion
> "Original add takes a and b. So why doesn't wrapper take a and b too?"

### The Answer: One Wrapper Must Work For Any Function

```python
@logger
def add(a, b):                       # 2 positional args
    return a + b

@logger
def greet(name, greeting="Hello"):   # 1 positional + 1 keyword
    return f"{greeting} {name}"

@logger
def do_nothing():                    # 0 args
    pass
```

Same `logger`. Same `wrapper`. Three completely different signatures.

If wrapper said `def wrapper(a, b)`:
- Works for `add` ✓
- Crashes for `greet` ✗
- Crashes for `do_nothing` ✗

`*args, **kwargs` means: **"Accept whatever you throw at me, pack it, forward it."**

### The Pack → Forward → Unpack Flow

```python
def wrapper(*args, **kwargs):         # PACK: any args into tuple/dict
    return func(*args, **kwargs)      # FORWARD + UNPACK back to original

add(4, 5)
    ↓
wrapper(4, 5)                         # add IS wrapper
    ↓
args = (4, 5), kwargs = {}            # *args packs them
    ↓
func(*(4,5), **{})                    # unpacked back to positional
    ↓
original add(a=4, b=5)                # original receives normally
    ↓
returns 9
```

This is the exact same `*` mechanism from the very first session on `*args/**kwargs`.
Pack → forward → unpack. Same tool, applied inside a decorator.

---

## §4 — WHAT DOES level="INFO" MEAN AND WHERE DOES IT LIVE

### The Confusion
> "What is level? Is it a special keyword? How does it get used inside wrapper?"

### The Answer: A Plain String, Stored in Closure

`level` is not special. Not magic. Not a Python keyword.
It is a plain variable — a string you pass as configuration.

### The Complete Journey of level

```python
def logger(level):              # level = "INFO" — just a parameter
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{level}] calling {func.__name__}")
            #          ↑
            #    level read from closure here — always "INFO" for this function
            return func(*args, **kwargs)
        return wrapper
    return decorator

@logger(level="INFO")
def add(a, b): return a + b
```

```
Step 1: logger(level="INFO") called
        level = "INFO" stored in logger's local scope
        decorator created — closes over level
        decorator's closure = {level: "INFO"}
        logger returns decorator, LOGGER IS DONE

Step 2: decorator(add) called
        func = original add stored
        wrapper created — closes over func AND level (inherited)
        wrapper's closure = {func: original_add, level: "INFO"}
        decorator returns wrapper, DECORATOR IS DONE

Every call to add(2, 3):
        wrapper opens closure chip
        level = "INFO"  → used in print(f"[INFO]...")
        func  = original_add → called to get real result
```

`"INFO"` and `"DEBUG"` are just labels you choose.
They get **baked into the closure at decoration time** and never change.

```python
@logger(level="INFO")
def add(a, b): return a + b      # add's wrapper: level = "INFO" forever

@logger(level="DEBUG")
def multiply(a, b): return a*b   # multiply's wrapper: level = "DEBUG" forever
```

---

## §5 — DOES LOGGER RUN EVERY TIME I CALL add()?

### The Answer: NO. Logger runs ONCE at definition time. Never again.

```
DEFINITION TIME (once, when file loads / line is read):
    logger(level="INFO") runs
        → creates decorator
        → returns decorator
    decorator(original_add) runs
        → creates wrapper
        → returns wrapper
    name 'add' = wrapper
    BOTH logger and decorator are done and gone

CALL TIME (every single time you call add()):
    wrapper runs  ← ONLY this
    logger:        NEVER involved again
    decorator:     NEVER involved again
```

This is why decorators are efficient — the setup cost (logger, decorator) pays once.
Every call after that only hits the thin wrapper layer.

---

## §6 — WHAT DOES return result DO — WHERE DOES IT GO

### The Result Travels Like a Bucket Being Passed Upward

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)   # original runs, returns value HERE
        print("after")
        return result                    # wrapper passes value UPWARD
    return wrapper

@logger
def add(a, b): return a + b

x = add(2, 3)    # x = 5
```

```
original add(2, 3)
    ↓ computes 2+3=5
    ↓ returns 5
result = func(2, 3) = 5    ← wrapper catches it in 'result'
    ↓
wrapper does after-behavior
    ↓
return result (5)          ← wrapper passes 5 upward
    ↓
x = add(2, 3) = 5          ← caller receives 5
```

### What Happens If You Forget to Return

```python
def bad_logger(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)    # calls it — but DISCARDS return value
        # no return → Python returns None implicitly
    return wrapper

@bad_logger
def add(a, b): return a + b

print(add(2, 3))    # None — wrapper swallowed the result
```

**Rule:** Always `return result` in every wrapper. Always.
In stacked decorators, every layer must return — or value is swallowed at that layer.

---

## §7 — STACKING: APPLICATION ORDER vs EXECUTION ORDER

### The Core Rule

```python
@decorator_one      # applied SECOND — outermost layer
@decorator_two      # applied FIRST  — innermost layer
def my_func(): ...

# Equivalent without @:
my_func = decorator_one(decorator_two(my_func))
#                       ↑              ↑
#                 applied 2nd    applied 1st
```

```
Application order: BOTTOM to TOP   (stack being built from ground up)
Execution order:   TOP to BOTTOM   (onion being peeled from outside in)
```

### Two Robberies — Bottom to Top

```python
@bold
@italic
def greet(name): print(f"Hello {name}")
```

```
Robbery 1 (bottom first — italic steals greet):
    greet = italic(original_greet)
    greet ──► [italic_wrapper]
                   └─ closure: func ──► [original greet]

Robbery 2 (top second — bold steals greet from italic):
    greet = bold(italic_wrapper)
    greet ──► [bold_wrapper]
                   └─ closure: func ──► [italic_wrapper]
                                            └─ closure: func ──► [original greet]
```

### Execution — Onion Peeling (Top to Bottom)

```
greet("Arsh")
    ↓ greet IS bold_wrapper
bold_wrapper("Arsh"):
    print("bold: before")
    ↓ func("Arsh") → calls italic_wrapper
    italic_wrapper("Arsh"):
        print("italic: before")
        ↓ func("Arsh") → calls original greet
        original greet: print("Hello Arsh")
        print("italic: after")
        return result
    print("bold: after")
    return result

Output:
bold: before
italic: before
Hello Arsh
italic: after
bold: after
```

Execution **enters** through outermost (bold) → works inward → hits original →
**unwinds** back outward (italic after → bold after).

---

## §8 — DECORATOR WITH ARGUMENTS: THE 3-LAYER STRUCTURE

### Normal vs With Arguments

```python
# NORMAL DECORATOR — 2 layers:
def logger(func):               # layer 1: receives function
    def wrapper(*args, **kwargs):   # layer 2: runs on each call
        ...
    return wrapper

# WITH ARGUMENTS — 3 layers (one extra outer layer):
def logger(level):              # layer 1: receives YOUR config
    def decorator(func):        # layer 2: receives function
        def wrapper(*args, **kwargs):   # layer 3: runs on each call
            ...
        return wrapper
    return decorator
```

### What Python Does With `@logger(level="INFO")`

```python
# Python translates this:
@logger(level="INFO")
def add(a, b): return a + b

# Into exactly this:
add = logger(level="INFO")(add)
#            ↑               ↑
#     step 1: called        step 2: result called
#     with config           with function

# Step-by-step without @:
_decorator = logger(level="INFO")   # step 1: get a plain decorator
add = _decorator(add)               # step 2: decorate the function
```

### Three Functions, Three Jobs, Three Closures

```
logger(level)        → job: receive config, return decorator
                        closure: none (level is a plain parameter)
                        dies after returning decorator

decorator(func)      → job: receive function, return wrapper
                        closure: {level: "INFO"}
                        dies after returning wrapper

wrapper(*args,**kwargs) → job: run on every call, before/after original
                           closure: {func: original_add, level: "INFO"}
                           lives forever — this IS what 'add' points to
```

---

## §9 — GENERATOR: HOW yield PAUSES AND RESUMES

### Normal Function vs Generator Function

```
Normal function:
┌──────────────────┐
│ run everything   │──► returns value once, function is GONE
└──────────────────┘

Generator function:
┌──────────────────┐
│ run until yield  │──► hands value, FREEZES (frame preserved)
│       ↑          │
│  resume here     │◄── next() called
│ run until yield  │──► hands value, FREEZES again
│       ↑          │
│  resume here     │◄── next() called
│  function ends   │──► StopIteration
└──────────────────┘
```

### Three Things to Remember

```
1. gen = counter()   → does NOT run the function
                        gives you a generator object (the paused machine)

2. next(gen)         → runs until next yield
                        hands you one value
                        pauses right after yield

3. function ends     → StopIteration raised automatically
```

### Vending Machine Mental Model

```
Generator = vending machine

You press a button (next()) → machine makes ONE snack → hands it → WAITS
Press again → ONE more snack → hands it → WAITS
Machine empty (function ends) → StopIteration
```

```python
def vending_machine():
    yield "chips"    # press 1 → chips  → FREEZE
    yield "soda"     # press 2 → soda   → FREEZE
    yield "candy"    # press 3 → candy  → FREEZE

vm = vending_machine()   # machine exists, nothing dispensed yet
next(vm)   # chips
next(vm)   # soda
next(vm)   # candy
next(vm)   # StopIteration — machine empty
```

### Why Infinite Generators Don't Crash

```python
def infinite_counter():
    x = 0
    while True:        # infinite loop — BUT yield suspends it
        x += 1
        yield x        # PAUSES here, hands x to caller, waits

g = infinite_counter()
next(g)   # 1 — loop ran once, paused
next(g)   # 2 — loop ran again, paused
next(g)   # 3 — loop ran again, paused
# Only advances when YOU call next() — you control the pace
```

### Generator IS Its Own Iterator — Exhaustion Problem

```python
gen = simple_gen()
print(list(gen))    # [1, 2, 3]
print(list(gen))    # []  — exhausted, i is still at end position

# Fix: call generator FUNCTION each time for a fresh object
print(list(simple_gen()))   # [1, 2, 3] — fresh
print(list(simple_gen()))   # [1, 2, 3] — fresh again
```

---

## §10 — GENERATOR vs LIST: MEMORY DIFFERENCE

### The Precise Difference

```python
a = [x * 2 for x in range(1_000_000)]   # list comprehension
b = (x * 2 for x in range(1_000_000))   # generator expression
```

```
'a' (list):
    ALL 1 million values computed RIGHT NOW
    ALL stored in heap memory as a list object
    ~8MB in memory immediately
    stays in memory until deleted

'b' (generator):
    NOTHING computed yet
    b is a tiny object (~200 bytes) regardless of n
    stores only: function code + current position + local variable state
    each next(b) computes ONE value, hands it out, suspends
    previous values NOT stored — gone after yielded
```

Neither lives on the call stack — both on the heap.
The difference: `a` holds ALL values simultaneously,
`b` holds only enough state to produce the NEXT one.

---

## §11 — WHY list(items) DOESN'T MAKE [[1,2,3]]

### The Confusion
> "If I pass a list to list(), doesn't it store a list inside a list → [[1,2,3]]?"

### The Answer: list() Unpacks, Not Wraps

`list()` takes any iterable and **consumes it element by element** into a new list.
It does NOT wrap. It unpacks.

```python
list([1, 2, 3])    # iterates → pulls out 1, 2, 3 → [1, 2, 3]
list([[1, 2, 3]])  # iterates → pulls out [1,2,3] as ONE element → [[1,2,3]]
```

The elements of the iterable become the elements of the new list — as-is.

### Connection to *args — Same Mechanism

```python
# * unpacks at language level:
fn(*[1, 2, 3])     # → fn(1, 2, 3)

# list() unpacks at function level:
list([1, 2, 3])    # → [1, 2, 3]

# Both consume iterable element by element via __iter__ + __next__
```

```python
# These produce the same result via the same mechanism:
[*[1, 2, 3]]        # spread syntax → [1, 2, 3]
list([1, 2, 3])     # list() call   → [1, 2, 3]
```

### Why Bag Does This

```python
class Bag:
    def __init__(self, items):
        self._items = list(items)   # defensive copy, NOT wrapping

# REASON 1: Protection from external mutation
original = [1, 2, 3]
b = Bag(original)
original.append(99)
print(b._items)    # [1, 2, 3] — Bag's copy is unaffected

# REASON 2: Accept any iterable
Bag([1, 2, 3])          # list ✓
Bag((1, 2, 3))          # tuple ✓
Bag({1, 2, 3})          # set ✓
Bag(range(1, 4))        # range ✓
Bag(x for x in [1,2])  # generator ✓
# self._items = items would make _items a tuple/generator
# list() normalises everything to a list
```

---

## §12 — FULL MENTAL MODEL SUMMARIES

### Decorator Mental Model (All 5 Rules)

```
Rule 1: Decorator = name robbery
        After @logger, the name 'add' is stolen from original
        and given to wrapper. Calling add() calls wrapper() —
        they are the same object, same memory address.

Rule 2: Original function never disappears
        It lives in wrapper's closure as 'func'.
        Reachable via: add.__closure__[0].cell_contents

Rule 3: Return value = bucket passed upward
        original returns value
        → wrapper catches in 'result'
        → wrapper returns it up
        → caller receives it
        If any layer forgets return result → None swallowed

Rule 4: Decorator with arguments = one extra outer layer
        logger(level) → returns decorator
        decorator(func) → returns wrapper
        wrapper closes over BOTH func AND level

Rule 5: Stacking = chain of robberies, bottom to top
        Application: bottom decorator applied first (innermost)
        Execution:   top decorator runs first (outermost)
        Each layer holds previous version in its closure
```

### Generator Mental Model

```
Generator function   → any function containing yield
Generator object     → what calling generator function produces
                        has __iter__ and __next__ automatically
                        is its OWN iterator

yield                → suspend + hand value out + preserve frame
next()               → resume from suspension point
StopIteration        → function body finished, no more values

Generator expression → lazy list comprehension with ()
                        nothing computed until next() called

yield from x         → delegate entirely to x until x is exhausted

Key rule:            → call generator FUNCTION each time for fresh object
                        same object = shared position = exhaustion bug
```

### Closure Mental Model

```
Closure = inner function keeping outer function's variables alive
          even after outer function has returned and its frame is gone

Why it exists:
    Python sees inner function uses outer variable
    → cannot destroy that variable when outer returns
    → attaches it to inner function's __closure__

Where to find it:
    fn.__closure__                    → tuple of cell objects
    fn.__closure__[0].cell_contents   → the actual value

In decorators:
    wrapper closes over: func (original function)
                         level / any config from outer layers
    These live in wrapper's closure forever
    Accessible every time wrapper runs
```