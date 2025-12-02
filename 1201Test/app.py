class LRUCache:
    class _Node():
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None
            self.prev = None
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache = {}
        self.head = self._Node("","")
        self.tail = self._Node("","")
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def _recent_access(self, node):
        self._pop_helper(node)
        self._add(node)
    
    def _add(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _pop(self):
        temp = self.tail.prev
        if temp is self.head:
            return None
        self._pop_helper(temp)
        return temp

    def _pop_helper(self, node):
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node
        node.prev = node.next = None
    
    def get(self, key: str) -> str | None:
        node = self.cache.get(key)
        if not node:
            return None
        self._recent_access(node)
        return node.value

    def put(self, key: str, value: str) -> None:
        node = self.cache.get(key)
        if node:
            node.value = value
            self._recent_access(node)
            return
        new = self._Node(key, value)
        self.cache[key] = new
        self._add(new)
        if len(self.cache) > self.capacity:
            lru = self._pop()
            if lru:
                del self.cache[lru.key]
                
                # cache = LRUCache(2)
                
                
                
if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put("a", "apple")
    cache.put("b", "banana")
    print(cache.get("a"))  # "apple"
    cache.put("c", "cherry")  # evicts "b"
    print(cache.get("b"))  # None
    cache.put("d", "date")    # evicts "a"
    print(cache.get("a"))  # None
    print(cache.get("c"))  # "cherry"
    print(cache.get("d"))  # "date"
        