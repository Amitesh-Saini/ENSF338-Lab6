import random
import timeit
import statistics
from collections import deque

#4: In this approach Array Binary Search is significantly faster than BST search, because Arrays store elements contiguously in memory, They don't 
# have pointer chasing, and BST access pattern is random and unpredictable. 

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        """Insert a key into the BST"""
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)
    
    def _insert_recursive(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)
    
    def search(self, key):
        """Search for a key in the BST"""
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node is not None
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    def inorder_traversal(self):
        """Return sorted list of all keys (for verification)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)


def binary_search(arr, key):
    """Binary search on a sorted array"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == key:
            return True
        elif arr[mid] < key:
            left = mid + 1
        else:
            right = mid - 1
    return False


def measure_bst_performance(data):
    """Measure BST search performance"""
    bst = BinarySearchTree()
    for val in data:
        bst.insert(val)
    
    search_times = []
    for val in data:
        timer = timeit.Timer(lambda: bst.search(val))
        times = timer.repeat(repeat=10, number=1)
        avg_time = statistics.mean(times)
        search_times.append(avg_time)
    
    avg_search_time = statistics.mean(search_times)
    total_time = sum(search_times)
    
    return {
        'avg_time': avg_search_time,
        'total_time': total_time,
        'all_times': search_times
    }


def measure_array_binary_search_performance(data):
    """Measure binary search on sorted array performance"""
    sorted_data = sorted(data)
    
    search_times = []
    for val in data:
        timer = timeit.Timer(lambda: binary_search(sorted_data, val))
        times = timer.repeat(repeat=10, number=1)
        avg_time = statistics.mean(times)
        search_times.append(avg_time)
    
    avg_search_time = statistics.mean(search_times)
    total_time = sum(search_times)
    
    return {
        'avg_time': avg_search_time,
        'total_time': total_time,
        'all_times': search_times
    }


def run_experiment():
    print("=" * 60)
    print("BST vs ARRAY BINARY SEARCH PERFORMANCE COMPARISON")
    print("=" * 60)
    
    N = 10000
    print(f"\n1. Generating {N}-element vector...")
    sorted_vector = list(range(N))
    
    shuffled_vector = sorted_vector.copy()
    random.shuffle(shuffled_vector)
    print(f"   First 10 elements of shuffled vector: {shuffled_vector[:10]}...")
    
    # 2. Measure BST performance
    print(f"\n2. MEASURING BST PERFORMANCE")
    print("-" * 40)
    bst_results = measure_bst_performance(shuffled_vector)
    print(f"   Average search time per element: {bst_results['avg_time']:.10f} seconds")
    print(f"   Total search time for all elements: {bst_results['total_time']:.6f} seconds")
    
    # 3. Measure binary search on array performance
    print(f"\n3. MEASURING ARRAY BINARY SEARCH PERFORMANCE")
    print("-" * 40)
    array_results = measure_array_binary_search_performance(shuffled_vector)
    print(f"   Average search time per element: {array_results['avg_time']:.10f} seconds")
    print(f"   Total search time for all elements: {array_results['total_time']:.6f} seconds")
    
    print(f"\n4. DISCUSSION")
    print("-" * 40)
    
    if bst_results['avg_time'] < array_results['avg_time']:
        faster = "BST"
        ratio = array_results['avg_time'] / bst_results['avg_time']
    else:
        faster = "Array Binary Search"
        ratio = bst_results['avg_time'] / array_results['avg_time']
    
    print(f"   {faster} is approximately {ratio:.2f}x faster")
    print()
    
    print("   WHY IS THIS THE CASE?")
    print("   - BST search time: O(h) where h is tree height (can be O(n) in worst case,")
    print("     but O(log n) on average for random insertions)")
    print("   - Array binary search time: Always O(log n) with very low constant factors")
    print("   - Binary search on array typically wins because:")
    print("     * Arrays have better cache locality (contiguous memory)")
    print("     * No pointer dereferencing overhead")
    print("     * Predictable memory access patterns")
    print("     * Lower constant factors even though both are O(log n)")
    
    print(f"\n   Additional analysis:")
    print(f"   - For 10,000 elements, perfect BST height would be ~{int(log2(N)) + 1}")
    print(f"   - Random BST average height: ~{2*log2(N)}")
    print(f"   - Each BST search involves multiple pointer dereferences")
    print(f"   - Array binary search works entirely in CPU cache")


def plot_comparison(bst_results, array_results):
    """Optional: Create a simple visualization"""
    try:
        import matplotlib.pyplot as plt
        
        labels = ['BST', 'Array Binary Search']
        avg_times = [bst_results['avg_time'] * 1e6, array_results['avg_time'] * 1e6]  
        
        plt.figure(figsize=(8, 5))
        bars = plt.bar(labels, avg_times, color=['skyblue', 'lightcoral'])
        plt.ylabel('Average Search Time (microseconds)')
        plt.title('BST vs Array Binary Search Performance')
        plt.grid(axis='y', alpha=0.3)
        
        for bar, time in zip(bars, avg_times):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{time:.3f} µs', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("\nMatplotlib not installed. Skipping visualization.")


if __name__ == "__main__":
    from math import log2
    run_experiment()
    
   