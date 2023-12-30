import threading
import math

import concurrent.futures
from typing import List
from performanzer import performance_logger

class ParallelQuickSort:
    """
    Ordena una lista utilizando el algoritmo QuickSort en paralelo.

    Complejidad:
    - Tiempo promedio: O(n log n), donde n es el número de elementos.
    - Espacio: O(n), debido a las listas adicionales 'less' y 'greater'.

    Funcionamiento:
    - Divide la lista en dos sublistas basadas en un pivote.
    - Ordena las sublistas en paralelo utilizando hilos.
    - Combina las sublistas ordenadas y el pivote.

    Paralelización:
    - Utiliza 2 hilos en cada nivel de la recursión.
    - El número de hilos activos en promedio depende de la profundidad de la recursión.
    """
    @performance_logger()
    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        """
        Args:
            arr (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada de enteros.
        """
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
    """
    Ordena una lista utilizando el algoritmo MergeSort en paralelo.

    Complejidad:
    - Tiempo promedio: O(n log n), donde n es el número de elementos.
    - Espacio: O(n), debido a las sublistas adicionales creadas durante la división.

    Funcionamiento:
    - Divide la lista en dos mitades.
    - Ordena cada mitad en paralelo utilizando hilos.
    - Combina las dos mitades ordenadas en una lista final ordenada.

    Paralelización:
    - Utiliza 2 hilos en cada nivel de la división para ordenar las mitades.
    - El número de hilos activos depende de la profundidad de la división.
    """

    @staticmethod
    @performance_logger()
    def sort(arr: List[int]) -> List[int]:
        """
        Ordena una lista de enteros utilizando el algoritmo MergeSort en paralelo.

        Args:
            arr (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada de enteros.
        """
        if len(arr) > 1:
            # Dividir la lista en dos mitades
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            # Crear hilos para ordenar las mitades en paralelo
            left_thread = threading.Thread(target=lambda: ParallelMergeSort.sort(left_half))
            right_thread = threading.Thread(target=lambda: ParallelMergeSort.sort(right_half))

            left_thread.start()
            right_thread.start()

            # Esperar a que los hilos terminen
            left_thread.join()
            right_thread.join()

            # Combinar las mitades ordenadas
            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            # Combinar los elementos restantes
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
    """
    Ordena una lista utilizando el algoritmo Bucket Sort en paralelo.

    Complejidad:
    - Tiempo promedio: O(n + k), donde n es el número de elementos y k el número de buckets.
    - Espacio: O(n * k), debido a la creación de listas adicionales para los buckets.

    Funcionamiento:
    - Divide los elementos en diferentes 'buckets' basándose en un rango.
    - Ordena cada bucket en paralelo utilizando hilos.
    - Combina los buckets ordenados en una lista final ordenada.

    Paralelización:
    - Crea un hilo por cada bucket para realizar el ordenamiento.
    - El número de hilos es igual al número de buckets creados.
    """

    @staticmethod
    @performance_logger()
    def sort(arr: List[int], bucket_size: int = 5) -> List[int]:
        """
        Ordena una lista de enteros utilizando el algoritmo Bucket Sort en paralelo.

        Args:
            arr (List[int]): Lista de enteros a ordenar.
            bucket_size (int): Tamaño de cada bucket.

        Returns:
            List[int]: Lista ordenada de enteros.
        """
        if len(arr) == 0:
            return arr

        # Determinar los valores mínimo y máximo de la lista
        min_value, max_value = min(arr), max(arr)

        # Inicializar los buckets
        bucket_count = math.ceil((max_value - min_value) / bucket_size)
        buckets = [[] for _ in range(bucket_count)]

        # Distribuir los elementos en los buckets
        for i in range(len(arr)):
            index = math.floor((arr[i] - min_value) / bucket_size)
            buckets[index].append(arr[i])

        # Ordenar los buckets en paralelo y concatenar
        sorted_arr = []
        threads = []
        for bucket in buckets:
            thread = threading.Thread(target=lambda b=bucket: b.sort())
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        # Concatenar los buckets ordenados
        for bucket in buckets:
            sorted_arr.extend(bucket)

        return sorted_arr


class ParallelRadixSort:
    """
    Ordena una lista utilizando el algoritmo Radix Sort en paralelo.

    Complejidad:
    - Tiempo promedio: O(d*(n+b)), donde n es el número de elementos, d es el número de dígitos y b es la base (en este caso, 10).
    - Espacio: O(n + b), debido a la creación de listas adicionales para el conteo y la salida.

    Funcionamiento:
    - Divide los elementos en números negativos y no negativos.
    - Aplica Radix Sort a cada subconjunto en paralelo.
    - Combina los resultados para obtener la lista ordenada final.

    Paralelización:
    - Utiliza hilos para ordenar en paralelo los números negativos y no negativos.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista de enteros utilizando el algoritmo Radix Sort en paralelo.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada de enteros.
        """

        # Función interna para ordenar basado en un dígito específico
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
        # Funcion interna para realizar el Radix Sort
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

