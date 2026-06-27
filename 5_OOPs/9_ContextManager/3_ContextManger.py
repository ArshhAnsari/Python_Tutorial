"""
================================================================================
CONTEXT MANAGERS — Deep Dive (From First Principles)
A Mentor-Style Explanation File
Topics: resource leaks, try/finally, with statement mechanics,
        __enter__/__exit__ protocol, contextlib, exception handling, and bugs!
================================================================================

How to use this file:
Read it top to bottom. It is a fully runnable Python script. As you read the 
comments, run the file to see the concepts proved in the output.
"""

import os
import tempfile
import shutil
from contextlib import contextmanager

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SETUP — create a test file to work with throughout this script
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with open("test_file.txt", "w") as f:
    f.write("line 1\nline 2\nline 3\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1: THE PROBLEM — RESOURCE LEAKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*50 + "\nPART 1: THE PROBLEM\n" + "="*50)

# What happens if we don't use a context manager? 
# Beginners often write code like this:
#
# f = open("test_file.txt", "r")
# data = f.read()       <-- What if this line crashes?
# f.close()             <-- If the above crashes, this NEVER runs.

# If `f.close()` doesn't run, the file stays open in your system's memory.
# This is called a "Resource Leak". If a server does this 1,000 times, the OS 
# eventually says "Too many open files" and the entire server crashes.

# BEFORE context managers existed, we solved this with a `try/finally` block:
print("=== try/finally pattern (The Old Way) ===")

f = open("test_file.txt", "r")
try:
    data = f.read()
    print("  File read successfully.")
finally:
    f.close()           # 'finally' GUARANTEES this runs, even if a crash happens
    print("  File closed safely in finally block.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2: THE `with` STATEMENT — WHAT PYTHON ACTUALLY DOES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*50 + "\nPART 2: UNDER THE HOOD OF `with`\n" + "="*50)

# The `with` statement is just a cleaner, automatic way to do the try/finally 
# pattern above. It asks an object to manage its own setup and cleanup.

with open("test_file.txt", "r") as f:
    print("  Reading inside 'with' block.")

# When Python sees the code above, it essentially translates it to this:
#
#   manager = open("test_file.txt", "r")   <-- 1. Get the manager object
#   f = manager.__enter__()                <-- 2. Run SETUP, give result to 'f'
#   try:
#       print("Reading...")                <-- 3. Run YOUR code
#   finally:
#       manager.__exit__(...)              <-- 4. Run TEARDOWN (always!)

# Notice the 'as f' part. 
# 'f' is NOT always the manager object! 'f' is specifically whatever the 
# `__enter__()` method decides to hand back to you.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 3: THE PROTOCOL — WRITING A CLASS-BASED MANAGER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*50 + "\nPART 3: CLASS-BASED PROTOCOL\n" + "="*50)

# --- 3.1 THE BASIC PROTOCOL ---
class ManagedFile:
    def __init__(self, path, mode="r"):
        self.path = path
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"  [__enter__] opening: {self.path}")
        self.file = open(self.path, self.mode)
        # We return self.file! This is what gets assigned to 'f' in 'as f'
        return self.file 

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  [__exit__]  closing: {self.path}")
        if self.file:
            self.file.close()
        return False 

with ManagedFile("test_file.txt", "r") as f:
    print("  " + f.readline().strip())


# --- 3.2 INSPECTING EXCEPTION PARAMETERS ---
print("\n=== Inspecting __exit__ Parameters ===")
# What actually gets passed into exc_type, exc_val, and exc_tb? Let's force a crash.

class InspectingManager:
    def __enter__(self): 
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  exc_type → {exc_type}")       # e.g., <class 'ZeroDivisionError'>
        print(f"  exc_val  → {exc_val}")         # e.g., division by zero
        print(f"  exc_tb   → {exc_tb}")          # e.g., <traceback object>
        return False                            # Let the crash propagate

try:
    with InspectingManager():
        1 / 0
except ZeroDivisionError:
    print("  (Caught the ZeroDivisionError outside the with block)")


# --- 3.3 SUPPRESSING EXCEPTIONS (return True) ---
print("\n=== Suppressing Exceptions (return True) ===")
# Returning False means: "Let it crash."
# Returning True means: "Swallow the crash and pretend it didn't happen."

class SuppressingManager:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"  [exit] Suppressed a ValueError: {exc_val}")
            return True    # swallow — code continues after with
        return False       # everything else propagates

# Test 1: Suppressed Exception
with SuppressingManager():
    raise ValueError("hidden crash")
print("  This runs! The ValueError was completely swallowed.") 

# Test 2: Unsuppressed Exception
try:
    with SuppressingManager():
        raise TypeError("not hidden")
except TypeError:
    print("  TypeError propagated normally — not suppressed.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 4: THE SHORTCUT — `contextlib.contextmanager`
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*50 + "\nPART 4: THE GENERATOR SHORTCUT\n" + "="*50)

