import random
import timeit
import statistics
import heapq
from dataclasses import dataclass
from typing import Optional, List, Any

#4: for this implimentation the HeapPriorityQueue is significantly faster than the ListPriorityQueue. HeapPriorityQueue is better because it has a better complexity 
# (ListPriorityQueue: Enqueue: O(n), Dequeue: O(1)) (HeapPriorityQueue: Both enqueue and dequeue: O(log n)).
#



class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class ListPriorityQueue:
    """Priority queue implemented using a sorted linked list"""
    
    def __init__(self):
        self.head = None
        self.size = 0
    
    def enqueue(self, value):
        """Insert element in order (smallest to largest)"""
        new_node = Node(value)
        self.size += 1
        
        if self.head is None or value < self.head.value:
            new_node.next = self.head
            self.head = new_node
            return
        
        current = self.head
        while current.next is not None and current.next.value < value:
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
    
    def dequeue(self):
        """Retrieve and remove the smallest element (at head)"""
        if self.head is None:
            return None  
        
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return "[" + ", ".join(values) + "]"


class HeapPriorityQueue:
    """Priority queue implemented using a binary heap"""
    
    def __init__(self):
        self.heap = []
    
    def enqueue(self, value):
        """Insert element into heap"""
        heapq.heappush(self.heap, value)
    
    def dequeue(self):
        """Retrieve and remove smallest element from heap"""
        if not self.heap:
            return None
        return heapq.heappop(self.heap)
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def __len__(self):
        return len(self.heap)
    
    def __str__(self):
        return str(self.heap)


def generate_tasks(num_tasks=1000, enqueue_prob=0.7):
    """
    Generate a list of tasks:
    - enqueue: add random integer with probability enqueue_prob
    - dequeue: remove element with probability (1 - enqueue_prob)
    """
    tasks = []
    for _ in range(num_tasks):
        if random.random() < enqueue_prob:
            value = random.randint(1, 10000)
            tasks.append(('enqueue', value))
        else:
            tasks.append(('dequeue', None))
    return tasks


