# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

from typing import TypeVar
from collections import deque
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')


class Node:
    def __init__(self, key: KeyType, val: ValType, rank: int):
        self.key = key
        self.val = val
        self.rank = rank
        self.left = None
        self.right = None


class ZipTree:
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def get_random_rank() -> int:
        heads = 0
        ran = random.randint(0, 1)
        while ran != 0:
            heads += 1
            ran = random.randint(0,1)
        return heads

    def insert(self, key: KeyType, val: ValType, rank: int = -1):
        self.size += 1
        if rank == -1:
            rank = self.get_random_rank()

        node = Node(key, val, rank)

        curr = self.root
        prev = None
        fix = None

        while curr is not None and (rank < curr.rank or (rank == curr.rank and key > curr.key)):
            prev = curr
            curr = curr.left if key < curr.key else curr.right

        if curr == self.root:
            self.root = node
        elif key < prev.key:
            prev.left = node
        else:
            prev.right = node

        if curr is None:
            node.left = node.right = None
            return
        if key < curr.key:
            node.right = curr
        else:
            node.left = curr

        prev = node

        while curr is not None:
            fix = prev
            if curr.key < key:
                while curr is not None and curr.key <= key:
                    prev = curr
                    curr = curr.right
            else:
                while curr is not None and curr.key >= key:
                    prev = curr
                    curr = curr.left
            if fix.key > key or (fix == node and prev.key > key):
                fix.left = curr
            else:
                fix.right = curr

    def remove(self, key: KeyType):
        self.size -= 1
        curr = self.root
        prev = None

        while key != curr.key:
            prev = curr
            curr = curr.left if key < curr.key else curr.right

        left = curr.left
        right = curr.right

        if left is None:
            curr = right
        elif right is None:
            curr = left
        elif left.rank >= right.rank:
            curr = left
        else:
            curr = right

        if self.root.key == key:
            self.root = curr
        elif key < prev.key:
            prev.left = curr
        else:
            prev.right = curr

        while left is not None and right is not None:
            if left.rank >= right.rank:
                while left is not None and left.rank >= right.rank:
                    prev = left
                    left = left.right
                prev.right = right
            else:
                while right is not None and left.rank < right.rank:
                    prev = right
                    right = right.left
                prev.left = left

    def find(self, key: KeyType) -> ValType:
        curr = self.root
        while curr is not None and curr.key != key:
            if curr.key > key:
                curr = curr.left
            else:
                curr = curr.right
        return curr.val

    def get_size(self) -> int:
        return self.size

    def get_height(self) -> int:
        if self.root is None:
            return 0
        queue = deque()
        queue.append(self.root)
        height = 0

        while queue:
            sz = len(queue)
            changed = False
            for _ in range(sz):
                node = queue.popleft()
                if node.left:
                    changed = True
                    queue.append(node.left)
                if node.right:
                    changed = True
                    queue.append(node.right)
            if changed:
                height += 1
        return height

    def get_depth(self, key: KeyType) -> int:
        depth = 0
        curr = self.root

        while curr is not None and curr.key != key:
            if curr.key > key:
                curr = curr.left
            else:
                curr = curr.right
            depth += 1
        return depth

# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define