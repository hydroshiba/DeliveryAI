# heap.py
# =============================================================================
#  A wrapper class for the PriorityQueue class in Python's queue module that
#  allows for custom comparison methods.
# =============================================================================

from queue import PriorityQueue

class Heap:
    def __init__(self, comparator):
        self._heap = PriorityQueue()
        self._comparator = comparator

    class Item:
        def __init__(self, value, comparator):
            self._value = value
            self._comparator = comparator

        def __lt__(self, other):
            return self._comparator(self._value, other._value)
        
        def __eq__(self, other):
            return self._value == other._value

    def put(self, value):
        self._heap.put(self.Item(value, self._comparator))

    def get(self):
        return self._heap.get()._value
    
    def empty(self):
        return self._heap.empty()