def measure_queue_performance(queue_class, tasks, queue_name):
    """Measure time to process tasks with given queue implementation"""
    
    def process_tasks():
        queue = queue_class()
        for operation, value in tasks:
            if operation == 'enqueue':
                queue.enqueue(value)
            else:  
                queue.dequeue()
    
    timer = timeit.Timer(process_tasks)
    times = timer.repeat(repeat=5, number=1)  
    
    avg_time = statistics.mean(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0
    avg_per_task = avg_time / len(tasks)
    
    return {
        'queue_type': queue_name,
        'total_time': avg_time,
        'std_dev': std_dev,
        'avg_time_per_task': avg_per_task,
        'tasks_processed': len(tasks)
    }


def validate_queues():
    """Verify both implementations produce same results"""
    print("Validating implementations...")
    
    random.seed(42)
    tasks = generate_tasks(20, 0.7)
    
    list_queue = ListPriorityQueue()
    list_results = []
    for op, val in tasks:
        if op == 'enqueue':
            list_queue.enqueue(val)
        else:
            list_results.append(list_queue.dequeue())
    
    random.seed(42)  
    tasks = generate_tasks(20, 0.7)
    heap_queue = HeapPriorityQueue()
    heap_results = []
    for op, val in tasks:
        if op == 'enqueue':
            heap_queue.enqueue(val)
        else:
            heap_results.append(heap_queue.dequeue())
    
    print(f"List queue dequeue results: {list_results}")
    print(f"Heap queue dequeue results: {heap_results}")
    print(f"Results match: {list_results == heap_results}\n")


def run_experiment():
    print("=" * 70)
    print("PRIORITY QUEUE PERFORMANCE COMPARISON: Linked List vs Heap")
    print("=" * 70)
    
    NUM_TASKS = 1000
    ENQUEUE_PROB = 0.7
    
    print(f"\n1. Generating {NUM_TASKS} tasks (enqueue prob={ENQUEUE_PROB})...")
    random.seed(123)  
    tasks = generate_tasks(NUM_TASKS, ENQUEUE_PROB)
    
    enqueue_count = sum(1 for op, _ in tasks if op == 'enqueue')
    dequeue_count = NUM_TASKS - enqueue_count
    print(f"   Enqueue operations: {enqueue_count}")
    print(f"   Dequeue operations: {dequeue_count}")
    
    # 2. Measure ListPriorityQueue
    print(f"\n2. MEASURING LIST PRIORITY QUEUE")
    print("-" * 50)
    list_results = measure_queue_performance(ListPriorityQueue, tasks, "Linked List")
    print(f"   Total time: {list_results['total_time']:.6f} seconds")
    print(f"   Avg time per task: {list_results['avg_time_per_task']:.8f} seconds")
    print(f"   Std deviation: {list_results['std_dev']:.6f} seconds")
    
    # 3. Measure HeapPriorityQueue
    print(f"\n3. MEASURING HEAP PRIORITY QUEUE")
    print("-" * 50)
    heap_results = measure_queue_performance(HeapPriorityQueue, tasks, "Heap")
    print(f"   Total time: {heap_results['total_time']:.6f} seconds")
    print(f"   Avg time per task: {heap_results['avg_time_per_task']:.8f} seconds")
    print(f"   Std deviation: {heap_results['std_dev']:.6f} seconds")
    
    print(f"\n4. DISCUSSION")
    print("-" * 50)
    
    if list_results['total_time'] < heap_results['total_time']:
        faster = "Linked List"
        ratio = heap_results['total_time'] / list_results['total_time']
    else:
        faster = "Heap"
        ratio = list_results['total_time'] / heap_results['total_time']
    
    print(f"\n   RESULTS: {faster} is {ratio:.2f}x faster")
    print(f"\n   WHY IS THE HEAP FASTER?")
    print(f"   - Heap enqueue: O(log n) vs List enqueue: O(n)")
    print(f"   - Heap dequeue: O(log n) vs List dequeue: O(1)")
    print(f"   - With {enqueue_count} enqueues and {dequeue_count} dequeues:")
    
    list_complexity = enqueue_count * (NUM_TASKS/2) + dequeue_count * 1
    heap_complexity = (enqueue_count + dequeue_count) * (NUM_TASKS ** 0.5)  
    
    print(f"\n   Theoretical complexity:")
    print(f"   - List: O(n) for enqueue, O(1) for dequeue")
    print(f"     Total operations ≈ {enqueue_count} × (n/2) + {dequeue_count} × 1")
    print(f"   - Heap: O(log n) for both operations")
    print(f"     Total operations ≈ {NUM_TASKS} × log₂(1000) ≈ {NUM_TASKS} × 10")
    
    print(f"\n   REAL REASONS HEAP IS FASTER:")
    print(f"   1. Better time complexity: O(log n) vs O(n) for the dominant enqueue operation")
    print(f"   2. Cache efficiency: Heap uses array (contiguous memory) vs scattered linked list nodes")
    print(f"   3. Less memory overhead: No pointers stored per element")
    print(f"   4. Constant factors: Heap operations are simple array index calculations")


def plot_comparison(list_results, heap_results):
    """Optional visualization"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        labels = ['Linked List', 'Heap']
        times = [list_results['total_time'] * 1000, heap_results['total_time'] * 1000]  
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        bars = ax1.bar(labels, times, color=['skyblue', 'lightcoral'])
        ax1.set_ylabel('Total Time (milliseconds)')
        ax1.set_title('Total Processing Time')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, time in zip(bars, times):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{time:.3f} ms', ha='center', va='bottom')
        
        per_task_times = [list_results['avg_time_per_task'] * 1e6, 
                         heap_results['avg_time_per_task'] * 1e6]  
        
        bars = ax2.bar(labels, per_task_times, color=['skyblue', 'lightcoral'])
        ax2.set_ylabel('Average Time per Task (microseconds)')
        ax2.set_title('Average Time per Operation')
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, time in zip(bars, per_task_times):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    f'{time:.2f} µs', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
    except ImportError:
        print("\nMatplotlib not installed. Skipping visualization.")


if __name__ == "__main__":
    validate_queues()
    
    list_results, heap_results = run_experiment()  
    
   