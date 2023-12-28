import os
import sys

import unittest

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
algoritmos_path = os.path.join(root_path, 'Algoritmos')

if root_path not in sys.path:
    sys.path.append(root_path)

if algoritmos_path not in sys.path:
    sys.path.append(algoritmos_path)

from Algoritmos import Searching
from tests.Fixtures.search_data import data

class TestSearching(unittest.TestCase):
    def test_searching_with_int_numbers(self):
        # Preparando estructura de datos
        skip_list = Searching.SkipList()
        binary_tree = Searching.BinaryTree()
        redblack_tree = Searching.RedBlackTree()

        for elem in data.enteros_sorted:
            skip_list.insert(elem)
            binary_tree.insert(elem)
            redblack_tree.insert(elem)

        self.assertEqual(data.enteros_chosed, data.enteros_sorted[Searching.LinearSearch.search(data.enteros_sorted, data.enteros_chosed)])
        self.assertEqual(data.enteros_chosed, data.enteros_sorted[Searching.BinarySearch.search(data.enteros_sorted, data.enteros_chosed)])
        self.assertEqual(data.enteros_chosed, data.enteros_sorted[Searching.JumpSearch.search(data.enteros_sorted, data.enteros_chosed)])
        self.assertEqual(data.enteros_chosed, data.enteros_sorted[Searching.ExponentialSearch.search(data.enteros_sorted, data.enteros_chosed)])
        self.assertEqual(data.enteros_chosed, data.enteros_sorted[Searching.InterpolationSearch.search(data.enteros_sorted, data.enteros_chosed)])
        self.assertEqual(data.enteros_chosed, skip_list.search(data.enteros_chosed).key)
        self.assertEqual(data.enteros_chosed, binary_tree.search(data.enteros_chosed).val)
        self.assertEqual(data.enteros_chosed, redblack_tree.search(data.enteros_chosed).data)
    
    def test_searching_with_real_numbers(self):
        # Preparando estructura de datos
        skip_list = Searching.SkipList()
        binary_tree = Searching.BinaryTree()
        redblack_tree = Searching.RedBlackTree()

        for elem in data.flotantes_sorted:
            skip_list.insert(elem)
            binary_tree.insert(elem)
            redblack_tree.insert(elem)

        self.assertEqual(data.flotantes_chosed, data.flotantes_sorted[Searching.LinearSearch.search(data.flotantes_sorted, data.flotantes_chosed)])
        self.assertEqual(data.flotantes_chosed, data.flotantes_sorted[Searching.BinarySearch.search(data.flotantes_sorted, data.flotantes_chosed)])
        self.assertEqual(data.flotantes_chosed, data.flotantes_sorted[Searching.JumpSearch.search(data.flotantes_sorted, data.flotantes_chosed)])
        self.assertEqual(data.flotantes_chosed, data.flotantes_sorted[Searching.ExponentialSearch.search(data.flotantes_sorted, data.flotantes_chosed)])
        self.assertEqual(data.flotantes_chosed, data.flotantes_sorted[Searching.InterpolationSearch.search(data.flotantes_sorted, data.flotantes_chosed)])
        self.assertEqual(data.flotantes_chosed, skip_list.search(data.flotantes_chosed).key)
        self.assertEqual(data.flotantes_chosed, binary_tree.search(data.flotantes_chosed).val)
        self.assertEqual(data.flotantes_chosed, redblack_tree.search(data.flotantes_chosed).data)

    def test_searching_with_flotantes_de_precision_numbers(self):
        # Preparando estructura de datos
        skip_list = Searching.SkipList()
        binary_tree = Searching.BinaryTree()
        redblack_tree = Searching.RedBlackTree()

        for elem in data.flotantes_de_precision_sorted:
            skip_list.insert(elem)
            binary_tree.insert(elem)
            redblack_tree.insert(elem)

        self.assertEqual(data.flotantes_de_precision_chosed, data.flotantes_de_precision_sorted[Searching.LinearSearch.search(data.flotantes_de_precision_sorted, data.flotantes_de_precision_chosed)])
        self.assertEqual(data.flotantes_de_precision_chosed, data.flotantes_de_precision_sorted[Searching.BinarySearch.search(data.flotantes_de_precision_sorted, data.flotantes_de_precision_chosed)])
        self.assertEqual(data.flotantes_de_precision_chosed, data.flotantes_de_precision_sorted[Searching.JumpSearch.search(data.flotantes_de_precision_sorted, data.flotantes_de_precision_chosed)])
        self.assertEqual(data.flotantes_de_precision_chosed, data.flotantes_de_precision_sorted[Searching.ExponentialSearch.search(data.flotantes_de_precision_sorted, data.flotantes_de_precision_chosed)])
        self.assertEqual(data.flotantes_de_precision_chosed, data.flotantes_de_precision_sorted[Searching.InterpolationSearch.search(data.flotantes_de_precision_sorted, data.flotantes_de_precision_chosed)])
        self.assertEqual(data.flotantes_de_precision_chosed, skip_list.search(data.flotantes_de_precision_chosed).key)
        self.assertEqual(data.flotantes_de_precision_chosed, binary_tree.search(data.flotantes_de_precision_chosed).val)
        self.assertEqual(data.flotantes_de_precision_chosed, redblack_tree.search(data.flotantes_de_precision_chosed).data)
    
    def test_searching_with_int_numbers_fail(self):
        # Preparando estructura de datos
        skip_list = Searching.SkipList()
        binary_tree = Searching.BinaryTree()
        redblack_tree = Searching.RedBlackTree()

        for elem in data.enteros_sorted:
            skip_list.insert(elem)
            binary_tree.insert(elem)
            redblack_tree.insert(elem)

        self.assertEqual(-1, Searching.LinearSearch.search(data.enteros_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.BinarySearch.search(data.enteros_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.JumpSearch.search(data.enteros_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.ExponentialSearch.search(data.enteros_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.InterpolationSearch.search(data.enteros_sorted, data.no_chosed))
        self.assertEqual(-1, skip_list.search(data.no_chosed))
        self.assertEqual(-1, binary_tree.search(data.no_chosed))
        self.assertEqual(-1, redblack_tree.search(data.no_chosed))
    
    def test_searching_with_real_numbers_fail(self):
        # Preparando estructura de datos
        skip_list = Searching.SkipList()
        binary_tree = Searching.BinaryTree()
        redblack_tree = Searching.RedBlackTree()

        for elem in data.flotantes_sorted:
            skip_list.insert(elem)
            binary_tree.insert(elem)
            redblack_tree.insert(elem)

        self.assertEqual(-1, Searching.LinearSearch.search(data.flotantes_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.BinarySearch.search(data.flotantes_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.JumpSearch.search(data.flotantes_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.ExponentialSearch.search(data.flotantes_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.InterpolationSearch.search(data.flotantes_sorted, data.no_chosed))
        self.assertEqual(-1, skip_list.search(data.no_chosed))
        self.assertEqual(-1, binary_tree.search(data.no_chosed))
        self.assertEqual(-1, redblack_tree.search(data.no_chosed))

    def test_searching_with_flotantes_de_precision_numbers_fail(self):
        # Preparando estructura de datos
        skip_list = Searching.SkipList()
        binary_tree = Searching.BinaryTree()
        redblack_tree = Searching.RedBlackTree()

        for elem in data.flotantes_de_precision_sorted:
            skip_list.insert(elem)
            binary_tree.insert(elem)
            redblack_tree.insert(elem)

        self.assertEqual(-1, Searching.LinearSearch.search(data.flotantes_de_precision_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.BinarySearch.search(data.flotantes_de_precision_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.JumpSearch.search(data.flotantes_de_precision_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.ExponentialSearch.search(data.flotantes_de_precision_sorted, data.no_chosed))
        self.assertEqual(-1, Searching.InterpolationSearch.search(data.flotantes_de_precision_sorted, data.no_chosed))
        self.assertEqual(-1, skip_list.search(data.no_chosed))
        self.assertEqual(-1, binary_tree.search(data.no_chosed))
        self.assertEqual(-1, redblack_tree.search(data.no_chosed))
    

if __name__ == '__main__':
    unittest.main()