"""
================================================================================
GENERATORS AND DECORATORS — A First-Principles Walkthrough
================================================================================

Generators are about LAZY ITERATION — producing values on demand instead of
all at once. Decorators are about WRAPPING BEHAVIOR around a function without
touching its body. Neither requires new syntax categories or new object types.
They're patterns built on top of the iterator protocol and closures.

================================================================================
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1 — GENERATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 1.1 THE PROBLEM GENERATORS SOLVE
# ─────────────────────────────────────────────

# Say you need to process a million numbers. The obvious approach:

def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i * i)
    return result

squares = get_squares_list(1_000_000)
# The instant this call returns, ONE MILLION integers already exist in
# memory — even if you only ever look at the first three. The function did
# all the work up front, whether you needed it or not.

# Compare:

def get_squares_gen(n):
    for i in range(n):
        yield i * i

squares_gen = get_squares_gen(1_000_000)
# At this exact line, NOTHING has been computed. squares_gen is a small
# object holding only:
#   - a reference to the function's code
#   - its current execution position (not yet started)
#   - its local variables (i, the range iterator)
# Regardless of whether n is 10 or 10 billion, that object stays roughly
# the same tiny size. Values get computed one at a time, only when asked for.


# ─────────────────────────────────────────────
# 1.2 THE MENTAL MODEL: A VENDING MACHINE
# ─────────────────────────────────────────────

# A generator doesn't manufacture all its output and dump it on the floor.
# It makes ONE item per button press (next()), hands it over, and freezes
# until pressed again.

def vending_machine():
    yield "chips"
    yield "soda"
    yield "candy"

vm = vending_machine()

print("=== 1.2 Vending Machine ===")
print(next(vm))   # chips
print(next(vm))   # soda
print(next(vm))   # candy
# print(next(vm)) # StopIteration — machine is empty, uncomment to see it


# ─────────────────────────────────────────────
# 1.3 WHAT yield ACTUALLY DOES, TRACED STEP BY STEP
# ─────────────────────────────────────────────

# Three facts to hold onto:
#   1. Calling a generator function does NOT run it — it returns a
#      generator object.
#   2. next() runs the function body until it hits a yield, then pauses.
#   3. When the function body finishes with no more yields, Python raises
#      StopIteration.

def counter_demo():
    print("  [start of function]")
    yield 1
    print("  [after yield 1]")
    yield 2
    print("  [after yield 2]")
    yield 3
    print("  [function body ends]")

print("\n=== 1.3 Yield Step-by-Step Trace ===")

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
    val = next(gen)      # resumes, function body ends -> StopIteration
except StopIteration:
    print("  StopIteration raised — generator exhausted")

# Execution flow:
#
#  gen = counter_demo()
#      -> function body frozen at the very top, not started
#
#  next(gen)
#      -> runs -> print("[start]") -> hits yield 1
#      -> PAUSES, returns 1 to caller (frame frozen right after yield 1)
#
#  next(gen)
#      -> resumes -> print("[after yield 1]") -> hits yield 2
#      -> PAUSES, returns 2
#
#  next(gen)
#      -> resumes -> print("[after yield 2]") -> hits yield 3
#      -> PAUSES, returns 3
#
#  next(gen)
#      -> resumes -> print("[function body ends]") -> no more yield
#      -> StopIteration
#
# The key thing yield gives you that return doesn't: the ENTIRE function
# frame (local variables, instruction pointer, everything) is preserved
# across calls, instead of being torn down.


# ─────────────────────────────────────────────
# 1.4 A GENERATOR IS AN ITERATOR — FOR FREE
# ─────────────────────────────────────────────

# Any object implementing __iter__ and __next__ is an iterator. A generator
# object has both, automatically.

def simple_gen():
    yield 1
    yield 2
    yield 3

gen = simple_gen()

print("\n=== 1.4 Generator is an Iterator ===")
print(hasattr(gen, '__iter__'))   # True
print(hasattr(gen, '__next__'))   # True
print(iter(gen) is gen)           # True — a generator is its OWN iterator

# If you've hand-written the iterator protocol before (a class with a
# separate __iter__ returning a fresh iterator object, and a __next__ that
# raises StopIteration), a generator collapses all of that into one
# function. yield anywhere in a function body is what makes Python treat
# the whole function as a generator function.

# This also means generators inherit the "exhausted after one pass"
# behavior that any iterator has:

gen = simple_gen()
print(list(gen))    # [1, 2, 3]
print(list(gen))    # []  — already consumed, nothing left

# Fix: call the generator FUNCTION again to get a fresh object.
print(list(simple_gen()))   # [1, 2, 3]
print(list(simple_gen()))   # [1, 2, 3]  — independent, fresh state each time

# The function (simple_gen) is reusable. The object (simple_gen()) is
# single-use. This distinction — generator FUNCTION vs generator OBJECT —
# is worth keeping sharp:

def counter(n):
    i = 0
    while i < n:
        i += 1
        yield i

gen1 = counter(3)
gen2 = counter(3)

print("\n=== 1.4b Independent Generator Objects ===")
print(next(gen1))   # 1 — gen1 advances
print(next(gen1))   # 2 — gen1 advances again, independent of gen2
print(next(gen2))   # 1 — gen2 hasn't been touched yet, starts fresh


# ─────────────────────────────────────────────
# 1.5 DOES `while True` INSIDE A GENERATOR HANG THE PROGRAM?
# ─────────────────────────────────────────────

# No — and this is worth being precise about, because it looks alarming
# on first read.

def infinite_counter():
    x = 0
    while True:        # infinite loop — BUT yield pauses it each iteration
        x += 1
        yield x

g = infinite_counter()

print("\n=== 1.5 Infinite Generator ===")
print(next(g))   # 1
print(next(g))   # 2
print(next(g))   # 3

# `while True` is only dangerous in a NORMAL function, where nothing stops
# the loop from running to completion in one go. Inside a generator, yield
# suspends execution EVERY SINGLE ITERATION. The loop only advances when
# you call next() again — you are pulling values, not the function pushing
# them at you. This is the standard pattern for infinite ID sequences,
# streaming data sources, and event loops.


# ─────────────────────────────────────────────
# 1.6 MEMORY: LIST COMPREHENSION vs GENERATOR EXPRESSION
# ─────────────────────────────────────────────

import sys

a = [x * 2 for x in range(10_000)]   # list comprehension
b = (x * 2 for x in range(10_000))   # generator expression — () instead of []

print("\n=== 1.6 Memory Comparison ===")
print(f"List size:      {sys.getsizeof(a):,} bytes")
print(f"Generator size: {sys.getsizeof(b):,} bytes")

# `a` computes and stores ALL ten thousand values immediately, as a real
# list object on the heap. `b` computes NOTHING yet — it's a tiny
# generator object holding only its code, position, and local state. Each
# next(b) produces exactly one value and suspends again.
#
# Both objects live on the heap (neither is "on the stack" in any
# meaningful sense for this comparison) — the difference isn't WHERE they
# live, it's HOW MUCH THEY HOLD AT ONCE. `a` holds every value
# simultaneously. `b` holds only enough state to produce the next one.

# Generator expressions shine in pipelines where you never need the
# intermediate collection at all:

total = sum(x * x for x in range(1_000_000))
print(f"Sum of squares: {total}")
# sum() pulls one value at a time from the generator — a million-element
# list is never built.


# ─────────────────────────────────────────────
# 1.6b A GENERATOR EXPRESSION CONSUMED BY A BUILTIN
# ─────────────────────────────────────────────

# sum() isn't the only builtin that pulls from a generator expression this
# way — max(), min(), and any() all take one directly, no parentheses
# needed beyond the expression's own.

students = [
    {"name": "A", "marks": [80, 75, 90]},
    {"name": "B", "marks": [65, 70, 72]},
    {"name": "C", "marks": [95, 92, 88]},
]

highest = max(student["marks"][0] for student in students)
print("\n=== 1.6b max() over a generator expression ===")
print(highest)   # 95

# This is exactly equivalent to building the list first and calling max()
# on it:
first_marks = [student["marks"][0] for student in students]
highest_v2 = max(first_marks)
# ...except the generator version never materializes first_marks as a
# real list. max() pulls one value at a time from the generator
# expression, keeps whichever is largest so far, and discards the rest.

# WORTH GETTING PRECISELY RIGHT — easy to state backwards:
# max() happens to process every element, but that's a fact about max()'s
# ALGORITHM, not about generator expressions as a category. A generator
# expression never processes anything on its own — it only produces one
# value per pull, exactly as in §1.6. max() pulls until the generator is
# exhausted because it has no way to know the maximum without seeing
# every value. But hand that same generator expression to any() instead,
# and it can stop at the FIRST truthy value:

has_high_scorer = any(student["marks"][0] > 90 for student in students)
print(has_high_scorer)   # True
# stops after checking "A" (80, no) and "C" (95, yes) — never evaluates
# whether "B" (65) would also match, because any() already has its answer

# Same generator-expression syntax, two different consumption patterns.
# Whether "all items get processed" depends entirely on what's PULLING
# from the expression — not on the expression itself.


# ─────────────────────────────────────────────
# 1.7 WORKED EXAMPLE: TURNING A FILTER INTO A GENERATOR
# ─────────────────────────────────────────────

# BEFORE — list version, builds the full result up front:
def get_evens_list(n):
    return [x for x in range(n) if x % 2 == 0]

# AFTER — generator version, yields one even number at a time:
def get_evens(n):
    for x in range(n):
        if x % 2 == 0:
            yield x
    # no return, no list — each match is handed out as it's found

# From the caller's side these look identical:
print("\n=== 1.7 get_evens Generator ===")
for num in get_evens(10):
    print(num, end=" ")   # 0 2 4 6 8
print()
print(list(get_evens(10)))   # [0, 2, 4, 6, 8]

# Tracing get_evens(6) shows the actual control flow — including the fact
# that a single call to next() can silently skip several loop iterations
# before it finds something to yield:
#
#   next() -> x=0, 0%2==0 -> yield 0 -> pause
#   next() -> x=1, skip
#             x=2, 2%2==0 -> yield 2 -> pause
#   next() -> x=3, skip
#             x=4, 4%2==0 -> yield 4 -> pause
#   next() -> x=5, skip -> loop exits -> StopIteration
#
# next() doesn't mean "run one loop iteration." It means "run until the
# next yield" — however many iterations that takes, including zero if a
# value is immediately ready.


# ─────────────────────────────────────────────
# 1.8 yield from — DELEGATING TO ANOTHER ITERABLE
# ─────────────────────────────────────────────

def first():
    yield 1
    yield 2

def second():
    yield 3
    yield 4

# Without yield from, chaining two generators means an explicit loop:
def combined_manual():
    for x in first():
        yield x
    for x in second():
        yield x

# yield from does the same thing more directly — it hands control to the
# inner iterable and pauses the outer generator until the inner one is
# fully exhausted:
def combined():
    yield from first()
    yield from second()

print("\n=== 1.8 yield from ===")
print(list(combined()))   # [1, 2, 3, 4]

# Works with ANY iterable on the right-hand side — a list, a tuple, a
# range, or another generator. Its real value shows up once you're
# building generators that recursively delegate to sub-generators (e.g.
# flattening a nested structure), where the manual
# "for x in ...: yield x" loop gets repetitive fast.


# ─────────────────────────────────────────────
# 1.9 REPLACING A FULL ITERATOR CLASS WITH ONE GENERATOR
# ─────────────────────────────────────────────

# If you've written the two-class version of the iterator protocol — a
# container class plus a separate iterator class — this is the payoff
# for learning generators.

# BEFORE — explicit iterator protocol, two classes:
class CounterOld:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return CounterIterator(self.n)   # must return a FRESH iterator each time

class CounterIterator:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        return self.i

# AFTER — one class, __iter__ is itself a generator function:
class Counter:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        i = 0
        while i < self.n:
            i += 1
            yield i   # presence of `yield` makes this __iter__ a generator function

print("\n=== 1.9 Counter with Generator __iter__ ===")
c = Counter(3)
print(list(c))   # [1, 2, 3]
print(list(c))   # [1, 2, 3] — fresh iterator again, no exhaustion carried over

# WHY THIS WORKS: because __iter__ contains yield, calling c.__iter__()
# doesn't run the loop — it returns a FRESH GENERATOR OBJECT each time,
# with its own independent `i`. That's exactly the contract __iter__ is
# supposed to fulfill (return a new iterator on every call), and you get
# it without writing a second class.


# ─────────────────────────────────────────────
# 1.10 GENERATORS — SUMMARY
# ─────────────────────────────────────────────

# Generator function   -> any function containing yield
# Generator object     -> what calling a generator function returns
#                         (is its own iterator — has __iter__ and __next__)
# yield                -> pause + hand value out + preserve entire frame
# next()               -> resume from the last pause point
# StopIteration         -> raised automatically when function body ends
# Generator expression -> (expr for x in iterable) — a lazy comprehension
# yield from           -> delegate entirely to an inner iterable


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2 — DECORATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 2.1 WHY DECORATORS AREN'T A NEW CONCEPT
# ─────────────────────────────────────────────

# Decorators are built from two things you already have full command of:
#   1. Functions are objects — you can pass them as arguments, return
#      them, store them in variables, put them in lists.
#   2. Closures — an inner function can remember variables from its
#      enclosing function even after that enclosing function has returned.
#
# A decorator is just a PATTERN that combines these two. Nothing new is
# happening mechanically — only a new way of arranging familiar pieces.


# ─────────────────────────────────────────────
# 2.2 THE PROBLEM DECORATORS SOLVE
# ─────────────────────────────────────────────

# Say you want every function call logged, without editing each
# function's body:

def add_bad(a, b):
    print("add called")       # copied to every function
    return a + b

def multiply_bad(a, b):
    print("multiply called")  # same line, repeated everywhere
    return a * b

# This duplicates the logging line everywhere, and if the logging logic
# ever changes, every function needs a manual edit. Decorators let you
# wrap a function with extra behavior — logging, timing, auth checks,
# caching — without touching its body at all.


# ─────────────────────────────────────────────
# 2.3 BUILDING A DECORATOR FROM NOTHING, FOUR STEPS
# ─────────────────────────────────────────────

print("\n=== 2.3 Building a Decorator Step by Step ===")

# STEP 1 — functions are ordinary objects, so you can pass one into
# another function:
def greet():
    print("Hello")

def run(func):
    func()

run(greet)   # "Hello" — greet was passed around like any variable


# STEP 2 — a function can return another function:
def outer():
    def inner():
        print("I am inner")
    return inner   # returns the function object itself, not the result of calling it

fn = outer()
fn()   # "I am inner"


# STEP 3 — combine both into the wrapping pattern:
def logger_simple(func):
    def wrapper():
        print(f"  → calling {func.__name__}")
        result = func()
        print(f"  → done")
        return result
    return wrapper

def greet():
    print("Hello")

greet = logger_simple(greet)   # greet is now wrapper, not the original function
print("\nSimple wrapper:")
greet()
# → calling greet
# Hello
# → done

# What just happened:
#   - logger_simple(greet) runs, creates wrapper, and wrapper captures a
#     reference to the original greet through closure.
#   - logger_simple returns wrapper.
#   - The name `greet` is reassigned to point at wrapper.
#   - Calling greet() now calls wrapper(), which calls the ORIGINAL greet
#     internally.


# STEP 4 — @ syntax is shorthand for exactly this reassignment:
#
#   # manual:
#   def greet(): ...
#   greet = logger_simple(greet)
#
#   # identical, using @ syntax:
#   @logger_simple
#   def greet(): ...
#
# These two forms produce byte-for-byte identical behavior. @decorator
# above a def is Python doing `name = decorator(name)` IMMEDIATELY WHEN
# THE MODULE LOADS — not when the function is later called. §2.9 traces
# this in full.


# ─────────────────────────────────────────────
# 2.4 MAKING THE WRAPPER HANDLE ARGUMENTS
# ─────────────────────────────────────────────

# The wrapper above only works for zero-argument functions — wrapper()
# can't forward anything to something like add(a, b). The fix is
# *args/**kwargs, which accept any call signature and forward it
# unchanged.

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

print("\n=== 2.4 Logger with *args/**kwargs ===")
add(3, 4)
greet("Arsh", greeting="Hey")

# Tracing add(3, 4):
#
#   add(3, 4)
#       -> (add IS wrapper now)
#   wrapper(3, 4)
#       -> args=(3,4), kwargs={}
#       -> func(3, 4)   <- func is the original add, held in closure
#       -> returns 7
#   wrapper prints, then returns 7


# ─────────────────────────────────────────────
# 2.5 THE IDENTITY-LOSS PROBLEM
# ─────────────────────────────────────────────

# Decorate a function and it loses its own metadata:

@logger
def multiply(a, b):
    """Multiplies two numbers."""
    return a * b

print("\n=== 2.5 Identity Loss Problem ===")
print(multiply.__name__)   # 'wrapper' <- WRONG, should be 'multiply'
print(multiply.__doc__)    # None      <- docstring is gone

# The reason: multiply IS wrapper now. wrapper has its own __name__
# (literally the string 'wrapper') and its own __doc__ (None, since it
# has no docstring). The original function's identity is buried inside
# the closure, not exposed on the name that everyone else sees.


# ─────────────────────────────────────────────
# 2.6 THE FIX — functools.wraps
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

print("\n=== 2.6 After functools.wraps ===")
print(multiply.__name__)   # 'multiply' — correct
print(multiply.__doc__)    # 'Multiplies two numbers.' — correct

# @wraps(func) is not a nice-to-have — leave it out and every decorated
# function in a codebase reports itself as `wrapper` in tracebacks, docs,
# and introspection. Django, DRF, and Flask all rely on @wraps internally
# for exactly this reason. Treat it as mandatory whenever you write a
# decorator.


# ─────────────────────────────────────────────
# 2.7 FULL TRACE: timer, A SECOND DECORATOR ON THE SAME TEMPLATE
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
    """Sum of range n — deliberately slow."""
    total = 0
    for i in range(n):
        total += i
    return total

print("\n=== 2.7 timer decorator ===")
slow_sum(1_000_000)

# Same shape every time: capture something BEFORE the call, call the
# original via func(*args, **kwargs), do something AFTER the call, return
# the result. start/end live in wrapper's local scope; func lives in the
# closure. This is the general template — once you have it, logger,
# timer, caching decorators, retry decorators, and permission-check
# decorators are all the same skeleton with different "before" and
# "after" logic.


# ─────────────────────────────────────────────
# 2.8 THE MECHANISM MOST PEOPLE SKIP: HOW wrapper REMEMBERS func
# ─────────────────────────────────────────────

# logger(func) returns and its stack frame is, in the usual sense, gone.
# So how does wrapper still know what func is when it's called later?

def logger_explained(func):           # func = the original function, lives here
    def wrapper(*args, **kwargs):     # wrapper is defined inside logger_explained
        # func is a FREE VARIABLE inside wrapper:
        # not local to wrapper, not global —
        # it lives in logger_explained's scope (the enclosing scope).
        # LEGB lookup: L(wrapper) -> E(logger_explained) -> G(module) -> B(builtins)
        # Python finds `func` in E.
        result = func(*args, **kwargs)
        return result
    return wrapper                    # logger_explained returns and its frame
                                       # is, in the usual sense, gone — BUT
                                       # Python keeps func alive because
                                       # wrapper holds a reference to it
                                       # via closure

# This is a CLOSURE: wrapper carries a live reference to func bundled
# alongside it, even after logger_explained's own frame has finished
# executing. Python keeps the enclosing scope alive precisely because an
# inner function still references it. That reference is what makes
# decorators work at all — without it, func would be garbage the moment
# logger_explained returned.


# ─────────────────────────────────────────────
# 2.9 WHAT @decorator ACTUALLY DOES, AT DEFINITION TIME
# ─────────────────────────────────────────────

# This is the detail worth being airtight on: the decorator runs ONCE,
# when the module is loaded — not every time the decorated function is
# called.

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

# The EXACT equivalent without @ syntax:
def add_no_decorator(a, b):
    return a + b

add_no_decorator = logger_q3(add_no_decorator)   # <- this line is ALL @ does

print("\n=== 2.9 @ syntax vs explicit assignment ===")
add(3, 5)
add_no_decorator(3, 5)
# Both produce identical output — they ARE the same operation.

# What Python does when it hits @logger_q3 above a def, in order:
#
#   Step 1: Parses the def block and builds the original function object
#           (the real, undecorated add).
#
#   Step 2: Immediately calls logger_q3(add). logger_q3 runs, builds
#           wrapper (which closes over func = add via closure), and
#           returns wrapper.
#
#   Step 3: Rebinds the name `add` to point at the returned wrapper.
#           add = wrapper
#
#   Step 4: The original add function object still exists in memory —
#           but the only way to reach it now is through func inside
#           wrapper's closure. The name `add` itself only ever points to
#           wrapper.
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
# This is also why func.__name__ inside wrapper correctly says 'add' even
# though wrapper is what actually gets called — @wraps(func) copies that
# name across. Skip @wraps and wrapper.__name__ would say 'wrapper' instead.

# Proof that all of this happens at DEFINITION time, not call time:
print("\n=== 2.9b Proof: rebinding happens at definition time ===")

def spy(func):
    print(f"  spy called with: {func.__name__}")  # runs at DEFINITION
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

print("About to define decorated function:")

@spy
def do_something():      # spy() executes RIGHT HERE, while the module loads
    pass

print("Function defined. Now calling it:")
do_something()           # spy's print already happened — nothing new prints here

# Output, in order:
#   About to define decorated function:
#   spy called with: do_something
#   Function defined. Now calling it:
#
# do_something() produces no additional output — spy only ever runs once,
# at the moment @spy was processed. Calling do_something() afterward just
# invokes wrapper, which silently forwards to the original function.


# ─────────────────────────────────────────────
# 2.10 DECORATORS — SUMMARY
# ─────────────────────────────────────────────

# decorator        -> function that takes a function, returns a function
# wrapper          -> inner function that adds behavior around the original
# @syntax          -> shorthand for func = decorator(func) at DEFINITION time
#                     (not at call time — happens when module loads)
# *args/**kwargs   -> make wrapper forward any arguments to original
# @wraps(func)     -> preserve __name__, __doc__ from original
# closure          -> how wrapper remembers func after decorator returns
# name rebinding   -> after @decorator, the original name points to wrapper;
#                     original function only reachable via closure inside wrapper

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


# ─────────────────────────────────────────────
# 2.11 WHERE THE TWO IDEAS MEET
# ─────────────────────────────────────────────

# A decorator can wrap a GENERATOR function exactly the same way it wraps
# a normal one — func(*args, **kwargs) inside wrapper still just calls
# whatever func is, and if func is a generator function, calling it
# returns a generator object, which wrapper then returns unchanged. The
# wrapping logic (timing, logging, auth) doesn't need special-casing for
# generators — the pattern is orthogonal to what kind of function it wraps.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 3 — SELF-CHECK: QUESTIONS AND ANSWERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# Q1. What prints, and in what order, if you call next() three times on
#     infinite_counter() from §1.5, interleaved with your own print
#     statements between each call?
# ─────────────────────────────────────────────

def infinite_counter_q1():
    x = 0
    while True:
        x += 1
        yield x

print("\n=== Q1 ===")
g = infinite_counter_q1()

print("before first next")
print(next(g))          # 1
print("between calls")
print(next(g))           # 2
print("before third next")
print(next(g))           # 3

# ANSWER / EXPLANATION:
#
#   before first next
#   1
#   between calls
#   2
#   before third next
#   3
#
# There is nothing subtle hiding here — and that's the point of the
# question. Your own print() calls run on the main thread, in the exact
# order you wrote them, because calling next(g) is just a normal function
# call that returns a value and control comes straight back to you.
# The generator doesn't run "in the background" or on any kind of
# separate timeline — it only executes when next() is called on it, and
# it only executes UNTIL the next yield, then hands control back
# immediately. So interleaving your own prints with next() calls produces
# exactly the sequence you'd expect from reading top to bottom: nothing
# from inside infinite_counter_q1 ever "jumps ahead" of your surrounding
# code. The only thing that would look surprising is if you expected
# next(g) to print something itself — it doesn't, because
# infinite_counter_q1 has no print statements in it. All next(g) does is
# resume x += 1 and hand back the new x.


# ─────────────────────────────────────────────
# Q2. Write a decorator retry(func) that calls func, and if it raises an
#     exception, calls it exactly one more time before letting the
#     exception propagate. Use the standard template from §2.7.
# ─────────────────────────────────────────────

from functools import wraps

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)          # first attempt
        except Exception:
            print(f"  {func.__name__} failed once, retrying...")
            return func(*args, **kwargs)           # second and final attempt
            # if this also raises, the exception propagates naturally —
            # there is no second try/except around it
    return wrapper

# Demonstration — a function that fails the first time it's called,
# using a mutable default to simulate "flaky" behavior across calls:

call_count = {"n": 0}

@retry
def flaky_call():
    call_count["n"] += 1
    if call_count["n"] == 1:
        raise ValueError("simulated failure on first attempt")
    return "success"

print("\n=== Q2 ===")
print(flaky_call())   # "  flaky_call failed once, retrying..." then "success"

# ANSWER / EXPLANATION:
#
# This is the exact same shape as `timer` and `logger` — the only
# difference is that the "before/after" logic is replaced with a
# try/except around the call to func. Walking through why each piece is
# there:
#
#   - `return func(*args, **kwargs)` inside the try block: this is the
#     first attempt. If func succeeds, wrapper returns immediately and the
#     except block never runs — no retry happens on success, which is the
#     correct behavior.
#
#   - `except Exception:` catches ANY exception func might raise. In
#     production code you'd usually narrow this to specific exception
#     types (e.g. except requests.ConnectionError), because catching bare
#     Exception can silently swallow bugs you actually want to see. Here
#     it's intentionally broad to keep the demonstration simple.
#
#   - the second `return func(*args, **kwargs)` inside the except block:
#     this is "exactly one more time," as the question specifies. It is
#     NOT wrapped in its own try/except, which is deliberate — if this
#     second call also raises, there is nothing left to catch it, so the
#     exception propagates up to whoever called the decorated function.
#     That satisfies "before letting the exception propagate": the retry
#     happened once, and now the caller sees the real failure.
#
#   - @wraps(func) is still present, for the same reason as every other
#     decorator in this file: without it, flaky_call.__name__ would
#     report 'wrapper' instead of 'flaky_call'.
#
# A common mistake here is writing a loop with a retry COUNT instead of
# a single hardcoded extra attempt — that's a reasonable generalization,
# but it's solving a different (broader) problem than what was asked.
# The question specifically wants "exactly one more time," which is best
# expressed as two straight-line calls rather than a loop, since a loop
# implies a variable number of retries.


# ─────────────────────────────────────────────
# Q3. Counter.__iter__ in §1.9 uses yield. What would break if you
#     replaced the while loop with
#     return [i for i in range(1, self.n + 1)] instead — and would
#     list(c) still work?
# ─────────────────────────────────────────────

class CounterListVersion:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return [i for i in range(1, self.n + 1)]   # returns a LIST, not a generator

print("\n=== Q3 ===")
c2 = CounterListVersion(3)
print(list(c2))   # [1, 2, 3]
print(list(c2))   # [1, 2, 3] — also works!

# ANSWER / EXPLANATION:
#
# Nothing breaks, and list(c2) still works both times — but for a
# DIFFERENT reason than the generator version, and it's worth being clear
# on why.
#
# The __iter__ protocol only requires that __iter__ return SOMETHING that
# is itself an iterator (i.e. has __next__). A list is NOT an iterator —
# but list(c2) doesn't call __next__ directly on whatever __iter__
# returns. Under the hood, list(obj) calls iter(obj), which calls
# obj.__iter__(). If __iter__ returns a plain list, Python then calls
# iter() AGAIN on that list to get a genuine list_iterator object, and
# THAT is what actually gets pulled from via __next__.
#
# So `return [...]` technically violates the strict expectation that
# __iter__ returns an iterator directly — but Python's `iter()` builtin
# is lenient enough to paper over it in the specific case of list(),
# because list() calls iter() on its argument, and iter() knows how to
# get an iterator out of anything iterable, list included.
#
# Where it WOULD break: if you tried to call next() directly on the
# result of c2.__iter__() itself, instead of going through iter() again:
#
#     it = c2.__iter__()      # this is a LIST, e.g. [1, 2, 3]
#     next(it)                 # TypeError: 'list' object is not an iterator
#
# This fails because a list has __iter__ but not __next__ — it's
# ITERABLE, not an ITERATOR, and next() requires an iterator specifically.
# Code that does `for x in c2:` or `list(c2)` never hits this problem,
# because both of those go through the extra iter() call automatically.
# But any code that manually calls c2.__iter__() and expects to get
# something next()-able back would break.
#
# There's also a memory-behavior difference worth naming even though
# nothing "breaks": `return [i for i in range(1, self.n + 1)]` builds the
# ENTIRE list eagerly, every single time __iter__ is called — exactly the
# §1.6 list-vs-generator tradeoff, just relocated inside a class. The
# yield version keeps the original laziness (values computed one at a
# time, on demand); the list version throws that laziness away while
# still technically satisfying `for` loops and list(). For a Counter(3)
# this is invisible. For a Counter(10_000_000) it means every single
# `for x in c2:` eagerly materializes ten million ints up front before
# the loop even starts, which defeats the entire reason you'd reach for
# an __iter__-as-generator pattern in the first place.


print("\n=== END OF FILE ===")