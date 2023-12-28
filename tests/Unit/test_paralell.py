import unittest
import os
import sys

# Asegurando que los módulos del proyecto están accesibles
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
algoritmos_path = os.path.join(root_path, 'Algoritmos')

if root_path not in sys.path:
    sys.path.append(root_path)

if algoritmos_path not in sys.path:
    sys.path.append(algoritmos_path)

from Algoritmos import Paralelizables
from tests.Fixtures.sorting_data import data as sorting_data
from tests.Fixtures.search_data import data as search_data

class TestParalelizables(unittest.TestCase):

    def test_sort_with_multiple_algorithms(self):
        algorithms = [
            Paralelizables.ParallelQuickSort,
            Paralelizables.ParallelMergeSort,
            Paralelizables.ParallelBucketSort,
            Paralelizables.ParallelRadixSort,
            Paralelizables.ParallelCountingSort,
            Paralelizables.ParallelTimSort
        ]

        for algo in algorithms:
            with self.subTest(algorithm=algo.__name__):
                self.assertEqual(
                    sorting_data.enteros_sorted,
                    algo.sort(sorting_data.enteros_unsorted.copy())
                )

                self.assertEqual(
                    sorting_data.flotantes_sorted,
                    algo.sort(sorting_data.flotantes_unsorted.copy())
                )

                # Ajustar la precisión para el Counting Sort si es necesario
                if algo == Paralelizables.ParallelCountingSort:
                    sorted_data = [round(num, 3) for num in algo.sort(sorting_data.flotantes_de_precision_unsorted.copy())]
                    expected_data = [round(num, 3) for num in sorting_data.flotantes_de_precision_sorted]
                    self.assertEqual(expected_data, sorted_data)
                else:
                    self.assertEqual(
                        sorting_data.flotantes_de_precision_sorted,
                        algo.sort(sorting_data.flotantes_de_precision_unsorted.copy())
                    )

    def test_search_with_multiple_algorithms(self):
        algorithms = [
            Paralelizables.ParallelExponentialSearch,
            Paralelizables.ParallelInterpolationSearch
        ]

        for algo in algorithms:
            with self.subTest(algorithm=algo.__name__):
                index = algo.search(search_data.enteros_sorted, search_data.enteros_chosed)
                self.assertEqual(search_data.enteros_sorted[index], search_data.enteros_chosed)

                index = algo.search(search_data.flotantes_sorted, search_data.flotantes_chosed)
                self.assertEqual(search_data.flotantes_sorted[index], search_data.flotantes_chosed)

                index = algo.search(search_data.flotantes_de_precision_sorted, search_data.flotantes_de_precision_chosed)
                self.assertEqual(search_data.flotantes_de_precision_sorted[index], search_data.flotantes_de_precision_chosed)

                self.assertEqual(-1, algo.search(search_data.enteros_sorted, search_data.no_chosed))
                self.assertEqual(-1, algo.search(search_data.flotantes_sorted, search_data.no_chosed))
                self.assertEqual(-1, algo.search(search_data.flotantes_de_precision_sorted, search_data.no_chosed))

if __name__ == '__main__':
    unittest.main()
