"""
================================================================================
DECORATORS WITH ARGUMENTS + STACKING — A First-Principles Walkthrough
================================================================================

You already know the two-layer decorator shape: outer function takes func,
inner function (wrapper) does the work, outer returns wrapper. Everything here
is that same shape with one new wrinkle — what happens when the decorator
itself needs to take a CONFIGURATION argument, like @logger(level="INFO")
instead of just @logger. And separately: what happens when you STACK more
than one decorator on the same function. Neither needs new machinery — both
are the same closure mechanics you already have, nested one level deeper.

================================================================================
"""

from functools import wraps


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1 — DECORATORS THAT TAKE ARGUMENTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 1.1 THE SHAPE, BEFORE THE EXPLANATION
# ─────────────────────────────────────────────

# A normal decorator is TWO layers:
#
#   def logger(func):                    # layer 1: receives the function
#       def wrapper(*args, **kwargs):    # layer 2: runs on each call
#           ...
#       return wrapper
#
# A decorator that accepts its OWN argument — @logger(level="INFO") instead
# of bare @logger — is exactly that, with ONE EXTRA LAYER wrapped around
# the outside:
#
#   def logger(level):                   # layer 1: receives YOUR config
#       def decorator(func):             # layer 2: receives the function
#           def wrapper(*args, **kwargs):    # layer 3: runs on each call
#               ...
#           return wrapper
#       return decorator
#
# That's the whole idea. One more function on the outside, whose only job
# is to receive your configuration and hand back an ordinary two-layer
# decorator.


# ─────────────────────────────────────────────
# 1.2 WHY THE EXTRA LAYER IS NECESSARY
# ─────────────────────────────────────────────

# You already know @logger above a def is shorthand for name = logger(name)
# — ONE function call, at definition time.
#
# @logger(level="INFO") is shorthand for TWO function calls, chained:
#
#   add = logger(level="INFO")(add)
#              ↑                ↑
#         call #1: logger    call #2: whatever call #1 returned,
#         is called with     called again with the function
#         your config
#
# Read left to right: logger(level="INFO") runs first and produces
# SOMETHING. That something is then immediately called with add as its
# argument. For this to work, logger(level="INFO") has to evaluate to a
# callable that itself takes a function and returns a wrapper — i.e. it
# has to evaluate to an ordinary two-layer decorator. That's exactly what
# the outer layer (logger(level)) exists to produce.

# Without @ syntax:

def add_raw(a, b):
    return a + b

# _decorator = logger(level="DEBUG")   # step 1 — logger receives your config
# add_raw    = _decorator(add_raw)     # step 2 — decorator receives the function
# (logger isn't defined yet at this point in the file — see §1.3)


# ─────────────────────────────────────────────
# 1.3 BUILDING THE THREE-LAYER STRUCTURE
# ─────────────────────────────────────────────

