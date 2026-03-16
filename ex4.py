
class Heap:
    def __init__(self):
        self.heap = []


    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _heapify_down(self, i):
        smallest = i
        left = self._left(i)
        right = self._right(i)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)

    def _heapify_up(self, i):
        while i > 0 and self.heap[self._parent(i)] > self.heap[i]:
            parent = self._parent(i)
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent


    def heapify(self, arr):
        """Convert an array into a heap"""
        self.heap = arr[:]
        n = len(self.heap)

        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down(i)

    def enqueue(self, value):
        """Insert element into heap"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def dequeue(self):
        """Remove smallest element"""
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return root



def test_sorted_heap():
    """Test when input is already a valid heap"""
    h = Heap()
    arr = [1, 2, 3, 4, 5]
    h.heapify(arr)

    assert h.heap == [1, 2, 3, 4, 5]
    print("Test 1 passed (already heap)")


def test_empty_array():
    """Test heapify on empty array"""
    h = Heap()
    arr = []
    h.heapify(arr)

    assert h.heap == []
    print("Test 2 passed (empty array)")


def test_random_array():
    """Test heapify on random shuffled array"""
    import random

    h = Heap()
    arr = list(range(10))
    random.shuffle(arr)

    h.heapify(arr)

    for i in range(len(h.heap)):
        left = 2*i + 1
        right = 2*i + 2

        if left < len(h.heap):
            assert h.heap[i] <= h.heap[left]

        if right < len(h.heap):
            assert h.heap[i] <= h.heap[right]

    print("Test 3 passed (random array)")



if __name__ == "__main__":
    test_sorted_heap()
    test_empty_array()
    test_random_array()

    print("All tests passed.")