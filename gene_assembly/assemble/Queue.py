__author__ = 'Nhuy'

from assemble.longest_common_substring import *

"""
Priority Queue used to store the edges in order of edge weights

Uses a heap:
# root of heap = array[1]
# left child is array[2]
# right child is array[3]
# in array[k] left child is array[k*2], right child is array[k*2+1], parent is array[k/2]
"""

class Priority_Queue:

    """
    Constructor: initializes heap, which is an array of edge objects
    """
    def __init__(self):
        self.heap = [None]
        self.size = 0

    """
    Size functions
    Returns: size of the queue
    """
    def is_empty(self):
        return self.size == 0

    """
    Insertion methods
    Parameters: 2 strings, the from string and the to string

    Given 2 strings, finds the longest common substring (lcs). Makes an edge object and adds it to queue
    iff the length of the lcs > 0 (at least 1 character overlaps) and there is a logical from and to node.
    After addition, the queue is adjusted to ensure that added object is positioned accordingly to its edge weight.
    """
    def enqueue(self, str1, str2):
        # finds the lcs, generates an  if it exists
        data = longest_common_substring(str1, str2)

        if data is None:
            return None

        # initialize the queue
        if self.is_empty():
            self.heap.append(data)
            self.size += 1

        # adds to the queue and repositions new object to position by comparing it to its parent
        else:
            self.heap.append(data)
            self.size += 1
            current_position = self.size

            while current_position > 1 and data > self.heap[current_position/2]:
                self.heap[current_position] = self.heap[current_position/2]
                current_position /= 2

            self.heap[current_position] = data

    """
    Removal methods
    Returns: the edge object with the greatest weight

    Uses recursion to find the edge object with the greatest weight and rearrange the queue according to weight
    """
    def dequeue(self):

        # throw and exception if the queue is empty
        if self.is_empty():
            raise Exception("the queue is empty")

        # return the last object if queue is of size 1
        if self.size == 1:
            self.size -= 1
            return self.heap.pop()

        # removes the edge object with the greatest weight and replaces it with the smallest child
        max = self.heap[1]
        self.heap[1] = self.heap.pop()
        self.size -= 1

        # recursively reorganizes the queue
        self.heap[1] = self.__aux_dequeue(1, self.heap[1])

        # return the max object
        return max

    # Recursive method to organize tree after removal of max object
    # Parameters: int for current location to be filled (index), int value in current position (value)
    # Returns: the object that should be placed in the position under consideration when function called
    def __aux_dequeue(self, index, value):

        # saves the position of the right and left child
        left_pos = index * 2
        right_pos = index * 2 + 1

        # if the current position has no children, it is in the smallest location and there is no smaller object
        if left_pos > self.size:
            return value

        # if the current position has 1 child, compare it to its child;
        # swap positions if it is smaller than its child
        # return its value if it is bigger than its child (don't swap)
        elif left_pos == self.size:
            if self.heap[left_pos] < value:
                return value
            else:
                temp = self.heap[left_pos]
                self.heap[left_pos] = value
                return temp

        # if the current position has 2 children, compare it to both children
        # swap positions with its biggest child if it is smaller than either child
        # return its value if it is bigger than both children (don't swap)
        else:
            if self.heap[left_pos] < value and self.heap[right_pos] < value:
                return value
            else:
                if self.heap[left_pos] > self.heap[right_pos]:
                    temp = self.heap[left_pos]
                    self.heap[left_pos] = self.__aux_dequeue(left_pos, value)
                else:
                    temp = self.heap[right_pos]
                    self.heap[right_pos] = self.__aux_dequeue(right_pos, value)
                return temp

