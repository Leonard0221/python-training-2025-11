```markdown
# Python Interview Questions & Coding Challenges - Session 2

## Concept Questions

* What is the difference between mutable and immutable data types in Python?

    - Mutable data types → can be changed after creation (their contents can be modified in place).
    - Immutable data types → cannot be changed after creation (any modification creates a new object).

* What's the difference between a list and a tuple in Python?

    - List: Mutable — can be changed after creation
    - Tuple: Immutable — cannot be changed once created
    - Syntax: [ ] | ( )
    - Methods Available: Many (e.g. append(), remove(), sort()) | Few (only count() and index())
    - Performance: Slightly slower (mutable) | Faster (immutable and hashable)
    - Use Cases: When you need to modify, add, or remove items | When you need fixed data that shouldn’t change
    - Hashable (usable as dict key): No | Yes (if it contains only immutable elements)

* What's the difference between `list.append()`, `list.extend()`, and `list.insert()`?

    - append(): Adds a single element to the end of the list. It doesn’t flatten or unpack anything. It always increases the list length by 1
    - extend(): Adds all elements from another iterable (like a list, tuple, or string) to the end of the list. It iterates through the argument and appends each element. Extends the list with multiple elements.
    - insert(): list.insert(index, x), Inserts a single element at a specific position (index). Does not replace existing elements — it shifts them to the right.

* Explain the difference between shallow copy and deep copy between `list.copy()`, `list[:]`, and `copy.deepcopy()`

    - Shallow Copy (list[:] & list.copy()) : Creates a new container object (like a new list), but does not recursively copy the inner (nested) objects. Instead, it just copies references to them. So the operation changes to inner elements affect both copies.
    - Deep Copy (copy.deepcopy()): Creates a new container and recursively copies all nested objects. So the two objects become completely independent.

* What are the advantages and disadvantages of using set comprehensions vs converting a list comprehension to a set?

    - Set Comprehension: Uses curly braces {} directly.
    - converting a list comprehension to a set: Creates a list first, then converts it into a set.
    - They produce the same result, but differ internally in efficiency, readability, and intent.

* What's the time complexity difference between checking membership (`in` operator) in a list vs a set?

    - Lists are using Linear Search, Python checks each element one by one, O(n)
    - Sets are Hash Table Lookup, Sets store elements by their hash value, so membership check directly computes the hash and jumps to the bucket where the item should be. O(1) 

* Why are tuples immutable but you can still modify a list inside a tuple?
   
    - When we say a tuple is immutable, it means: Once created, the tuple’s structure — i.e., the sequence of object references it holds — cannot be changed. That means: You cannot add, remove, or replace elements in the tuple. But the objects inside the tuple can still change if they are mutable themselves.

* What will `my_list[::2]`, `my_list[::-1]`, and `my_list[1::3]` return for `my_list = [0,1,2,3,4,5,6,7,8,9]`?

    - `my_list[::2]` → “Every 2nd element”. Result: [0, 2, 4, 6, 8]
    - `my_list[::-1]` → “Reversed list”. Result: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    - `my_list[1::3]` → “Every 3rd element starting from index 1”. Result: [1, 4, 7]

* What's the difference between `remove()`, `pop()`, and `del` for lists?

    - remove(value): Removes the first matching value in the list.
    - pop(i): Removes and returns the element at the given index.
    - del list[i]: Deletes an element by index, or a slice of elements. Does not return anything.

---

## Coding Questions

### Coding Problem 1: Two Sum

**Problem:**  
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

**Description:**  
You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.

**Function Signature:**
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List containing indices of the two numbers
    
    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
        
        >>> two_sum([3, 2, 4], 6)
        [1, 2]
    """
    pass
```

---

### Coding Problem 2: Longest Substring Without Repeating Characters

**Problem:**  
Given a string `s`, find the length of the longest substring without repeating characters.

**Description:**  
A substring is a contiguous sequence of characters within a string. You need to find the longest substring where all characters are unique (no character appears more than once).

**Function Signature:**
```python
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.
    
    Args:
        s: Input string
    
    Returns:
        Integer representing the length of longest substring
    
    Example:
        >>> length_of_longest_substring("abcabcbb")
        3  # "abc"
        
        >>> length_of_longest_substring("bbbbb")
        1  # "b"
        
        >>> length_of_longest_substring("pwwkew")
        3  # "wke"
    """
    pass
```

---

### Coding Problem 3: Product of Array Except Self

**Problem:**  
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

**Description:**  
You must write an algorithm that runs in O(n) time and without using the division operation. The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

**Function Signature:**
```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    Calculate product of array except self.
    
    Args:
        nums: List of integers
    
    Returns:
        List where each element is the product of all other elements
    
    Example:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
        # For index 0: 2*3*4 = 24
        # For index 1: 1*3*4 = 12
        # For index 2: 1*2*4 = 8
        # For index 3: 1*2*3 = 6
        
        >>> product_except_self([-1, 1, 0, -3, 3])
        [0, 0, 9, 0, 0]
    """
    pass
```

---

### Coding Problem 4: Group Anagrams

**Problem:**  
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Description:**  
An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once. For example, "listen" and "silent" are anagrams.

**Function Signature:**
```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group anagrams together.
    
    Args:
        strs: List of strings
    
    Returns:
        List of lists, where each inner list contains anagrams
    
    Example:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
        
        >>> group_anagrams([""])
        [[""]]
        
        >>> group_anagrams(["a"])
        [["a"]]
    """
    pass
```