"""
================================================================================
GENERATORS AND DECORATORS — Deep Dive
Topics: yield mechanics, generator objects, expressions, yield from,
        decorator pattern, functools.wraps, *args/**kwargs forwarding
================================================================================
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1: GENERATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 1.1 THE PROBLEM — WHY GENERATORS EXIST
# ─────────────────────────────────────────────

# Imagine you need to process 1 million numbers.
# The naive approach builds the entire list in memory first.

def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i * i)
    return result

squares = get_squares_list(1_000_000)
# At this point, 1 million integers are sitting in memory RIGHT NOW.
# Even if you only need the first 3 values.
# This is wasteful.

# The generator version — produces ONE value at a time, on demand.

def get_squares_gen(n):
    for i in range(n):
        yield i * i    # pause here, hand this value out, resume on next call

squares_gen = get_squares_gen(1_000_000)
# At this point: NOTHING has been computed.
# squares_gen is a tiny object — stores only:
#   → the function code
#   → current position (not started yet)
#   → local variable state (i, the range iterator)
# Memory: ~200 bytes regardless of n.


# ─────────────────────────────────────────────
# 1.2 THE VENDING MACHINE MENTAL MODEL
# ─────────────────────────────────────────────

# Think of a generator as a vending machine.
# It does not make all the snacks at once and dump them on the floor.
# You press a button (call next()), it makes ONE snack, hands it to you,
# and WAITS until you press again.

def vending_machine():
    yield "chips"    # press 1 → get chips  → machine FREEZES
    yield "soda"     # press 2 → get soda   → machine FREEZES
    yield "candy"    # press 3 → get candy  → machine FREEZES
                     # press 4 → StopIteration (machine empty)

vm = vending_machine()

print("=== Vending Machine ===")
print(next(vm))   # chips
print(next(vm))   # soda
print(next(vm))   # candy
# print(next(vm)) # StopIteration — uncomment to see it crash


# ─────────────────────────────────────────────
# 1.3 HOW yield ACTUALLY WORKS — STEP BY STEP
# ─────────────────────────────────────────────

# Three things to remember:
#   1. Calling the function → does NOT run it, gives you the generator object
#   2. next()              → runs until next yield, gives you one value
#   3. Function ends       → StopIteration automatically

def counter_demo():
    print("  [start of function]")
    yield 1
    print("  [after yield 1]")
    yield 2
    print("  [after yield 2]")
    yield 3
    print("  [function body ends]")

print("\n=== Yield Step-by-Step Trace ===")

gen = counter_demo()
print("Generator object created — function body has NOT run yet")

print("\ncalling next(gen) #1:")
val = next(gen)          # runs until yield 1, pauses
print(f"  got: {val}")

print("\ncalling next(gen) #2:")
val = next(gen)          # resumes from after yield 1, runs until yield 2
print(f"  got: {val}")

print("\ncalling next(gen) #3:")
val = next(gen)          # resumes from after yield 2, runs until yield 3
print(f"  got: {val}")

print("\ncalling next(gen) #4:")
try:
    val = next(gen)      # resumes, function body ends → StopIteration
except StopIteration:
    print("  StopIteration raised — generator exhausted")

# Visual flow of execution:
#
#  gen = counter_demo()
#      ↓
#  [function body frozen at top — not started]
#
#  next(gen)
#      ↓ runs → print("[start]") → hits yield 1
#      ↓ PAUSES, returns 1 to caller
#      ↓ pointer frozen AFTER yield 1
#
#  next(gen)
#      ↓ resumes from pointer → print("[after yield 1]") → hits yield 2
#      ↓ PAUSES, returns 2 to caller
#
#  next(gen)
#      ↓ resumes → print("[after yield 2]") → hits yield 3
#      ↓ PAUSES, returns 3
#
#  next(gen)
#      ↓ resumes → print("[function body ends]") → no more yield
#      ↓ StopIteration


# ─────────────────────────────────────────────
# 1.4 GENERATOR IS AN ITERATOR
# ─────────────────────────────────────────────

# A generator object automatically has __iter__ and __next__.
# You get a full iterator without writing a class.

def simple_gen():
    yield 1
    yield 2
    yield 3

gen = simple_gen()

print("\n=== Generator is an Iterator ===")
print(hasattr(gen, '__iter__'))   # True
print(hasattr(gen, '__next__'))   # True
print(iter(gen) is gen)           # True — generator is its OWN iterator

# This means: like the broken Counter class from container protocols,
# a generator object exhausts after one full pass.

gen = simple_gen()
print(list(gen))    # [1, 2, 3]
print(list(gen))    # []  — already exhausted, same Counter bug

# Fix: call the generator FUNCTION each time to get a FRESH object.
print(list(simple_gen()))   # [1, 2, 3]
print(list(simple_gen()))   # [1, 2, 3]  — fresh each time


# ─────────────────────────────────────────────
# 1.5 GENERATOR FUNCTION vs GENERATOR OBJECT
# ─────────────────────────────────────────────

# simple_gen      → generator FUNCTION (defined with yield)
# simple_gen()    → generator OBJECT   (what you iterate over)
# Every call to simple_gen() produces a FRESH, independent object.

def counter(n):
    i = 0
    while i < n:
        i += 1
        yield i

gen1 = counter(3)
gen2 = counter(3)

print("\n=== Independent Generator Objects ===")
print(next(gen1))   # 1 — gen1 advances
print(next(gen1))   # 2 — gen1 advances again
print(next(gen2))   # 1 — gen2 is independent, starts fresh


# ─────────────────────────────────────────────
# 1.6 INFINITE GENERATORS — SAFE WITH yield
# ─────────────────────────────────────────────

# Q1 FROM SESSION:
# Does this crash? What does it print?

def infinite_counter():
    x = 0
    while True:       # infinite loop — BUT yield pauses it each iteration
        x += 1
        yield x

g = infinite_counter()

print("\n=== Infinite Generator (Q1) ===")
print(next(g))   # 1
print(next(g))   # 2
print(next(g))   # 3

# Does NOT crash. while True with yield is not dangerous because:
# The function SUSPENDS at yield and waits.
# The loop only advances when YOU call next().
# You control the pace entirely.
# Common use: infinite ID sequences, streaming data, event loops.


# ─────────────────────────────────────────────
# 1.7 MEMORY MODEL — LIST vs GENERATOR (Q2)
# ─────────────────────────────────────────────

# Q2 FROM SESSION:
# What is the difference in memory behavior?

# a = [x * 2 for x in range(1_000_000)]
# b = (x * 2 for x in range(1_000_000))

# a → LIST COMPREHENSION
#   ALL 1 million values computed RIGHT NOW
#   ALL stored in heap memory as a list object
#   ~8MB in memory immediately
#   a points to that full list until deleted

# b → GENERATOR EXPRESSION
#   NOTHING computed yet
#   b is a tiny generator object (~200 bytes)
#   stores only: function code + current position + local state
#   each next(b) computes ONE value, yields it, suspends

# Neither lives on the call stack — both on the heap.
# Difference: a holds ALL values simultaneously,
#             b holds only enough state to produce the NEXT one.

# Practical:
import sys

a = [x * 2 for x in range(10_000)]
b = (x * 2 for x in range(10_000))

print("\n=== Memory Comparison (Q2) ===")
print(f"List size:      {sys.getsizeof(a):,} bytes")
print(f"Generator size: {sys.getsizeof(b):,} bytes")


# ─────────────────────────────────────────────
# 1.8 GENERATOR EXPRESSIONS
# ─────────────────────────────────────────────

# Same as list comprehension, but lazy. Uses () instead of [].

squares_list = [x * x for x in range(5)]    # builds list NOW
squares_gen  = (x * x for x in range(5))    # computes on demand

print("\n=== Generator Expression ===")
print(next(squares_gen))   # 0 — only this computed so far
print(next(squares_gen))   # 1
print(list(squares_gen))   # [4, 9, 16] — rest (0,1 already consumed)

# Pipeline pattern — no intermediate list ever built:
total = sum(x * x for x in range(1_000_000))
print(f"Sum of squares: {total}")
# sum() pulls values from the generator one at a time
# never builds a million-item list


# ─────────────────────────────────────────────
# 1.9 REWRITING get_evens AS A GENERATOR (Q3)
# ─────────────────────────────────────────────

# Q3 FROM SESSION: Rewrite get_evens using yield.

# BEFORE — list version:
def get_evens_list(n):
    return [x for x in range(n) if x % 2 == 0]

# AFTER — generator version:
def get_evens(n):
    for x in range(n):
        if x % 2 == 0:
            yield x
    # no list built, no return needed
    # each even number produced one at a time

# Both work identically from caller's perspective:
print("\n=== get_evens Generator (Q3) ===")
for num in get_evens(10):
    print(num, end=" ")   # 0 2 4 6 8
print()
print(list(get_evens(10)))   # [0, 2, 4, 6, 8]

# Trace of get_evens(6):
#   next() → x=0, 0%2==0 → yield 0  → pause
#   next() → x=1, 1%2!=0 → skip
#            x=2, 2%2==0 → yield 2  → pause
#   next() → x=3, skip
#            x=4, 4%2==0 → yield 4  → pause
#   next() → x=5, skip → loop ends → StopIteration


# ─────────────────────────────────────────────
# 1.10 yield from — DELEGATING TO INNER ITERABLES
# ─────────────────────────────────────────────

def first():
    yield 1
    yield 2

def second():
    yield 3
    yield 4

# Without yield from:
def combined_manual():
    for x in first():
        yield x
    for x in second():
        yield x

# With yield from — identical result, cleaner:
def combined():
    yield from first()    # delegates entirely to first() until exhausted
    yield from second()   # then delegates to second()

print("\n=== yield from ===")
print(list(combined()))   # [1, 2, 3, 4]

# yield from delegates to another iterable completely.
# The outer generator pauses until the inner one is exhausted.
# Works with any iterable — list, tuple, another generator, range.


# ─────────────────────────────────────────────
# 1.11 REWRITING COUNTER CLASS AS A GENERATOR
# ─────────────────────────────────────────────

# Remember the two-class CounterIterator solution from container protocols?
# Generators replace the entire iterator class.

# BEFORE — explicit iterator class (verbose):
class CounterOld:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return CounterIterator(self.n)

class CounterIterator:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self): return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        return self.i

# AFTER — generator inside __iter__ replaces the entire iterator class:
class Counter:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        i = 0
        while i < self.n:
            i += 1
            yield i           # yield inside __iter__ makes it a generator function
                              # Python auto-creates a fresh iterator object each call

print("\n=== Counter with Generator __iter__ ===")
c = Counter(3)
print(list(c))   # [1, 2, 3]
print(list(c))   # [1, 2, 3] — fresh each time, no exhaustion problem


# ─────────────────────────────────────────────
# 1.12 GENERATOR SUMMARY
# ─────────────────────────────────────────────

# Generator function   → any function with yield
# Generator object     → what calling a generator function produces
#                        (is its own iterator — has __iter__ and __next__)
# yield                → pause + hand value out + preserve entire frame
# next()               → resume from pause point
# StopIteration        → function body ran to end
# Generator expression → lazy list comprehension with ()
# yield from           → delegate to inner iterable completely


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2: DECORATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 2.1 TWO THINGS YOU ALREADY KNOW THAT MAKE THIS EASY
# ─────────────────────────────────────────────

# Decorators are NOT a new concept.
# They are built from two things you already understand:
#
#   1. Functions are objects — pass them, return them, store them
#   2. Closures — inner function remembers outer function's variables
#
# Nothing new mechanically. Decorators are just a PATTERN using those tools.


# ─────────────────────────────────────────────
# 2.2 THE PROBLEM — WHY DECORATORS EXIST
# ─────────────────────────────────────────────

# You have several functions. You want to log every call
# WITHOUT modifying each function's body.

# Naive approach — copy-paste extra behavior everywhere:
def add_bad(a, b):
    print("add called")       # copied to every function
    return a + b

def multiply_bad(a, b):
    print("multiply called")  # same line, repeated everywhere
    return a * b

# Problems:
#   → duplication
#   → modifying function body
#   → if logging logic changes, update EVERY function

# Decorators solve this: wrap a function with extra behavior
# without touching its body.


# ─────────────────────────────────────────────
# 2.3 BUILDING A DECORATOR FROM SCRATCH — 4 STEPS
# ─────────────────────────────────────────────

print("\n=== Building Decorator Step by Step ===")

# STEP 1: Functions are objects — pass them around
def greet():
    print("Hello")

def run(func):      # accepts a function as argument
    func()          # calls it

run(greet)          # Hello — function passed like any variable


# STEP 2: A function that returns a function
def outer():
    def inner():
        print("I am inner")
    return inner    # returns the function object, not the result

fn = outer()        # fn IS inner now
fn()                # "I am inner"


# STEP 3: Wrapping — the decorator pattern
def logger_simple(func):       # takes a function
    def wrapper():
        print(f"  → calling {func.__name__}")
        result = func()        # calls the original
        print(f"  → done")
        return result
    return wrapper             # returns the enhanced version

def greet():
    print("Hello")

greet = logger_simple(greet)   # replace greet with wrapped version
print("\nSimple wrapper:")
greet()
# → calling greet
# Hello
# → done

# What happened:
#   logger_simple(greet) → creates wrapper, wrapper holds reference to
#                          original greet via closure
#   returns wrapper
#   greet is now wrapper
#   calling greet() → calls wrapper() → wrapper calls original greet inside


# STEP 4: @ syntax — syntactic sugar for the same thing

# BEFORE — manual:
# def greet(): ...
# greet = logger_simple(greet)

# AFTER — decorator syntax:
# @logger_simple
# def greet(): ...
#
# These are 100% identical. @ is just shorthand.

# Q3 FROM SESSION:
# What does @logger do at definition time?
# Answer: Python immediately calls logger(greet) and rebinds
# the name 'greet' to whatever logger returns (the wrapper).
# This happens ONCE, at definition time, not at call time.


# ─────────────────────────────────────────────
# 2.4 HANDLING ARGUMENTS — *args AND **kwargs
# ─────────────────────────────────────────────

# The simple wrapper only works for functions with no arguments.
# wrapper() can't handle add(a, b).
# Fix: use *args/**kwargs to accept and forward anything.

def logger(func):
    def wrapper(*args, **kwargs):          # accepts any arguments
        print(f"  → calling {func.__name__} with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)     # forwards everything to original
        print(f"  → returned: {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

@logger
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print("\n=== Logger with *args/**kwargs ===")
add(3, 4)
greet("Arsh", greeting="Hey")

# Trace of add(3, 4):
#   add(3, 4)
#       ↓
#   wrapper(3, 4)              ← add IS wrapper now
#       ↓
#   args=(3,4), kwargs={}
#       ↓
#   func(3, 4)                 ← func is original add, held in closure
#       ↓
#   returns 7
#       ↓
#   wrapper prints and returns 7


# ─────────────────────────────────────────────
# 2.5 THE IDENTITY LOSS PROBLEM
# ─────────────────────────────────────────────

# After decorating, the function loses its identity:

@logger
def multiply(a, b):
    """Multiplies two numbers."""
    return a * b

print("\n=== Identity Loss Problem ===")
print(multiply.__name__)   # 'wrapper' ← WRONG, should be 'multiply'
print(multiply.__doc__)    # None      ← docstring lost

# Why: multiply IS wrapper now.
# wrapper has its own __name__ ('wrapper') and __doc__ (None).
# The original function's metadata is hidden inside the closure.


# ─────────────────────────────────────────────
# 2.6 FIX: functools.wraps
# ─────────────────────────────────────────────

from functools import wraps

def logger_fixed(func):
    @wraps(func)                           # copies __name__, __doc__,
    def wrapper(*args, **kwargs):          # __module__, __qualname__ from func
        print(f"  → calling {func.__name__} with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"  → returned: {result}")
        return result
    return wrapper

@logger_fixed
def multiply(a, b):
    """Multiplies two numbers."""
    return a * b

print("\n=== After functools.wraps ===")
print(multiply.__name__)   # 'multiply' ✓
print(multiply.__doc__)    # 'Multiplies two numbers.' ✓

# @wraps(func) is not optional in real code.
# Django, DRF, Flask all use @wraps internally.
# Always include it.


# ─────────────────────────────────────────────
# 2.7 Q1 FROM SESSION — FULL TRACE
# ─────────────────────────────────────────────

# Q: Trace add(2, 3) manually. What does it print?

from functools import wraps

def logger_q1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"result: {result}")
        return result
    return wrapper

@logger_q1
def add_q1(a, b):
    return a + b

print("\n=== Q1 Trace: add(2, 3) ===")
add_q1(2, 3)

# Trace:
#   add_q1(2, 3)
#       ↓ add_q1 IS wrapper (rebound at definition)
#   wrapper(2, 3)
#       ↓ args=(2,3), kwargs={}
#       ↓ print("calling add_q1")
#       ↓ result = add_q1_original(2, 3) → 5
#       ↓ print("result: 5")
#       ↓ return 5
#
# Output:
#   calling add_q1
#   result: 5


# ─────────────────────────────────────────────
# 2.8 Q2 FROM SESSION — timer DECORATOR
# ─────────────────────────────────────────────

import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()                      # record time before
        result = func(*args, **kwargs)           # call the original
        end = time.time()                        # record time after
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_sum(n):
    """Sum of range n — artificially slow."""
    total = 0
    for i in range(n):
        total += i
    return total

print("\n=== Q2: timer decorator ===")
slow_sum(1_000_000)

# Pattern is identical to logger:
#   before → call → after → return
# start/end captured in wrapper's local scope.
# func held in closure.


# ─────────────────────────────────────────────
# 2.9 THE COMPLETE DECORATOR TEMPLATE
# ─────────────────────────────────────────────

from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # ── before the call ──
        result = func(*args, **kwargs)
        # ── after the call ──
        return result
    return wrapper

@my_decorator
def any_function(x):
    return x * 2

# This template handles:
#   → any number of positional arguments (*args)
#   → any number of keyword arguments (**kwargs)
#   → return value forwarded correctly
#   → original name and docstring preserved (@wraps)


# ─────────────────────────────────────────────
# 2.10 CLOSURE INSIDE DECORATOR — HOW func IS REMEMBERED
# ─────────────────────────────────────────────

# This is the mechanism most people skip.
# How does wrapper() "know" what func is after logger() has returned?

def logger_explained(func):           # func = original add, lives here
    def wrapper(*args, **kwargs):     # wrapper is defined inside logger
        # func is FREE VARIABLE — not local to wrapper,
        # not global — lives in logger's scope (enclosing)
        # LEGB: L(wrapper) → E(logger) → G → B
        # Python finds func in E (enclosing scope of logger)
        result = func(*args, **kwargs)
        return result
    return wrapper                    # logger returns and its frame could
                                      # be destroyed — BUT Python keeps
                                      # func alive because wrapper holds
                                      # a reference to it via closure

# Even after logger_explained() returns and its stack frame is gone,
# wrapper still holds a live reference to the original func.
# This is a closure — inner function outlives the outer function's frame.


# ─────────────────────────────────────────────
# 2.11 Q3 FROM SESSION — WHAT DOES @logger DO AT DEFINITION TIME?
# ─────────────────────────────────────────────

# Q: What does @logger actually do to the function at definition time?
#    Write out the equivalent code without @ syntax.

# The @ symbol is purely syntactic sugar. Python translates it
# into an explicit assignment at class/module load time —
# BEFORE any calls are made.

# WITH @ syntax:
from functools import wraps

def logger_q3(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  → calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  → returned: {result}")
        return result
    return wrapper

@logger_q3
def add(a, b):
    return a + b

# The EXACT equivalent WITHOUT @ syntax:
def add_no_decorator(a, b):
    return a + b

add_no_decorator = logger_q3(add_no_decorator)   # ← this is ALL @ does

# Python sees @logger_q3 above a def and translates it to this
# assignment line IMMEDIATELY when the module/file loads.
# Not when add() is called. At DEFINITION time.

print("\n=== Q3: @ syntax vs explicit assignment ===")
add(3, 5)
add_no_decorator(3, 5)
# Both produce identical output — they ARE the same operation.

# Step-by-step what Python does at definition time with @:
#
#   Step 1: Python reads the def block → creates the original function object
#           (the real add, before decoration)
#
#   Step 2: Python calls logger_q3(add)
#           → logger_q3 runs
#           → wrapper is created inside logger_q3
#           → wrapper closes over func (= original add) via closure
#           → logger_q3 returns wrapper
#
#   Step 3: Python rebinds the name 'add' to the returned wrapper
#           add = wrapper
#
#   Step 4: The original add function object still exists in memory
#           but is ONLY reachable via func inside wrapper's closure
#           The name 'add' now points to wrapper
#
# Visual:
#
#   BEFORE @:
#   name 'add' ──────────────────► [original add function object]
#
#   AFTER @:
#   name 'add' ──► [wrapper function object]
#                       │
#                       └─ closure: func ──► [original add function object]
#
# This is why func.__name__ inside wrapper still prints 'add' —
# @wraps(func) copies the name from the original to wrapper.
# Without @wraps: wrapper.__name__ would be 'wrapper'.

# Proof — the name rebinding happens at definition, not at call:
print("\n=== Proof: rebinding happens at definition time ===")

def spy(func):
    print(f"  spy called with: {func.__name__}")  # prints at DEFINITION
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

print("About to define decorated function:")

@spy
def do_something():      # ← spy() is called RIGHT HERE, during definition
    pass

print("Function defined. Now calling it:")
do_something()           # spy's print already happened above — not here

# Output:
#   About to define decorated function:
#   spy called with: do_something     ← printed at definition
#   Function defined. Now calling it:
#   (nothing from spy — wrapper just calls original silently)


# ─────────────────────────────────────────────
# 2.12 DECORATOR SUMMARY
# ─────────────────────────────────────────────

# decorator        → function that takes a function, returns a function
# wrapper          → inner function that adds behavior around the original
# @syntax          → shorthand for func = decorator(func) at DEFINITION time
#                    (not at call time — happens when module loads)
# *args/**kwargs   → make wrapper forward any arguments to original
# @wraps(func)     → preserve __name__, __doc__ from original
# closure          → how wrapper remembers func after decorator returns
# name rebinding   → after @decorator, the original name points to wrapper
#                    original function only reachable via closure inside wrapper

# Standard template — memorise this:
#
# from functools import wraps
#
# def my_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         # before
#         result = func(*args, **kwargs)
#         # after
#         return result
#     return wrapper