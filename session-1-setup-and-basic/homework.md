# Python Interview Questions & Coding Challenges - Session 1

## Concept Questions

* What is Python's main characteristic regarding syntax compared to other programming languages?
  
  Python’s syntax is clear, concise, and human-readable. It emphasizes readability by using indentation instead of braces {} or keywords to define code blocks (like loops or functions). This makes Python code look cleaner and closer to natural language.

* What are the basic data types available in Python?
  
  int – integers (5, -3)
  float – decimal numbers (3.14)
  str – strings ("Hello")
  bool – Boolean values (True, False)
  list – ordered, mutable sequences ([1, 2, 3])
  tuple – ordered, immutable sequences ((1, 2, 3))
  set – unordered collections of unique elements ({1, 2, 3})
  dict – key-value pairs ({"name": "Leonard", "age": 25})

* Why is indentation important in Python?
  
  Indentation defines code blocks (like inside functions, loops, and conditionals).Unlike many languages, Python does not use braces {} — incorrect indentation causes a IndentationError and changes how the program runs logically.

* What happens when you try to mix incompatible data types in an operation?
  
  Python raises a TypeError.

* What is Git Flow?
  
  Git Flow is a branching model that defines a structured workflow for managing releases and collaboration. It helps teams coordinate parallel development efficiently.
  
  Main branches:
  main (or master) – stable production code
  develop – integration branch for new features
  
  Supporting branches:
  feature/ – for new features
  release/ – for preparing releases
  hotfix/ – for emergency fixes on production

* Explain the difference between `==` and `is` operators
  
  "==" checks value equality (whether two objects have the same content).
  "is" checks identity equality (whether two variables point to the same object in memory).

* What's the difference between implicit and explicit type conversion?
  
  Implicit conversion (coercion) – Python automatically converts types when safe. result = 5 + 3.0  # int -> float automatically
  Explicit conversion (casting) – You manually convert using functions like int(), float(), str() int("10")  # 10
  
* What's the difference between `if x:` and `if x == True:`?
  
  if x: checks the truthiness of x — whether it’s considered True in a Boolean context.(e.g., non-zero numbers, non-empty strings/lists are True)
  
  if x == True: checks if x is exactly equal to True.

---

## Coding Questions

### Coding Problem 1: Palindrome Checker

**Problem:**  
Write a function that checks if a string is a palindrome (reads the same forwards and backwards), ignoring spaces, punctuation, and case.

**Description:**  
A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward. Your function should:
- Ignore spaces
- Ignore punctuation marks
- Be case-insensitive
- Return `True` if the string is a palindrome, `False` otherwise

**Function Signature:**
```python

def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.
    
    Args:
        s (str): Input string to check
    
    Returns:
        bool: True if palindrome, False otherwise
    
    Example:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    string = "".join(i.lower() for i in s if i.isalnum())    
    left , right = 0, len(string) - 1
    while left < right:
        if string[left] != string[right]:
            return False
        left += 1
        right -= 1
    return True

```
---

### Coding Problem 2: Valid Parentheses

**Problem:**  
Given a string containing just the characters `'(', ')', '{', '}', '[', ']'`, determine if the input string is valid.

**Description:**  
A string is considered valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type
4. Every open bracket must have a corresponding close bracket

**Function Signature:**
```python

def is_valid_parentheses(s: str) -> bool:
    """
    Check if a string has valid parentheses.
    
    Args:
        s (str): String containing only '(', ')', '{', '}', '[', ']'
    
    Returns:
        bool: True if parentheses are valid, False otherwise
    
    Example:
        >>> is_valid_parentheses("()")
        True
        >>> is_valid_parentheses("()[]{}")
        True
        >>> is_valid_parentheses("(]")
        False
    """
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for i in s:
        if i in pairs.values():
            stack.append(i)
        elif i in pairs.keys():
            if pairs[i] != stack[-1] or stack == []:
                return False
            else:
                stack.pop()
    return True

```