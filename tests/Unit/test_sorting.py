import os
import sys

import unittest

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
algoritmos_path = os.path.join(root_path, 'Algoritmos')

if root_path not in sys.path:
    sys.path.append(root_path)

if algoritmos_path not in sys.path:
    sys.path.append(algoritmos_path)

from Algoritmos import Sorting
from tests.Fixtures.sorting_data import data

class TestSorting(unittest.TestCase):
    def test_sorting_with_int_numbers(self):
        self.assertEqual(data.enteros_sorted, Sorting.BubbleSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.QuickSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.MergeSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.HeapSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.InsertionSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.SelectionSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.BucketSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.RadixSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.CountingSort.sort(data.enteros_unsorted))
        self.assertEqual(data.enteros_sorted, Sorting.TimSort.sort(data.enteros_unsorted))

    def test_sorting_with_real_numbers(self):
        self.assertEqual(data.flotantes_sorted, Sorting.BubbleSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.QuickSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.MergeSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.HeapSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.InsertionSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.SelectionSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.BucketSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.RadixSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.CountingSort.sort(data.flotantes_unsorted))
        self.assertEqual(data.flotantes_sorted, Sorting.TimSort.sort(data.flotantes_unsorted))

    def test_sorting_with_float_presition(self):
        counting_sort_limt_float_mem_error = [round(d, 3) for d in data.flotantes_de_precision_sorted]
        
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.BubbleSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.QuickSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.MergeSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.HeapSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.InsertionSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.SelectionSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.BucketSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.RadixSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(counting_sort_limt_float_mem_error, Sorting.CountingSort.sort(data.flotantes_de_precision_unsorted))
        self.assertEqual(data.flotantes_de_precision_sorted, Sorting.TimSort.sort(data.flotantes_de_precision_unsorted))