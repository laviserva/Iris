import threading
import math

from performanzer import performance_logger

class ParallelQuickSort:
    @performance_logger()
    @staticmethod
    def sort(arr):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            less = [x for x in arr[1:] if x <= pivot]
            greater = [x for x in arr[1:] if x > pivot]

            # Ordenar en paralelo
            threads = []
            sorted_sublists = [None, None]

            for i, sublist in enumerate([less, greater]):
                thread = threading.Thread(target=lambda idx, data: sorted_sublists.__setitem__(idx, ParallelQuickSort.sort(data)), args=(i, sublist))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            return sorted_sublists[0] + [pivot] + sorted_sublists[1]

"""# Uso del algoritmo
arr = [12, 11, 13, 5, 6, 7]
sorted_arr = ParallelQuickSort.sort(arr)
print("Sorted array is:", sorted_arr)
"""

class ParallelMergeSort:
    @staticmethod
    @performance_logger()
    def sort(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            # Crear threads para ordenar las mitades
            left_thread = threading.Thread(target=lambda: ParallelMergeSort.sort(left_half))
            right_thread = threading.Thread(target=lambda: ParallelMergeSort.sort(right_half))

            left_thread.start()
            right_thread.start()

            left_thread.join()
            right_thread.join()

            # Merge
            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1

        return arr

"""# Ejemplo de uso
arr = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = ParallelMergeSort.sort(arr)
print("Sorted array is:", sorted_arr)
"""

class ParallelBucketSort:
    @staticmethod
    @performance_logger()
    def sort(arr, bucket_size=5):
        if len(arr) == 0:
            return arr

        # Determinar mínimo y máximo
        min_value, max_value = min(arr), max(arr)

        # Inicializar buckets
        bucket_count = math.ceil((max_value - min_value) / bucket_size)
        buckets = [[] for _ in range(bucket_count)]

        # Distribuir elementos en buckets
        for i in range(len(arr)):
            index = math.floor((arr[i] - min_value) / bucket_size)
            buckets[index].append(arr[i])

        # Ordenar los buckets y concatenar
        sorted_arr = []
        threads = []
        for bucket in buckets:
            thread = threading.Thread(target=lambda b=bucket: b.sort())
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        for bucket in buckets:
            sorted_arr.extend(bucket)

        return sorted_arr

"""# Ejemplo de uso
arr = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
sorted_arr = ParallelBucketSort.sort(arr)
print("Sorted array is:", sorted_arr)
"""

class ParallelRadixSort:
    @staticmethod
    @performance_logger()
    def sort(arr, decimal_places=3):
        factor = 10 ** decimal_places
        scaled_arr = [int(x * factor) for x in arr]

        negative_nums = [-x for x in scaled_arr if x < 0]
        non_negative_nums = [x for x in scaled_arr if x >= 0]

        sorted_negatives = []
        sorted_non_negatives = []

        def sort_negatives():
            nonlocal sorted_negatives
            sorted_negatives = ParallelRadixSort._radix_sort(negative_nums)

        def sort_non_negatives():
            nonlocal sorted_non_negatives
            sorted_non_negatives = ParallelRadixSort._radix_sort(non_negative_nums)

        thread1 = threading.Thread(target=sort_negatives)
        thread2 = threading.Thread(target=sort_non_negatives)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        sorted_arr = [-x for x in reversed(sorted_negatives)] + sorted_non_negatives
        return [x / factor for x in sorted_arr]

    @staticmethod
    def _radix_sort(arr):
        if len(arr) == 0:
            return arr

        max_num = max(arr)
        max_digits = int(math.log10(max_num)) + 1 if max_num > 0 else 1

        for digit in range(max_digits):
            arr = ParallelRadixSort._counting_sort_for_digit(arr, digit)

        return arr

    @staticmethod
    def _counting_sort_for_digit(arr, digit):
        sorted_arr = [0] * len(arr)
        count = [0] * 10

        for num in arr:
            index = (num // 10 ** digit) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = len(arr) - 1
        while i >= 0:
            index = (arr[i] // 10 ** digit) % 10
            sorted_arr[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1

        return sorted_arr

"""# Ejemplo de uso
arr = [0.897, -0.565, 0.656, -0.1234, 0.665, -0.3434]
sorted_arr = ParallelRadixSort.sort(arr)
print("Sorted array is:", sorted_arr)
"""

class ParallelCountingSort:
    @staticmethod
    @performance_logger()
    def sort(arr, decimal_places=3):
        if len(arr) == 0:
            return arr

        # Escalar los números para manejar números flotantes
        factor = 10 ** decimal_places
        scaled_arr = [int(x * factor) for x in arr]

        # Encontrar el valor mínimo y máximo
        min_val = min(scaled_arr)
        max_val = max(scaled_arr)

        # Crear el arreglo de conteo
        count_arr_length = max_val - min_val + 1
        count_arr = [0] * count_arr_length

        # Dividir el arreglo y contar en paralelo
        def count_elements(start, end):
            for i in range(start, end):
                count_arr[scaled_arr[i] - min_val] += 1

        mid = len(scaled_arr) // 2
        thread1 = threading.Thread(target=count_elements, args=(0, mid))
        thread2 = threading.Thread(target=count_elements, args=(mid, len(scaled_arr)))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Reconstruir el arreglo ordenado
        sorted_arr = []
        for i, count in enumerate(count_arr):
            sorted_arr.extend([min_val + i] * count)

        # Escalar hacia atrás y devolver
        return [x / factor for x in sorted_arr]

"""# Ejemplo de uso
arr = [0.897, -0.565, 0.656, -0.1234, 0.665, -0.3434]
sorted_arr = ParallelCountingSort.sort(arr)
print("Sorted array is:", sorted_arr)
"""

class ParallelTimSort:
    @staticmethod
    @performance_logger()
    def sort(arr):
        if len(arr) <= 1:
            return arr

        # Dividir el arreglo en dos segmentos
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        # Ordenar en paralelo
        threads = []
        for segment in [left, right]:
            thread = threading.Thread(target=lambda l=segment: l.sort())
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Fusionar los segmentos ordenados
        return ParallelTimSort._merge(left, right)

    @staticmethod
    def _merge(left, right):
        # Función de fusión para Merge Sort
        result = []
        while left and right:
            if left[0] < right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left)
        result.extend(right)
        return result

"""# Ejemplo de uso
arr = [12, 11, 13, 5, 6, -7.1]
sorted_arr = ParallelTimSort.sort(arr)
print("Sorted array is:", sorted_arr)
"""

class ParallelExponentialSearch:
    @staticmethod
    @performance_logger()
    def search(arr, target):
        if arr[0] == target:
            return 0

        # Encontrar rango para la búsqueda binaria
        i = 1
        while i < len(arr) and arr[i] <= target:
            i = i * 2

        # Llamar a la búsqueda binaria para el rango encontrado
        return ParallelExponentialSearch._binary_search(arr, target, i // 2, min(i, len(arr)))

    @staticmethod
    def _binary_search(arr, target, left, right):
        if right < left:
            return -1

        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

"""# Ejemplo de uso
arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 5
index = ParallelExponentialSearch.search(arr, target)
print(f"Element found at index: {index}")"""


class ParallelInterpolationSearch:
    @staticmethod
    @performance_logger()
    def search(arr, target):
        return ParallelInterpolationSearch._parallel_search(arr, 0, len(arr) - 1, target)

    @staticmethod
    def _parallel_search(arr, low, high, target):
        if low <= high and target >= arr[low] and target <= arr[high]:
            # Interpolación para encontrar la posición predicha
            pos = low + int(((float(high - low) / (arr[high] - arr[low])) * (target - arr[low])))

            if arr[pos] == target:
                return pos

            if arr[pos] < target:
                return ParallelInterpolationSearch._parallel_search(arr, pos + 1, high, target)
            else:
                return ParallelInterpolationSearch._parallel_search(arr, low, pos - 1, target)

        return -1

"""# Ejemplo de uso
arr = [10, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 33, 35, 42, 47]
target = 18
index = ParallelInterpolationSearch.search(arr, target)
print(f"Element found at index: {index}")
"""