# Writing a whole class just for __enter__ and __exit__ is annoying.
# Python gives us a shortcut using a generator (a function with 'yield') 
# and a decorator.

# --- 4.1 YIELDING A VALUE ('as f') ---
@contextmanager
def managed_file_gen(path, mode="r"):
    print(f"  [enter] Opening {path} via generator")
    f = open(path, mode)
    try:
        # Think of 'yield' as a pause button. 
        # The variable you yield here is EXACTLY what 'as f' receives.
        yield f          
    finally:
        print(f"  [exit] Closing {path} via generator")
        f.close()

with managed_file_gen("test_file.txt") as f:
    print("  " + f.readline().strip())


# --- 4.2 YIELDING NOTHING (No 'as' needed) ---
@contextmanager
def simple_timer():
    import time
    start = time.time()
    print("  [enter] Timer started")
    try:
        yield  # Yielding nothing! We just want to pause.
    finally:
        elapsed = time.time() - start
        print(f"  [exit] Timer stopped. Elapsed: {elapsed:.5f}s")

with simple_timer():
    _ = sum(range(100000))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 5: THE DANGEROUS BUG (Why `try/finally` is mandatory)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*50 + "\nPART 5: THE DANGEROUS YIELD BUG\n" + "="*50)

# Look at this broken context manager. It uses yield, but forgets try/finally.
@contextmanager
def broken_manager():
    print("  [enter] Opening imaginary resource")
    yield "My Resource"
    # Wait, what happens if the 'with' block crashes?
    print("  [exit] Closing imaginary resource")

try:
    with broken_manager() as resource:
        print("  Inside with block.")
        print("  Uh oh, crashing the program now...")
        1 / 0  # ZeroDivisionError!
except ZeroDivisionError:
    print("  Caught the crash outside the block.")

# Notice in the output that "[exit] Closing imaginary resource" NEVER PRINTED!
# Why? 
# When a crash happens inside a 'with' block, Python takes that error and 
# literally throws it back INTO the generator at the exact line of the 'yield'.
# Because there was no try/finally protecting the yield, the generator exploded 
# instantly. The cleanup code was abandoned forever. Resource leak!


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 6: NESTED `WITH` BLOCKS AND LIFO STACKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*50 + "\nPART 6: NESTED MANAGERS (LIFO STACK)\n" + "="*50)

# You can open multiple things at once. 
@contextmanager
def block(name):
    print(f"  {name}: enter")
    try:
        yield
    finally:
        print(f"  {name}: exit")

# Watch the order of the output. 
with block("A"), block("B"):
    print("  inside")

# The output is:
# A: enter
# B: enter
# inside
# B: exit
# A: exit

# Why? Python treats them like a Last-In, First-Out (LIFO) stack.
# Entry happens left to right (A is pushed to stack, then B is pushed).
# Exit happens by popping off the top of the stack (B comes off, then A).
# This is crucial: if Resource B depends on Resource A being open, Python 
# safely tears down B *before* it tears down A.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 7: REAL WORLD EXAMPLES (Databases & Temp Files)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*50 + "\nPART 7: REAL WORLD EXAMPLES\n" + "="*50)

# Example 1: Guaranteed Temp Directory Cleanup
@contextmanager
def temp_directory():
    tmpdir = tempfile.mkdtemp()
    print(f"  [setup] created temp dir: {tmpdir}")
    try:
        yield tmpdir  # Hand the path to the with block
    finally:
        shutil.rmtree(tmpdir)
        print(f"  [teardown] deleted temp dir: {tmpdir}")

with temp_directory() as tmpdir:
    filepath = os.path.join(tmpdir, "data.txt")
    with open(filepath, "w") as f:
        f.write("Temporary data")
    print(f"  Working inside {filepath}")
# The directory is guaranteed gone here!


# Example 2: Database Transaction (Just like Django's transaction.atomic())
class DatabaseTransaction:
    def __init__(self):
        self.committed = False

    def __enter__(self):
        print(f"\n  [DB] BEGIN TRANSACTION")
        return self

    def commit(self):
        self.committed = True
        print(f"  [DB] COMMIT SUCCESSFUL")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"  [DB] CRASH DETECTED: {exc_val}. INITIATING ROLLBACK.")
            return False # Let the error continue to bubble up
        if not self.committed:
            self.commit() # Auto-commit if everything went fine
        return False

# Successful Transaction
with DatabaseTransaction() as tx:
    print("  Doing database work...")
    # tx.commit() happens automatically on exit

# Failing Transaction
try:
    with DatabaseTransaction() as tx:
        print("  Doing database work...")
        raise ValueError("Duplicate User Entry!")
except ValueError:
    print("  Handled the crash.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLEANUP (Removing our setup file)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if os.path.exists("test_file.txt"):
    os.remove("test_file.txt")
print("\n" + "="*50 + "\nEND OF LESSON - File cleaned up.\n" + "="*50)