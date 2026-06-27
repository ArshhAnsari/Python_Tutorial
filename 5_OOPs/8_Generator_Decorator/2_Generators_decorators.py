"""
================================================================================
DECORATORS WITH ARGUMENTS + STACKING — Deep Dive
Blog-style explanation file
Topics: 3-level decorator structure, closure chain, stacking mechanics,
        application order vs execution order, without-@ equivalents
================================================================================
"""

from functools import wraps


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1: DECORATOR WITH ARGUMENTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 1.1 THE ONE THING THAT MAKES THIS CLICK
# ─────────────────────────────────────────────

# A normal decorator is 2 layers:
#
#   def logger(func):           ← layer 1: receives function
#       def wrapper(...):       ← layer 2: runs on each call
#           ...
#       return wrapper
#
# A decorator WITH arguments is just ONE extra outer layer:
#
#   def logger(level):          ← layer 1: receives YOUR config
#       def decorator(func):    ← layer 2: receives function
#           def wrapper(...):   ← layer 3: runs on each call
#               ...
#           return wrapper
#       return decorator
#
# That's it. One extra function on the outside.


# ─────────────────────────────────────────────
# 1.2 WHY THE EXTRA LAYER IS NEEDED
# ─────────────────────────────────────────────

# Without arguments, Python translates @logger as:
#   add = logger(add)           ← logger receives function directly

# With arguments, Python translates @logger(level="DEBUG") as:
#   add = logger(level="DEBUG")(add)
#              ↑                 ↑
#   step 1: called with args    step 2: result called with function

# Two separate calls. The extra outer layer handles step 1.
# Step 1 returns a plain decorator. Step 2 is the normal decoration.

# Without @ syntax — IDENTICAL to what @ does:
def add_raw(a, b):
    return a + b

# What @logger(level="DEBUG") expands to:
# _decorator = logger(level="DEBUG")   # step 1
# add_raw    = _decorator(add_raw)     # step 2


# ─────────────────────────────────────────────
# 1.3 BUILDING THE 3-LAYER STRUCTURE
# ─────────────────────────────────────────────

