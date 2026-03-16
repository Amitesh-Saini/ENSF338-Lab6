import random
import timeit



class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None



def insert(root, key):
    temp = Node(key)

    # If tree is empty
    if root is None:
        return temp

    curr = root
    while curr is not None:
        if curr.data > key and curr.left is not None:
            curr = curr.left
        elif curr.data < key and curr.right is not None:
            curr = curr.right
        else:
            break

    if curr.data > key:
        curr.left = temp
    else:
        curr.right = temp

    return root


def search(root, key):
    curr = root
    while curr is not None:
        if key == curr.data:
            return True
        elif key < curr.data:
            curr = curr.left
        else:
            curr = curr.right
    return False


def build_tree(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


def measure_search_times(root, values, tries=10):
    total_time = 0.0

    for value in values:
        t = timeit.timeit(lambda: search(root, value), number=tries)
        total_time += t / tries   # average time for this one value

    average_time = total_time / len(values)
    return average_time, total_time


# Question 2: sorted insertion
sorted_vector = list(range(10000))
sorted_tree = build_tree(sorted_vector)

avg_sorted, total_sorted = measure_search_times(sorted_tree, sorted_vector)

print("Sorted insertion tree:")
print("Average search time per element:", avg_sorted)
print("Total search time:", total_sorted)


# Question 3: shuffled insertion
shuffled_vector = sorted_vector[:]   # copy
random.shuffle(shuffled_vector)

shuffled_tree = build_tree(shuffled_vector)

avg_shuffled, total_shuffled = measure_search_times(shuffled_tree, shuffled_vector)

print("\nShuffled insertion tree:")
print("Average search time per element:", avg_shuffled)
print("Total search time:", total_shuffled)


root = None
root = insert(root, 10)
root = insert(root, 5)
root = insert(root, 15)

print(search(root, 5))   # True
print(search(root, 20))  # False


# Question 4:

# The BST built from the sorted vector was slower because inserting sorted data into 
# a regular binary search tree produces a highly unbalanced tree. Its structure resembles 
# a linked list, so searching may require checking many nodes, giving near O(n) search time.

#The BST built from the shuffled vector was faster because random insertion 
# tends to create a more balanced tree. A more balanced BST has height closer to log n, 
# so search is much more efficient, around O(log n) on average.