class ParallelCountingSort:
    """
    Ordena una lista utilizando el algoritmo Counting Sort en paralelo.

    Complejidad:
    - Tiempo promedio: O(n + k), donde n es el número de elementos y k es el rango de los valores.
    - Espacio: O(n + k), debido a la creación de estructuras adicionales para el conteo y la salida.

    Funcionamiento:
    - Escala los números para reducir el rango.
    - Divide los elementos en números negativos y no negativos.
    - Aplica Counting Sort a cada subconjunto en paralelo.
    - Combina los resultados y los desescala para obtener la lista ordenada final.

    Paralelización:
    - Utiliza hilos para ordenar en paralelo los números negativos y no negativos.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[float]) -> List[float]:
        """
        Ordena una lista de números flotantes utilizando el algoritmo Counting Sort en paralelo.

        Args:
            data (List[float]): Lista de números flotantes a ordenar.

        Returns:
            List[float]: Lista ordenada de números flotantes.
        """
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
    def _optimized_counting_sort(data: List[int]) -> List[int]:
        """
        Método de ayuda para realizar un Counting Sort optimizado.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada de enteros.
        """
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
    """
    Ordena una lista utilizando el algoritmo TimSort en paralelo.

    Complejidad:
    - Tiempo promedio: O(n log n), donde n es el número de elementos.
    - Espacio: O(n), ya que TimSort requiere espacio adicional para la fusión de segmentos.

    Funcionamiento:
    - Divide la lista en dos segmentos.
    - Ordena cada segmento en paralelo.
    - Fusiona los segmentos ordenados para obtener la lista ordenada final.

    Paralelización:
    - Utiliza hilos para ordenar en paralelo los dos segmentos de la lista.
    """
    @staticmethod
    @performance_logger()
    def sort(arr):
        """
        Ordena una lista de enteros utilizando el algoritmo TimSort en paralelo.

        Args:
            arr (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada de enteros.
        """
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
        """
        Método auxiliar para fusionar dos segmentos ordenados.

        Args:
            left (List[int]): Segmento izquierdo ordenado.
            right (List[int]): Segmento derecho ordenado.

        Returns:
            List[int]: Lista resultante de la fusión de los segmentos.
        """
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
    """
    Realiza una búsqueda exponencial en paralelo en una lista ordenada.

    Complejidad:
    - Tiempo promedio: O(log n), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que la búsqueda no requiere espacio adicional significativo.

    Funcionamiento:
    - Encuentra rangos de índices donde el valor objetivo podría estar mediante búsqueda exponencial.
    - Realiza una búsqueda binaria en paralelo en cada uno de estos rangos.

    Paralelización:
    - Utiliza múltiples hilos para realizar búsquedas binarias en diferentes segmentos de la lista simultáneamente.
    """
    @staticmethod
    @performance_logger()
    def search(arr, target):
        """
        Busca un elemento en una lista ordenada utilizando la búsqueda exponencial en paralelo.

        Args:
            arr (List[int]): Lista ordenada de enteros donde buscar.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: Índice del elemento objetivo en la lista, o -1 si no se encuentra.
        """
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
        """
        Realiza una búsqueda binaria en un segmento de la lista.

        Args:
            arr (List[int]): Lista ordenada de enteros.
            target (int): Elemento objetivo a buscar.
            left (int): Índice izquierdo del segmento.
            right (int): Índice derecho del segmento.

        Returns:
            int: Índice del elemento objetivo en el segmento, o -1 si no se encuentra.
        """
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
    """
    Realiza una búsqueda por interpolación en una lista ordenada.

    Complejidad:
    - Tiempo promedio: O(log log n) para distribuciones uniformes, O(n) en el peor de los casos.
    - Espacio: O(1), ya que la búsqueda no requiere espacio adicional significativo.

    Funcionamiento:
    - Calcula una posición probable del objetivo mediante una fórmula de interpolación.
    - Compara el objetivo con el elemento en la posición calculada.
    - Ajusta los índices de búsqueda según sea necesario y repite el proceso.

    Paralelización:
    - Aunque el nombre sugiere paralelización, esta implementación actual es recursiva y no paralela.
    """
    @staticmethod
    @performance_logger()
    def search(arr: List[int], target: int) -> int:
        """
        Busca un elemento en una lista ordenada utilizando la búsqueda por interpolación.

        Args:
            arr (List[int]): Lista ordenada de enteros donde buscar.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: Índice del elemento objetivo en la lista, o -1 si no se encuentra.
        """
        return ParallelInterpolationSearch._parallel_search(arr, 0, len(arr) - 1, target)

    @staticmethod
    def _parallel_search(arr: List[int], low: int, high: int, target: int) -> int:
        """
        Método auxiliar para realizar una búsqueda por interpolación.

        Args:
            arr (List[int]): Lista ordenada de enteros.
            low (int): Índice inferior del segmento de búsqueda.
            high (int): Índice superior del segmento de búsqueda.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: Índice del elemento objetivo en el segmento, o -1 si no se encuentra.
        """
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