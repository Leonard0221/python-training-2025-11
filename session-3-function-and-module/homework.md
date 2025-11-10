# Python Coding Questions - Session 3: Recursion & Functions

## Concept Questions

* What is a lambda function, and how is it different from a regular function in Python?
    - A lambda function in Python is a small, anonymous function — meaning it doesn’t have a formal name like a normal function defined with def
  
* What is the difference between `*args` and `**kwargs` in function definitions?
    - *args — Variable Positional Arguments. Used to pass any number of positional (non-keyword) arguments to a function. Inside the function, args becomes a tuple containing all extra positional arguments.
    - Used to pass any number of keyword (named) arguments to a function. Inside the function, kwargs becomes a dictionary where: Keys = argument names Values = argument values. 
  
* What is LEGB? Explain LEGB rule with a code example
    - The LEGB rule in Python defines the scope resolution order — i.e., where Python looks for variables when you reference a name. It stands for: L → Local, E → Enclosing, G → Global, B → Built-in
    - Scope	    Meaning	        Example                                     Context
    L (Local)	Names defined inside a function (including its parameters)	Variables in the current function
    E (Enclosing)	Names in any enclosing (outer) functions — applies in nested functions	Variables in outer function but not global
    G (Global)	Names defined at the top level of a module/script	Variables declared outside all functions
    B (Built-in)	Names preloaded into Python (like len, print, sum, etc.)	Always available without import

* What is a closure in Python? How is it different from a regular nested function?
    - A closure = a nested function that captures and remembers variables from its enclosing scope, allowing it to use those values even after the outer function has returned — unlike a regular nested function, which loses access once its outer scope ends.    
  
* What is the purpose of `if __name__ == "__main__":`?
    - It is a Python convention that controls whether a block of code runs when a script is executed directly or imported as a module. Purpose: It ensures that certain code (like tests, demos, or the main program logic) only runs when the file is executed directly, and not when imported into another Python file.
  
* Can you modify a global variable inside a function without using the `global` keyword?
    - In general, you cannot directly modify a global variable inside a function without declaring it as global — unless you’re only mutating a mutable object (like a list or dictionary), not rebinding the variable name itself.
    - UnboundLocalError
    - You can read or mutate global objects without global, but to reassign or rebind a global variable name, you must use the global keyword.
  
* In what order must you define parameters in a function signature?
    - Positional-only (before /)
    - Positional-or-keyword (regular params)
    - Defaulted versions of the above (non-defaults must come first)
    - *args (var-positional)
    - Keyword-only (after *), with or without defaults
    - **kwargs (var-keyword)

* What is the difference between the `global` and `nonlocal` keywords?
    - global: Rebinds a name in the module/global scope.
    - nonlocal: Rebinds a name in the nearest enclosing (non-global) scope (used inside nested functions).
  
* What is a common pitfall when using mutable default arguments?
    - Defaults are evaluated once at function definition, so a mutable default (e.g., [], {}) is shared across calls.
  
* What is a higher-order function? Give examples of built-in higher-order functions
    - A higher-order function either takes functions as arguments or returns a function.
    - map(func, iterable)
    - filter(func, iterable)
    - sorted(iterable, key=func) and list.sort(key=func)
    - max(iterable, key=func) / min(iterable, key=func)
    - functools.reduce(func, iterable) (from functools)
---

## Coding Questions
### Coding Problem 1: Fibonacci Sequence with Optimization

**Problem:**  
Write a recursive function to calculate the nth Fibonacci number.

**Description:**  
The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, starting from 0 and 1.
- Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
- Formula: F(n) = F(n-1) + F(n-2), where F(0) = 0 and F(1) = 1

**Requirements:**
- Must use recursion
- Must be efficient enough to handle large values (e.g., n = 50 or higher) without timing out
- Time complexity should be O(n), not O(2^n)
- Hint: Consider using memoization/caching to optimize your solution

**Function Signature:**
```python

from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using optimized recursion.
    
    Args:
        n: Position in Fibonacci sequence (0-indexed)
    
    Returns:
        The nth Fibonacci number
    
    Example:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(6)
        8
        >>> fibonacci(10)
        55
        >>> fibonacci(50)
        12586269025
    """
    if n <= 1:
        return n
    elif n < 0:
        raise ValueError()
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```

---

## Coding Problem 2: Maximum Value in Nested List

**Problem:**  
Write a recursive function to find the maximum value in a nested list structure of arbitrary depth.

**Description:**  
Given a list that may contain integers and other lists (which may also contain integers and lists), find the maximum integer value at any level of nesting. The list can be nested to any depth.

**Function Signature:**
```python
def find_max_nested(nested_list: list) -> int:
    """
    Find the maximum value in a nested list structure using recursion.
    
    Args:
        nested_list: A list containing integers and/or other nested lists
    
    Returns:
        The maximum integer value found at any nesting level
    
    Example:
        >>> find_max_nested([1, 2, 3, 4, 5])
        5
        
        >>> find_max_nested([1, [2, 3], 4, [5, [6, 7]]])
        7
        
        >>> find_max_nested([[1, 2], [3, [4, [5, 6]]], 7])
        7
        
        >>> find_max_nested([10, [20, [30, [40, [50]]]]])
        50
    """
    max_number = -inf
    max_number = float('-inf')
    for element in nested_list:
        if isinstance(element, list):
            temp = find_max_nested(element)
            max_number = max(max_number, temp)
        else:
            max_number = max(max_number, element)
    return max_number
```

---

## Coding Problem 3: Reverse String Using Recursion

**Problem:**  
Write a recursive function to reverse a string without using built-in reverse methods, slicing, or any iteration.

**Description:**  
Given a string, reverse it using only recursion. You cannot use:
- String slicing (`s[::-1]`)
- The `reversed()` function
- Any loops (`for`, `while`)
- The `.reverse()` method
- List comprehensions or any iterative constructs

You must solve this purely using recursive function calls.

**Function Signature:**
```python
def reverse_string(s: str) -> str:
    """
    Reverse a string using only recursion (no loops, slicing, or built-in reverse).
    
    Args:
        s: Input string to reverse
    
    Returns:
        Reversed string
    
    Example:
        >>> reverse_string("hello")
        "olleh"
        
        >>> reverse_string("Python")
        "nohtyP"
        
        >>> reverse_string("a")
        "a"
        
        >>> reverse_string("")
        ""
        
        >>> reverse_string("racecar")
        "racecar"
    """
    if len(s) == 1:
        return s
    else:
        return reverse_string(s[1:]) + s[0]
```

---