import math
import random

from performanzer import performance_logger

class LinearSearch:
    @staticmethod
    @performance_logger()
    def search(arr, target):
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return -1

class BinarySearch:
    @staticmethod
    @performance_logger()
    def search(arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

class JumpSearch:
    @staticmethod
    @performance_logger()
    def search(arr, target):
        n = len(arr)
        step = math.sqrt(n)

        prev = 0
        while arr[int(min(step, n) - 1)] < target:
            prev = step
            step += math.sqrt(n)
            if prev >= n:
                return -1

        while arr[int(prev)] < target:
            prev += 1
            if prev == min(step, n):
                return -1

        if arr[int(prev)] == target:
            return int(prev)

        return -1

class ExponentialSearch:
    """Realiza una búsqueda exponencial en un arreglo ordenado mediante binary search"""
    @staticmethod
    @performance_logger()
    def search(arr, target):
        if not arr:
            return -1

        if arr[0] == target:
            return 0

        i = 1
        n = len(arr)
        while i < n and arr[i] <= target:
            i *= 2

        left = i // 2
        right = min(i, n - 1)

        # La búsqueda binaria se maneja igual para números reales
        return ExponentialSearch._binary_search(arr, target, left, right)

    def _binary_search(arr, target, left, right):
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                right = mid - 1
            else:
                left = mid + 1

        return -1  # Retorna -1 si el número no se encuentra

class InterpolationSearch:
    @staticmethod
    @performance_logger()
    def search(arr, target):
        low = 0
        high = len(arr) - 1

        while low <= high and target >= arr[low] and target <= arr[high]:
            if low == high:
                if arr[low] == target:
                    return low
                return -1

            pos = low + int(((float(high - low) / (arr[high] - arr[low])) * (target - arr[low])))

            if arr[pos] == target:
                return pos

            if arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1

        return -1

### Skip list
class Node_SkipList:
    """Clase para representar un nodo en la Skip List"""
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    """Clase para representar la Skip List"""
    def __init__(self, max_level=3, p=0.5):
        self.MAX_LEVEL = max_level
        self.p = p
        self.header = self.create_node(self.MAX_LEVEL, -1)
        self.level = 0

    def create_node(self, lvl, key):
        return Node_SkipList(key, lvl)

    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:
            rlevel = self.random_level()

            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            n = self.create_node(rlevel, key)

            for i in range(rlevel + 1):
                n.forward[i] = update[i].forward[i]
                update[i].forward[i] = n

    @performance_logger()
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]

        if current and current.key == key:
            return current
        return -1

class Node_BS:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node_BS(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = Node_BS(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = Node_BS(key)
            else:
                self._insert_recursive(node.right, key)

    @performance_logger()
    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if not node:
            return -1
        if node.val == key:
            return node
        if key < node.val:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

class Node_RB:
    def __init__(self, data, color="RED"):
        self.data = data
        self.color = color
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node_RB(0)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL

    def insert(self, key):
        node = Node_RB(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "RED"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = "BLACK"
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    @performance_logger()
    def search(self, k):
        return self._search_helper(self.root, k)

    def _search_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node if node != self.TNULL else -1

        if key < node.data:
            return self._search_helper(node.left, key)
        return self._search_helper(node.right, key)
    
    def delete_node(self, data):
        self._delete_node_helper(self.root, data)

    def _delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("No se puede encontrar la llave en el árbol")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def _fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.root = RedBlackTree.left_rotate(self.root, x.parent, self.TNULL)
                    s = x.parent.right

                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.right.color == "BLACK":
                        s.left.color = "BLACK"
                        s.color = "RED"
                        self.root = RedBlackTree.right_rotate(self.root, s, self.TNULL)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.right.color = "BLACK"
                    self.root = RedBlackTree.left_rotate(self.root, x.parent, self.TNULL)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.root = RedBlackTree.right_rotate(self.root, x.parent, self.TNULL)
                    s = x.parent.left

                if s.right.color == "BLACK" and s.left.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.left.color == "BLACK":
                        s.right.color = "BLACK"
                        s.color = "RED"
                        self.root = RedBlackTree.left_rotate(self.root, s, self.TNULL)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.left.color = "BLACK"
                    self.root = RedBlackTree.right_rotate(self.root, x.parent, self.TNULL)
                    x = self.root

        x.color = "BLACK"