def logger(level):                       # LAYER 1 — receives YOUR config
    """
    Outer function. Runs ONCE, at the moment @logger(level=...) is
    evaluated. Its only job is to hold `level` in a closure and hand back
    `decorator` — an ordinary function-to-wrapper decorator.
    """
    def decorator(func):                 # LAYER 2 — receives the function
        """
        Middle function. Runs ONCE, immediately after layer 1, when
        Python calls decorator(add). Its job is to hold `func` in a
        closure and hand back `wrapper`.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):    # LAYER 3 — runs on EVERY call
            """
            Inner function. This is what the name 'add' points to after
            decoration. Runs EVERY TIME the decorated function is called.
            """
            print(f"[{level}] → {func.__name__} called with args={args} kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"[{level}] → {func.__name__} returned {result}")
            return result
        return wrapper       # decorator hands back wrapper
    return decorator         # logger hands back decorator


# ─────────────────────────────────────────────
# 1.4 USING THE DECORATOR WITH ARGUMENTS
# ─────────────────────────────────────────────

@logger(level="INFO")
def add(a, b):
    return a + b

@logger(level="DEBUG")
def multiply(a, b):
    return a * b

@logger(level="WARNING")
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

print("=== 1.4 Decorator With Arguments ===")
add(2, 3)
multiply(4, 5)
divide(10, 2)

# Each decorated function ends up with its own `level` baked permanently
# into its closure — add always logs at INFO, multiply always at DEBUG,
# divide always at WARNING. Same decorator code, three different
# configurations, zero duplication.


# ─────────────────────────────────────────────
# 1.5 WHAT PYTHON DOES, STEP BY STEP, FOR @logger(level="INFO")
# ─────────────────────────────────────────────

# AT DEFINITION TIME (runs once, when the module loads):
#
#   1. logger(level="INFO") runs.
#        level = "INFO" is stored.
#        `decorator` is created, closing over level.
#          decorator's closure: {level: "INFO"}
#        logger returns decorator.
#        logger is now DONE — it will never run again for this `add`.
#
#   2. decorator(original_add) runs.
#        func = original_add is stored.
#        `wrapper` is created, closing over both func and level
#        (level is inherited from decorator's own enclosing scope).
#          wrapper's closure: {func: original_add, level: "INFO"}
#        decorator returns wrapper.
#        decorator is now DONE — it will never run again either.
#
#   3. The name `add` is reassigned to wrapper.
#        `add` no longer points to the original function.
#        The original function is only reachable through wrapper's closure.
#
#
# AT CALL TIME (runs every time you actually call add(...)):
#
#   add(2, 3)
#       ↓  add IS wrapper — the exact same object every call
#   wrapper(2, 3)
#       ↓  reads from its closure: level = "INFO", func = original_add
#       print("[INFO] → add called with args=(2, 3)")
#       result = func(2, 3)     →  original add(a=2, b=3)  →  5
#       print("[INFO] → add returned 5")
#       return 5                →  caller receives 5
#
# The critical thing to notice: logger and decorator are NEVER involved
# again after step 3. All the real work at call time happens inside
# wrapper, reading values that were frozen into its closure once, back at
# definition time. This is exactly why the three-layer structure is worth
# the extra indirection — the expensive-looking nesting only ever
# executes once per decorated function, not once per call.


# ─────────────────────────────────────────────
# 1.6 WRITING OUT A STACKED, ARGUMENT-TAKING DECORATOR WITH NO @ AT ALL
# ─────────────────────────────────────────────

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def greet(name):
    print(f"  Hi {name}")

# Expanding
#   @logger(level="DEBUG")
#   @repeat(times=2)
#   def greet(name): ...
# into explicit assignments, in the order Python actually applies them —
# BOTTOM decorator first:

# Step 1 — apply repeat(times=2), the bottom decorator, first:
_repeat_decorator = repeat(times=2)      # repeat receives times=2, returns decorator
greet = _repeat_decorator(greet)         # decorator receives greet, returns wrapper
# greet now points to repeat's wrapper

# Step 2 — apply logger(level="DEBUG") to the already-wrapped greet:
_logger_decorator = logger(level="DEBUG")   # logger receives level, returns decorator
greet = _logger_decorator(greet)            # decorator receives repeat's wrapper, returns wrapper
# greet now points to logger's wrapper
# logger's wrapper holds repeat's wrapper in its closure
# repeat's wrapper holds the original greet in its closure

print("\n=== 1.6 Without @ Syntax ===")
greet("Arsh")

# Output:
# [DEBUG] → greet called with args=('Arsh',) kwargs={}
#   Hi Arsh
#   Hi Arsh
# [DEBUG] → greet returned None
#
# greet runs twice (that's repeat's job), and the whole thing gets logged
# exactly once (that's logger's job, wrapping the outside).


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2 — STACKING DECORATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 2.1 THE CORE RULE
# ─────────────────────────────────────────────

# @decorator_one        ← applied SECOND — outermost layer
# @decorator_two        ← applied FIRST  — innermost layer
# def my_func(): ...
#
# APPLICATION order is bottom to top. Python processes decorators nearest
# the function first.
#
# EXECUTION order is top to bottom. The outermost wrapper runs first on
# every call, and it decides when (and whether) to call inward toward the
# next layer.
#
# These two orders being opposite is not a coincidence — the decorator
# applied last ends up as the OUTERMOST layer, because it's the last one
# to wrap something around what's already there. And being outermost is
# exactly what makes it run first on every call — it's the one the name
# my_func points to.
#
# Without @ syntax, stacking is just nested calls:
#
#   my_func = decorator_one(decorator_two(my_func))
#                           ↑              ↑
#                     applied 2nd    applied 1st (innermost)


# ─────────────────────────────────────────────
# 2.2 BASIC STACKING, TRACED FULLY
# ─────────────────────────────────────────────

def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("bold: before")
        result = func(*args, **kwargs)
        print("bold: after")
        return result
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("italic: before")
        result = func(*args, **kwargs)
        print("italic: after")
        return result
    return wrapper

@bold
@italic
def show(name):
    print(f"  Hello {name}")

print("\n=== 2.2 Basic Stacking ===")
show("Arsh")

# APPLICATION — two sequential reassignments of the name `show`, bottom
# decorator first:
#
#   Step 1 — italic wraps the original show:
#       show = italic(original_show)
#       show ──► [italic_wrapper]
#                     └─ closure: func ──► [original show]
#
#   Step 2 — bold wraps whatever `show` currently is (italic_wrapper):
#       show = bold(italic_wrapper)
#       show ──► [bold_wrapper]
#                     └─ closure: func ──► [italic_wrapper]
#                                               └─ closure: func ──► [original show]
#
# Notice the shape: a chain of closures, each one holding the next inward
# as `func`. That chain is what execution walks through.
#
# EXECUTION — calling show("Arsh") enters the chain from the outside and
# walks inward, then unwinds back outward:
#
#   show("Arsh")
#       ↓  show IS bold_wrapper
#   bold_wrapper("Arsh")
#       print("bold: before")
#       ↓  func("Arsh")  →  calls italic_wrapper
#       italic_wrapper("Arsh")
#           print("italic: before")
#           ↓  func("Arsh")  →  calls the original show
#           original show:  print("Hello Arsh")
#           print("italic: after")
#           return result
#       print("bold: after")
#       return result
#
# Output:
#   bold: before
#   italic: before
#     Hello Arsh
#   italic: after
#   bold: after
#
# "before" lines print outside-in (bold, then italic). "after" lines
# print inside-out (italic, then bold). Same shape as nested function
# calls or nested context managers — the thing that entered last is the
# thing that exits first, because each layer can only finish AFTER
# whatever it called returns.


# ─────────────────────────────────────────────
# 2.3 A SECOND FULL TRACE, TO MAKE THE PATTERN AUTOMATIC
# ─────────────────────────────────────────────

def prefix(text):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{text}: start")
            result = func(*args, **kwargs)
            print(f"{text}: end")
            return result
        return wrapper
    return decorator


@prefix("A")       # applied second — outermost
@prefix("B")       # applied first  — innermost
def run():
    print("  running")


print("\n=== 2.3 prefix Stacking Trace ===")
run()

# APPLICATION:
#   Step 1: prefix("B")(run)  →  B_wrapper; run = B_wrapper
#           B_wrapper's closure: {text: "B", func: original_run}
#
#   Step 2: prefix("A")(B_wrapper)  →  A_wrapper; run = A_wrapper
#           A_wrapper's closure: {text: "A", func: B_wrapper}
#
# EXECUTION:
#   run()
#       ↓  run IS A_wrapper
#   A_wrapper():
#       print("A: start")
#       ↓  func()  →  calls B_wrapper
#       B_wrapper():
#           print("B: start")
#           ↓  func()  →  calls original_run
#           original_run:  print("running")
#           print("B: end")
#           return
#       print("A: end")
#       return
#
# Output:
#   A: start
#   B: start
#     running
#   B: end
#   A: end
#
# Same shape as bold/italic — the decorator written CLOSER TO THE def
# (here, prefix("B")) is the one whose "start" prints last and whose
# "end" prints first, because it's the innermost layer, closest to the
# actual function call.


# ─────────────────────────────────────────────
# 2.4 STACKING A PLAIN DECORATOR WITH AN ARGUMENT-TAKING ONE
# ─────────────────────────────────────────────

# The two ideas from Part 1 and Part 2 combine with no special-casing — a
# three-layer decorator (logger) stacks with a plain two-layer one
# (repeat) exactly the same way two plain decorators stack.

@logger(level="INFO")     # applied second — outermost
@repeat(times=3)          # applied first  — innermost
def say(msg):
    print(f"  {msg}")

print("\n=== 2.4 Stacking With Arguments ===")
say("hello")

# APPLICATION:
#   Step 1: repeat(times=3)(say)  →  repeat_wrapper; say = repeat_wrapper
#           repeat_wrapper's closure: {times: 3, func: original_say}
#
#   Step 2: logger(level="INFO")(repeat_wrapper)  →  logger_wrapper; say = logger_wrapper
#           logger_wrapper's closure: {level: "INFO", func: repeat_wrapper}
#
# EXECUTION:
#   say("hello")
#       ↓  say IS logger_wrapper
#   logger_wrapper("hello"):
#       print("[INFO] → say called with args=('hello',)")
#       ↓  func("hello")  →  calls repeat_wrapper
#       repeat_wrapper("hello"):
#           calls original_say("hello") three times:
#               hello
#               hello
#               hello
#           returns the last result
#       print("[INFO] → say returned None")
#       return result
#
# Output:
#   [INFO] → say called with args=('hello',) kwargs={}
#     hello
#     hello
#     hello
#   [INFO] → say returned None
#
# repeat doesn't know or care that it's being wrapped by something with
# its own configuration; logger doesn't know or care that the function
# it's wrapping is itself a wrapper that runs things three times. Each
# decorator only ever sees "a callable that takes *args, **kwargs and
# returns something." That's the entire reason *args, **kwargs
# forwarding matters as much as it does — it's what makes decorators
# composable without any of them needing to know what's underneath them.


# ─────────────────────────────────────────────
# 2.5 WHERE DOES `level` ACTUALLY LIVE, AND WHAT KEEPS IT ALIVE?
# ─────────────────────────────────────────────

# After logger(level="INFO") returns, logger's own stack frame is gone —
# in the usual sense of a function call finishing and its locals being
# discarded. But level = "INFO" is still alive, because `decorator` was
# created INSIDE logger and closed over level at the moment it was
# defined. Then, one layer further in, `wrapper` is created inside
# decorator — and wrapper ALSO closes over level, inherited from
# decorator's own enclosing scope (this is the E in the LEGB lookup
# rule: Local -> Enclosing -> Global -> Built-in).
#
# So `level` ends up living in TWO SEPARATE CLOSURES SIMULTANEOUSLY:
#
#   decorator's closure  ->  {level: "INFO"}
#   wrapper's closure    ->  {level: "INFO", func: original_add}
#
# The mechanism keeping any of this alive is the closure itself: Python
# keeps a variable alive for as long as SOME function object holds a
# reference to it, regardless of whether the function that originally
# defined that variable has already returned. logger's frame being gone
# doesn't matter — wrapper still holds a live reference to level, so
# level persists.

def demo_closure():
    level = "INFO"
    def inner():
        return level        # level is captured here, via closure
    return inner

fn = demo_closure()          # demo_closure has already returned; its frame is gone

print("\n=== 2.5 Closure Inspection ===")
print(fn())                                # "INFO" — still alive
print(fn.__closure__[0].cell_contents)     # "INFO" — visible directly, as a closure cell

# fn.__closure__ is a tuple of "cell" objects, one per free variable the
# function references from an enclosing scope. Each cell holds the
# actual value. This is the same mechanism as the logger/decorator/
# wrapper chain, just with one function's worth of nesting instead of
# three.


# ─────────────────────────────────────────────
# 2.6 MENTAL MODEL, COMPRESSED
# ─────────────────────────────────────────────

# DECORATOR WITH ARGUMENTS — three layers, three distinct lifetimes:
#
#   def logger(level):            # runs once, when @logger(level=...) is evaluated
#       def decorator(func):      # runs once, immediately after, per decorated function
#           def wrapper(...):     # runs on every single call to the decorated function
#               ...
#           return wrapper
#       return decorator
#
#
# STACKING — an onion, built inside-out, executed outside-in:
#
#   @logger(level="INFO")     ← outermost layer: applied LAST, runs FIRST
#   @repeat(times=3)          ← inner layer:     applied FIRST, runs SECOND
#   def say(msg): ...          ← core:            runs LAST, returns FIRST
#
#
# THE CLOSURE CHAIN A STACKED DECORATOR LEAVES BEHIND:
#
#   name 'say' ──► [logger_wrapper]
#                       └─ closure: level="INFO"
#                                   func ──► [repeat_wrapper]
#                                                └─ closure: times=3
#                                                            func ──► [original say]
#
#
# THE RETURN VALUE HAS TO TRAVEL BACK OUT THROUGH EVERY LAYER:
#
#   original say returns its value
#       ↓
#   repeat_wrapper catches it, returns it onward
#       ↓
#   logger_wrapper catches it, returns it onward
#       ↓
#   caller finally receives it
#
# That last chain is the one bug worth internalizing before writing your
# own stacked decorators: if ANY layer forgets `return result` and just
# calls func(*args, **kwargs) without capturing and returning it, the
# value gets silently swallowed at that layer, and every caller further
# out gets None instead — with no error, no traceback, nothing to point
# you at which decorator in the stack ate the return value.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 3 — SELF-CHECK: QUESTIONS AND ANSWERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# Q1. Three decorators are stacked: @a, @b, @c (top to bottom) on def f():.
#     Each prints "<name> enter" before calling the wrapped function and
#     "<name> exit" after. What's the exact print order when f() is called?
# ─────────────────────────────────────────────

def make_trace_decorator(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{name} enter")
            result = func(*args, **kwargs)
            print(f"{name} exit")
            return result
        return wrapper
    return decorator

a = make_trace_decorator("a")
b = make_trace_decorator("b")
c = make_trace_decorator("c")

@a
@b
@c
def f():
    print("  f body")

print("\n=== Q1 ===")
f()

# ANSWER / EXPLANATION:
#
#   a enter
#   b enter
#   c enter
#     f body
#   c exit
#   b exit
#   a exit
#
# APPLICATION happens bottom to top: c wraps the original f first,
# then b wraps c's wrapper, then a wraps b's wrapper. That leaves f
# pointing at a_wrapper, whose closure holds b_wrapper, whose closure
# holds c_wrapper, whose closure holds the original f — three nested
# closures deep.
#
# EXECUTION then walks that chain from the outside in on the way down,
# and back out from the inside on the way back up — exactly the "onion"
# model from §2.6, just with one more layer than the bold/italic example
# had. a_wrapper is what f() actually is, so its "enter" print is
# unavoidably first: nothing can run before the outermost layer starts
# executing. It then calls inward to b_wrapper, which prints its own
# "enter" before calling further inward to c_wrapper, which prints
# "enter" and finally calls the real f body. Once the body finishes,
# execution unwinds back OUT through the same layers it went in through,
# in reverse — c's "exit" first (it's the last one that was entered),
# then b's, then a's last, since a was the first one entered and must be
# the last one to finish.
#
# The general rule this generalizes to: for N stacked decorators, the
# "enter" order matches the top-to-bottom @ order, and the "exit" order
# is the exact reverse of that. This is identical to how nested `with`
# blocks or nested try/finally blocks unwind — whatever opened last
# closes first.


# ─────────────────────────────────────────────
# Q2. Write debounce_count(n) — a decorator factory whose wrapper only
#     actually calls the wrapped function on every n-th call (all other
#     calls are no-ops that return None). Use the three-layer template
#     from §1.3.
# ─────────────────────────────────────────────

def debounce_count(n):
    def decorator(func):
        call_count = {"n": 0}          # mutable container, held in closure
        @wraps(func)
        def wrapper(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] % n == 0:
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator

@debounce_count(3)
def ping():
    print("  ping!")
    return "pong"

print("\n=== Q2 ===")
for i in range(1, 8):
    result = ping()
    print(f"  call {i} -> {result!r}")

# ANSWER / EXPLANATION:
#
# Expected output: ping() only actually prints "ping!" and returns
# "pong" on calls 3 and 6; every other call is a silent no-op returning
# None.
#
# This follows the exact same three-layer shape as `logger`:
#
#   - debounce_count(n): LAYER 1, receives config (n), runs once.
#   - decorator(func):   LAYER 2, receives the function, runs once.
#   - wrapper(...):      LAYER 3, runs on every call.
#
# The one new wrinkle is that `wrapper` needs to remember HOW MANY TIMES
# it has been called across separate invocations — and a plain local
# variable inside wrapper wouldn't work for this, because a fresh local
# scope is created every time wrapper runs, so `count = 0` written
# inside wrapper would reset to 0 on every call and never accumulate.
#
# The fix is to put the counter in `decorator`'s scope instead — one
# level UP from wrapper — because decorator only runs ONCE per decorated
# function, at definition time. A variable living there persists across
# every call to wrapper, exactly like `func` and `level` do in the
# logger example. There's a subtlety here worth naming: a plain
# `call_count = 0` in decorator's scope can be READ from wrapper via
# closure, but REASSIGNING it from inside wrapper (`call_count += 1`)
# would raise UnboundLocalError, because `+=` implies assignment, and
# assigning to a name inside a nested function makes Python treat it as
# LOCAL to that function unless you explicitly declare `nonlocal
# call_count`. Using a dict (`call_count = {"n": 0}`) sidesteps that
# entirely — wrapper isn't reassigning the name `call_count` itself, it's
# mutating the dict that name points to, which closures can always do
# without any special declaration. (`nonlocal call_count` plus
# `call_count += 1` on a plain int would also work — the mutable
# container is just the more common convention when a decorator needs to
# carry mutable state.)


# ─────────────────────────────────────────────
# Q3. In §2.4, repeat_wrapper calls original_say three times but only
#     ever returns the LAST result. Rewrite repeat so it instead returns
#     a list of all three results — and explain what has to change about
#     the loop to do that without touching logger at all.
# ─────────────────────────────────────────────

def repeat_collect(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@logger(level="INFO")
@repeat_collect(times=3)
def roll(msg):
    print(f"  {msg}")
    return msg.upper()

print("\n=== Q3 ===")
roll("hi")

# ANSWER / EXPLANATION:
#
# The only change needed is inside repeat's own wrapper — nothing about
# logger changes at all, which is the point of the question. That's a
# direct consequence of §2.4's observation: logger only ever sees "a
# callable that takes *args, **kwargs and returns something." It has no
# idea repeat is calling the inner function multiple times, and it
# doesn't need to — it just takes whatever single value comes back from
# calling repeat's wrapper and logs/returns THAT.
#
# The original version:
#
#   result = None
#   for _ in range(times):
#       result = func(*args, **kwargs)   # each iteration OVERWRITES result
#   return result                         # only the last call's value survives
#
# overwrites `result` on every pass, so only the final call's return
# value is ever visible outside the loop — the first two calls' results
# are computed and then immediately discarded.
#
# The fix replaces "overwrite a single variable" with "append to a
# list":
#
#   results = []
#   for _ in range(times):
#       results.append(func(*args, **kwargs))   # each iteration ADDS to results
#   return results                                # all three values survive
#
# Now `repeat_wrapper("hi")` returns ['HI', 'HI', 'HI'] instead of just
# 'HI'. From logger's point of view, absolutely nothing changed — it
# still calls func(*args, **kwargs) once, gets back a single object (now
# a list instead of a string), prints it, and returns it. logger has no
# mechanism for "knowing" what's inside the value it's forwarding, and it
# doesn't need one — that's exactly what makes stacking decorators
# composable: each layer's contract is "accept some arguments, return
# some single value," and what that value actually IS is none of the
# outer layer's business.


print("\n=== END OF FILE ===")