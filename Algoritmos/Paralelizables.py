import threading
import math

import concurrent.futures
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

class ParallelRadixSort:
    @staticmethod
    @performance_logger()
    def sort(data):
        def counting_sort(arr, exp1):
            n = len(arr)
            output = [0] * n
            count = [0] * 10

            for i in range(0, n):
                index = int(arr[i] / exp1)
                count[(index % 10)] += 1

            for i in range(1, 10):
                count[i] += count[i - 1]

            i = n - 1
            while i >= 0:
                index = int(arr[i] / exp1)
                output[count[(index % 10)] - 1] = arr[i]
                count[(index % 10)] -= 1
                i -= 1

            for i in range(0, len(arr)):
                arr[i] = output[i]
        def radix_sort(arr):
            if not arr:
                return
            max1 = max(arr)
            exp = 1
            while max1 / exp > 1:
                counting_sort(arr, exp)
                exp *= 10

        # Separar los números negativos y positivos
        neg = [-x for x in data if x < 0]
        non_neg = [x for x in data if x >= 0]

        # Aplicar Radix Sort a cada subconjunto en paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(radix_sort, subset) for subset in [neg, non_neg]]
            concurrent.futures.wait(futures)

        # Unir los resultados y ajustar los números negativos
        return [-x for x in reversed(neg)] + non_neg

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

class ParallelCountingSort:
    @staticmethod
    @performance_logger()
    def sort(data):
        # Escalamos los números para reducir el rango
        scale_factor = 10**3
        scaled_data = [int(x * scale_factor) for x in data]

        # Separamos los números negativos y no negativos
        negative_nums = [-x for x in scaled_data if x < 0]
        non_negative_nums = [x for x in scaled_data if x >= 0]

        # Paralelizamos la ordenación de los subconjuntos
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                'negatives': executor.submit(ParallelCountingSort._optimized_counting_sort, negative_nums),
                'non_negatives': executor.submit(ParallelCountingSort._optimized_counting_sort, non_negative_nums)
            }
            sorted_negatives = futures['negatives'].result()
            sorted_non_negatives = futures['non_negatives'].result()

        # Combinamos y desescalamos
        combined = [-x for x in reversed(sorted_negatives)] + sorted_non_negatives
        return [x / scale_factor for x in combined]

    @staticmethod
    def _optimized_counting_sort(data):
        if not data:
            return data

        # Usamos un diccionario para el conteo en lugar de una lista
        count = {}
        for number in data:
            count[number] = count.get(number, 0) + 1

        sorted_data = []
        for number in range(min(count), max(count) + 1):
            sorted_data.extend([number] * count.get(number, 0))

        return sorted_data

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

class ParallelExponentialSearch:
    @staticmethod
    @performance_logger()
    def search(arr, target):
        if not arr:
            return -1

        if arr[0] == target:
            return 0

        # Determinar los segmentos para la búsqueda binaria
        n = len(arr)
        segments = []
        i = 1
        while i < n:
            left = i // 2
            right = min(i, n - 1)
            segments.append((left, right))
            i *= 2

        # Ejecutar la búsqueda binaria en paralelo en cada segmento
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ParallelExponentialSearch._binary_search, arr, target, left, right) for left, right in segments]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result != -1:
                    return result
        return -1

    @staticmethod
    def _binary_search(arr, target, left, right):
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return -1

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