def logger(level):                       # LAYER 1 — receives YOUR config
    """
    Outer function. Receives arguments (config).
    Job: store config in closure, return a decorator.
    Runs ONCE at definition time. Never again.
    """
    def decorator(func):                 # LAYER 2 — receives function
        """
        Middle function. Receives the actual function being decorated.
        Job: store function reference in closure, return wrapper.
        Runs ONCE at definition time. Never again.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):    # LAYER 3 — runs on EVERY call
            """
            Inner function. This is what the name 'add' points to after decoration.
            Job: add behavior before/after, call original, return result.
            Runs EVERY TIME you call the decorated function.
            """
            # ── BEFORE ──
            print(f"[{level}] → {func.__name__} called with args={args} kwargs={kwargs}")

            # ── ORIGINAL CALL ──
            result = func(*args, **kwargs)    # calls the real function

            # ── AFTER ──
            print(f"[{level}] → {func.__name__} returned {result}")

            return result                     # bucket passed upward to caller
        return wrapper      # decorator returns wrapper
    return decorator        # logger returns decorator


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

print("=== Decorator With Arguments ===")
add(2, 3)
multiply(4, 5)
divide(10, 2)

# Each function gets its OWN level baked into its closure permanently.
# add      → level="INFO"    forever
# multiply → level="DEBUG"   forever
# divide   → level="WARNING" forever
#
# Same decorator. Different configuration. Zero code duplication.


# ─────────────────────────────────────────────
# 1.5 WHAT PYTHON DOES STEP BY STEP — @logger(level="INFO")
# ─────────────────────────────────────────────

# DEFINITION TIME (runs once when file loads):
#
# Step 1: logger(level="INFO")
#             level = "INFO" stored
#             decorator created
#             decorator's closure = {level: "INFO"}
#             logger returns decorator
#             LOGGER IS DONE — never runs again
#
# Step 2: decorator(original_add)
#             func = original_add stored
#             wrapper created
#             wrapper's closure = {func: original_add, level: "INFO"}
#             decorator returns wrapper
#             DECORATOR IS DONE — never runs again
#
# Step 3: name 'add' = wrapper  ← THE ROBBERY
#             'add' no longer points to original function
#             'add' now points to wrapper
#             original function only reachable via wrapper's closure
#
#
# CALL TIME (runs every time you call add):
#
# add(2, 3)
#     ↓ add IS wrapper — same object
# wrapper(2, 3)
#     ↓ opens closure chip
#     level = "INFO"        (from decorator's closure, inherited)
#     func  = original_add  (from decorator's closure)
#     ↓
#     print("[INFO] → add called with args=(2, 3)")
#     result = func(2, 3)   → original add(a=2, b=3) → returns 5
#     print("[INFO] → add returned 5")
#     return 5              → caller receives 5
#
# logger and decorator are NEVER involved again after definition


# ─────────────────────────────────────────────
# 1.6 WITHOUT @ SYNTAX — EVERY STEP EXPLICIT (Q2)
# ─────────────────────────────────────────────

# Q2 FROM SESSION:
# Write the equivalent of:
#   @logger(level="DEBUG")
#   @repeat(times=2)
#   def greet(name): ...
# without @ syntax, every intermediate step.

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

# Step 1: Apply repeat(times=2) to greet — bottom decorator first
_repeat_decorator = repeat(times=2)        # repeat receives times=2, returns decorator
greet = _repeat_decorator(greet)           # decorator receives greet, returns wrapper
# greet now points to repeat's wrapper

# Step 2: Apply logger(level="DEBUG") to the already-wrapped greet
_logger_decorator = logger(level="DEBUG")  # logger receives level, returns decorator
greet = _logger_decorator(greet)           # decorator receives repeat_wrapper, returns wrapper
# greet now points to logger's wrapper
# logger's wrapper holds repeat_wrapper in its closure
# repeat's wrapper holds original greet in its closure

print("\n=== Q2: Without @ Syntax ===")
greet("Arsh")

# Output:
# [DEBUG] → greet called with args=('Arsh',) kwargs={}
#   Hi Arsh
#   Hi Arsh
# [DEBUG] → greet returned None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2: STACKING DECORATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ─────────────────────────────────────────────
# 2.1 THE CORE RULE
# ─────────────────────────────────────────────

# @decorator_one      ← applied SECOND (outermost layer)
# @decorator_two      ← applied FIRST  (innermost layer)
# def my_func(): ...
#
# Application order: BOTTOM to TOP   (like a stack being built)
# Execution order:   TOP to BOTTOM   (like an onion being peeled)
#
# Equivalent without @:
# my_func = decorator_one(decorator_two(my_func))
#                         ↑              ↑
#                   applied 2nd    applied 1st


# ─────────────────────────────────────────────
# 2.2 BASIC STACKING — TWO ROBBERIES
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

print("\n=== Basic Stacking ===")
show("Arsh")

# APPLICATION (bottom to top — two robberies):
#
# Robbery 1 — italic steals 'show':
#   show = italic(original_show)
#   show ──► [italic_wrapper]
#                 └─ closure: func ──► [original show]
#
# Robbery 2 — bold steals 'show' from italic:
#   show = bold(italic_wrapper)
#   show ──► [bold_wrapper]
#                 └─ closure: func ──► [italic_wrapper]
#                                           └─ closure: func ──► [original show]
#
# EXECUTION (top to bottom — chain enters inward, exits outward):
#
# show("Arsh")
#     ↓ show IS bold_wrapper
# bold_wrapper("Arsh")
#     print("bold: before")
#     ↓ func("Arsh") → calls italic_wrapper
#     italic_wrapper("Arsh")
#         print("italic: before")
#         ↓ func("Arsh") → calls original show
#         original show: print("Hello Arsh")
#         print("italic: after")
#         return result
#     print("bold: after")
#     return result
#
# Output:
# bold: before
# italic: before
#   Hello Arsh
# italic: after
# bold: after


# ─────────────────────────────────────────────
# 2.3 Q1 FROM SESSION — TRACE THIS MANUALLY
# ─────────────────────────────────────────────

# Q: What is the exact output?

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


print("\n=== Q1: prefix stacking trace ===")
run()

# APPLICATION (bottom to top):
# Step 1: prefix("B")(run) → B_wrapper; run = B_wrapper
#         B_wrapper's closure: {text: "B", func: original_run}
#
# Step 2: prefix("A")(B_wrapper) → A_wrapper; run = A_wrapper
#         A_wrapper's closure: {text: "A", func: B_wrapper}
#
# EXECUTION (top to bottom):
# run()
#     ↓ run IS A_wrapper
# A_wrapper():
#     print("A: start")
#     ↓ func() → calls B_wrapper
#     B_wrapper():
#         print("B: start")
#         ↓ func() → calls original_run
#         original_run: print("running")
#         print("B: end")
#         return
#     print("A: end")
#     return
#
# Output:
# A: start
# B: start
#   running
# B: end
# A: end


# ─────────────────────────────────────────────
# 2.4 STACKING WITH ARGUMENTS
# ─────────────────────────────────────────────

print("\n=== Stacking With Arguments ===")

@logger(level="INFO")     # applied second — outermost
@repeat(times=3)          # applied first  — innermost
def say(msg):
    print(f"  {msg}")

say("hello")

# APPLICATION (bottom to top):
# Step 1: repeat(times=3)(say)         → repeat_wrapper; say = repeat_wrapper
#         repeat_wrapper's closure: {times: 3, func: original_say}
#
# Step 2: logger(level="INFO")(repeat_wrapper) → logger_wrapper; say = logger_wrapper
#         logger_wrapper's closure: {level: "INFO", func: repeat_wrapper}
#
# EXECUTION (top to bottom):
# say("hello")
#     ↓ say IS logger_wrapper
# logger_wrapper("hello"):
#     print("[INFO] → say called with args=('hello',)")
#     ↓ func("hello") → calls repeat_wrapper
#     repeat_wrapper("hello"):
#         calls original_say("hello") × 3
#           hello
#           hello
#           hello
#         returns result
#     print("[INFO] → say returned None")
#     return result
#
# Output:
# [INFO] → say called with args=('hello',) kwargs={}
#   hello
#   hello
#   hello
# [INFO] → say returned None


# ─────────────────────────────────────────────
# 2.5 Q3 FROM SESSION — WHERE DOES level LIVE?
# ─────────────────────────────────────────────

# Q: Where does level live after logger(level="INFO") returns?
#    What keeps it alive? Name the mechanism.
#
# Answer:
# After logger(level="INFO") returns, logger's stack frame is gone.
# BUT level = "INFO" is still alive — stored inside decorator's closure.
# decorator was created inside logger and closed over level.
# When wrapper is created inside decorator, it ALSO closes over level
# (inherited from decorator's enclosing scope — LEGB E rule).
#
# level lives in TWO closures simultaneously:
#   decorator's closure → {level: "INFO"}
#   wrapper's closure   → {level: "INFO", func: original_add}
#
# The mechanism keeping it alive: CLOSURE
# Python keeps any variable alive as long as a function object
# holds a reference to it via closure, even after the enclosing
# function has returned and its stack frame has been destroyed.
#
# Inspectable:
def demo_closure():
    level = "INFO"
    def inner():
        return level     # level captured in closure
    return inner

fn = demo_closure()      # demo_closure is done, frame gone
print("\n=== Q3: Closure inspection ===")
print(fn())                              # "INFO" — still alive
print(fn.__closure__[0].cell_contents)  # "INFO" — visible in closure cell


# ─────────────────────────────────────────────
# 2.6 MENTAL MODEL SUMMARY
# ─────────────────────────────────────────────

# DECORATOR WITH ARGUMENTS — three layers, three jobs:
#
#   def logger(level):           ← receives YOUR config
#       def decorator(func):     ← receives the function
#           def wrapper(...):    ← runs on EVERY actual call
#               ...
#           return wrapper
#       return decorator
#
#
# STACKING — onion layers:
#
#   @logger(level="INFO")        ← outermost layer (applied last, runs first)
#   @repeat(times=3)             ← inner layer     (applied first, runs second)
#   def say(msg): ...            ← core            (runs last, returns first)
#
#   Application:  inside-out  (bottom decorator applied first)
#   Execution:    outside-in  (top decorator runs first on each call)
#
#
# CLOSURE CHAIN FOR STACKED DECORATORS:
#
#   name 'say' ──► [logger_wrapper]
#                       └─ closure: level="INFO"
#                                   func ──► [repeat_wrapper]
#                                                └─ closure: times=3
#                                                            func ──► [original say]
#
#
# RETURN VALUE CHAIN:
#
#   original say returns value
#       ↓
#   repeat_wrapper catches, returns it
#       ↓
#   logger_wrapper catches, returns it
#       ↓
#   caller receives value
#
# If ANY layer forgets to return result → value swallowed → caller gets None