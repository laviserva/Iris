import unittest
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
algoritmos_path = os.path.join(root_path, 'Algoritmos')

if root_path not in sys.path:
    sys.path.append(root_path)

if algoritmos_path not in sys.path:
    sys.path.append(algoritmos_path)

from Algoritmos import Paralelizables, Sorting, Searching
from tests.Fixtures.sorting_data import data as sorting_data
from tests.Fixtures.search_data import data as search_data

from Algoritmos.run_algorithms import run_algorithms
from tests.manage_files import handle_exception

class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        self.sorting_data = sorting_data
        self.search_data = search_data

        self.sort_algorithms = ['BubbleSort', 'QuickSort', 'MergeSort', 'HeapSort', 'InsertionSort',
                                'SelectionSort', 'BucketSort', 'RadixSort', 'CountingSort', 'TimSort']
        
        self.search_algorithms = ['LinearSearch', 'BinarySearch', 'JumpSearch', 'ExponentialSearch',
                                  'InterpolationSearch', 'SkipList', 'BinaryTree', 'RedBlackTree']
        
        self.parallel_algorithms = ['ParallelQuickSort', 'ParallelMergeSort', 'ParallelBucketSort',
                                    'ParallelRadixSort', 'ParallelCountingSort', 'ParallelTimSort',
                                    'ParallelExponentialSearch', 'ParallelInterpolationSearch']
    
    @handle_exception()
    def test_sort_algorithms(self):
        if self.sort_algorithms:
            run_algorithms(self.sorting_data.enteros_unsorted, self.sort_algorithms, Sorting)
            run_algorithms(self.sorting_data.flotantes_unsorted, self.sort_algorithms, Sorting)
            run_algorithms(self.sorting_data.flotantes_de_precision_unsorted, self.sort_algorithms, Sorting)

    @handle_exception()
    def test_search_algorithms(self):
        if self.search_algorithms:
            run_algorithms(self.search_data.enteros_sorted, self.search_algorithms, Searching)
            run_algorithms(self.search_data.flotantes_sorted, self.search_algorithms, Searching)
            run_algorithms(self.search_data.flotantes_de_precision_sorted, self.search_algorithms, Searching)

    @handle_exception()
    def test_parallel_algorithms(self):
        if self.parallel_algorithms:
            sort_aux = [alg for alg in self.parallel_algorithms if "Sort" in alg]
            search_aux = [alg for alg in self.parallel_algorithms if "Search" in alg]
            
            if sort_aux:
                run_algorithms(self.sorting_data.enteros_unsorted, sort_aux, Paralelizables)
                run_algorithms(self.sorting_data.flotantes_unsorted, sort_aux, Paralelizables)
                run_algorithms(self.sorting_data.flotantes_de_precision_unsorted, sort_aux, Paralelizables)
            if search_aux:
                run_algorithms(self.sorting_data.enteros_sorted, search_aux, Paralelizables)
                run_algorithms(self.sorting_data.flotantes_sorted, search_aux, Paralelizables)
                run_algorithms(self.sorting_data.flotantes_de_precision_sorted, search_aux, Paralelizables)

if __name__ == '__main__':
    unittest.main()