from typing import List
from performanzer import performance_logger

class BubbleSort:
    """
    Implementa el algoritmo de ordenamiento burbuja.

    Complejidad:
    - Tiempo: O(n^2), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que el ordenamiento se realiza in situ.

    Métodos:
    - sort: Ordena una lista utilizando el algoritmo de ordenamiento burbuja.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento burbuja.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n^2), donde n es el número de elementos en la lista.
        - Espacio: O(1), ya que el ordenamiento se realiza in situ.
        """
        n = len(data)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class QuickSort:
    """
    Implementa el algoritmo de ordenamiento rápido (QuickSort).

    Complejidad:
    - Tiempo promedio: O(n log n), donde n es el número de elementos en la lista.
    - Tiempo en el peor caso: O(n^2), aunque este escenario es raro con un buen pivote.
    - Espacio: O(log n) en espacio adicional debido a la recursión.

    Métodos:
    - sort: Método público para ordenar la lista.
    - _quick_sort_helper: Método auxiliar para implementar QuickSort de manera recursiva.
    - _partition: Método para particionar la lista y seleccionar el pivote.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento rápido.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.
        """
        QuickSort._quick_sort_helper(data, 0, len(data)-1)
        return data

    @staticmethod
    def _quick_sort_helper(data: List[int], low: int, high: int) -> None:
        """
        Método auxiliar para implementar QuickSort de manera recursiva.

        Args:
            data (List[int]): Lista de enteros a ordenar.
            low (int): Índice más bajo de la lista o sublista.
            high (int): Índice más alto de la lista o sublista.
        """
        if low < high:
            pi = QuickSort._partition(data, low, high)
            QuickSort._quick_sort_helper(data, low, pi-1)
            QuickSort._quick_sort_helper(data, pi+1, high)

    @staticmethod
    def _partition(data: List[int], low: int, high: int) -> int:
        """
        Particiona la lista y selecciona el pivote.

        Args:
            data (List[int]): Lista de enteros a ordenar.
            low (int): Índice más bajo de la lista o sublista.
            high (int): Índice más alto de la lista o sublista.

        Returns:
            int: El índice del pivote después de la partición.
        """
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i = i + 1
                data[i], data[j] = data[j], data[i]
        data[i+1], data[high] = data[high], data[i+1]
        return i+1

class MergeSort:
    """
    Implementa el algoritmo de ordenamiento por mezcla (Merge Sort).

    Complejidad:
    - Tiempo: O(n log n), donde n es el número de elementos en la lista.
    - Espacio: O(n), ya que se requiere espacio adicional para las sublistas temporales.

    Métodos:
    - sort: Método público para ordenar la lista utilizando Merge Sort.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento por mezcla.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n log n), donde n es el número de elementos en la lista.
        - Espacio: O(n), ya que se requiere espacio adicional para las sublistas temporales.
        """
        if len(data) > 1:
            mid = len(data) // 2
            L = data[:mid]
            R = data[mid:]

            MergeSort.sort(L)
            MergeSort.sort(R)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    data[k] = L[i]
                    i += 1
                else:
                    data[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                data[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                data[k] = R[j]
                j += 1
                k += 1
        return data

class HeapSort:
    """
    Implementa el algoritmo de ordenamiento por montículo (Heap Sort).

    Complejidad:
    - Tiempo: O(n log n), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que el ordenamiento se realiza in situ.

    Métodos:
    - sort: Ordena una lista utilizando Heap Sort.
    - _heapify: Método auxiliar para mantener la propiedad de montículo.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento por montículo.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n log n), donde n es el número de elementos en la lista.
        - Espacio: O(1), ya que el ordenamiento se realiza in situ.
        """
        n = len(data)

        # Build a maxheap.
        for i in range(n//2 - 1, -1, -1):
            HeapSort._heapify(data, n, i)

        # Extract elements one by one
        for i in range(n-1, 0, -1):
            data[i], data[0] = data[0], data[i]  # swap
            HeapSort._heapify(data, i, 0)
        return data

    @staticmethod
    def _heapify(data: List[int], n: int, i: int) -> None:
        """
        Método auxiliar para mantener la propiedad de montículo.

        Args:
            data (List[int]): Lista de enteros.
            n (int): Tamaño del montículo.
            i (int): Índice del elemento a monticularizar.
        """
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and data[l] > data[largest]:
            largest = l

        if r < n and data[r] > data[largest]:
            largest = r

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            HeapSort._heapify(data, n, largest)

class InsertionSort:
    """
    Implementa el algoritmo de ordenamiento por inserción.

    Complejidad:
    - Tiempo: O(n^2) en el peor caso, donde n es el número de elementos en la lista.
    - Tiempo: O(n) en el mejor caso, cuando la lista ya está casi ordenada.
    - Espacio: O(1), ya que el ordenamiento se realiza in situ.

    Métodos:
    - sort: Ordena una lista utilizando el algoritmo de ordenamiento por inserción.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento por inserción.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n^2) en el peor caso, O(n) en el mejor caso.
        - Espacio: O(1), ya que el ordenamiento se realiza in situ.
        """
        for i in range(1, len(data)):
            key = data[i]
            j = i-1
            while j >=0 and key < data[j]:
                data[j+1] = data[j]
                j -= 1
            data[j+1] = key
        return data

    @staticmethod
    def _quick_sort_helper(data, low, high):
        if low < high:
            pi = QuickSort._partition(data, low, high)
            QuickSort._quick_sort_helper(data, low, pi-1)
            QuickSort._quick_sort_helper(data, pi+1, high)

    @staticmethod
    def _partition(data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i = i + 1
                data[i], data[j] = data[j], data[i]
        data[i+1], data[high] = data[high], data[i+1]
        return i+1

class SelectionSort:
    """
    Implementa el algoritmo de ordenamiento por selección.

    Complejidad:
    - Tiempo: O(n^2), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que el ordenamiento se realiza in situ.

    Métodos:
    - sort: Ordena una lista utilizando el algoritmo de ordenamiento por selección.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento por selección.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n^2), independientemente de la ordenación inicial de los datos.
        - Espacio: O(1), ya que el ordenamiento se realiza in situ.
        """
        for i in range(len(data)):
            min_idx = i
            for j in range(i+1, len(data)):
                if data[min_idx] > data[j]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
        return data

class BucketSort:
    """
    Implementa el algoritmo de ordenamiento por cubetas (Bucket Sort).

    Complejidad:
    - Tiempo: O(n + k), donde n es el número de elementos y k es el número de cubetas.
    - Espacio: O(n * k), ya que se crean listas adicionales para los cubos.

    Métodos:
    - sort: Ordena una lista utilizando el algoritmo de ordenamiento por cubetas.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento por cubetas.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n + k), donde n es el número de elementos y k es el número de cubetas.
        - Espacio: O(n * k), debido a la creación de listas adicionales para los cubos.
        """
        if not data:
            return []

        # Encuentra los valores mínimo y máximo para calcular el rango
        min_value = min(data)
        max_value = max(data)
        range_value = max_value - min_value

        # Crea buckets para números negativos, positivos y cero
        bucket_count = len(data)
        buckets = [[] for _ in range(bucket_count)]
        
        for d in data:
            # Índice normalizado para el bucket
            if range_value > 0:
                index = int((d - min_value) / range_value * (bucket_count - 1))
            else:
                index = 0
            buckets[index].append(d)
        
        # Ordena cada bucket y combina
        sorted_arr = []
        for bucket in buckets:
            sorted_arr.extend(sorted(bucket))
        return sorted_arr

class RadixSort:
    """
    Implementa el algoritmo de ordenamiento Radix Sort.

    Complejidad:
    - Tiempo: O(d * (n + b)), donde n es el número de elementos, d es el número de dígitos en el número más grande, y b es la base numérica (generalmente 10).
    - Espacio: O(n + b), ya que se requiere espacio adicional para los arreglos de conteo y salida.

    Métodos:
    - sort: Ordena una lista utilizando Radix Sort.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento Radix Sort.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(d * (n + b)), donde d es el número de dígitos, n es el número de elementos y b es la base numérica.
        - Espacio: O(n + b), debido a la necesidad de arreglos adicionales para el conteo y la salida.
        """
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

        # Aplicar Radix Sort a cada subconjunto
        radix_sort(neg)
        radix_sort(non_neg)

        # Unir los resultados y ajustar los números negativos
        return [-x for x in reversed(neg)] + non_neg

class CountingSort:
    """
    Implementa el algoritmo de ordenamiento por conteo (Counting Sort) con capacidad para manejar números negativos.

    Complejidad:
    - Tiempo: O(n + k), donde n es el número de elementos y k es el rango de los valores escalados.
    - Espacio: O(k), ya que se necesita espacio para el diccionario de conteo.

    Métodos:
    - sort: Ordena una lista utilizando Counting Sort.
    - _optimized_counting_sort: Método auxiliar para implementar un Counting Sort optimizado.
    """
    @staticmethod
    @performance_logger()
    def sort(data: List[float]) -> List[float]:
        """
        Ordena una lista utilizando el algoritmo de ordenamiento por conteo.

        Args:
            data (List[float]): Lista de números flotantes a ordenar.

        Returns:
            List[float]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n + k), donde n es el número de elementos y k es el rango de los valores escalados.
        - Espacio: O(k), debido al uso de un diccionario para el conteo.
        """
        # Escalamos los números para reducir el rango
        #max_abs_val = max(abs(num) for num in data)
        scale_factor = 10**3 #10 ** len(str(int(max_abs_val)))
        scaled_data = [int(x * scale_factor) for x in data]

        # Separamos los números negativos y no negativos
        negative_nums = [-x for x in scaled_data if x < 0]
        non_negative_nums = [x for x in scaled_data if x >= 0]

        # Ordenamos cada subconjunto usando un counting sort optimizado
        sorted_negatives = CountingSort._optimized_counting_sort(negative_nums)
        sorted_non_negatives = CountingSort._optimized_counting_sort(non_negative_nums)

        # Combinamos y desescalamos
        combined = [-x for x in reversed(sorted_negatives)] + sorted_non_negatives
        return [x / scale_factor for x in combined]

    @staticmethod
    def _optimized_counting_sort(data: List[int]) -> List[int]:
        """
        Método auxiliar para implementar un Counting Sort optimizado.

        Args:
            data (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada de enteros.

        Complejidad:
        - Tiempo: O(n + k), donde n es el número de elementos y k es el rango de los valores.
        - Espacio: O(k), debido al uso de un diccionario para el conteo.
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

class TimSort:
    """
    Implementación del algoritmo de ordenamiento TimSort.

    TimSort es un algoritmo híbrido que combina el ordenamiento por inserción y el Merge Sort,
    optimizado para un rendimiento eficiente en casos prácticos.

    Atributos:
        MIN_MERGE (int): El tamaño mínimo de una run. Determina si se utiliza el ordenamiento por inserción o Merge Sort.

    Métodos:
        calc_min_run(n: int) -> int:
            Calcula el tamaño mínimo de una run para el TimSort.
            Complejidad:
            - Tiempo: O(log n)
            - Espacio: O(1)

        insertion_sort(arr: List[int], left: int, right: int) -> None:
            Ordena una subsección del arreglo usando ordenamiento por inserción.
            Complejidad:
            - Tiempo: O(n^2) en el peor caso para la subsección.
            - Espacio: O(1) - Ordenamiento in situ.

        merge(arr: List[int], l: int, m: int, r: int) -> None:
            Fusiona dos subsecciones ordenadas del arreglo.
            Complejidad:
            - Tiempo: O(n), donde n es el número total de elementos en ambas subsecciones.
            - Espacio: O(n) para almacenar las subsecciones temporales.

        sort(arr: List[int]) -> List[int]:
            Ordena el arreglo completo utilizando TimSort.
            Complejidad:
            - Tiempo: O(n log n) en el caso promedio y en el peor caso.
            - Espacio: O(n) para almacenar subsecciones temporales durante la fusión.
    """
    MIN_MERGE = 32

    @staticmethod
    @performance_logger()
    def calc_min_run(n: int) -> int:
        """
        Calcula el tamaño mínimo de una run.

        Args:
            n (int): Tamaño del arreglo a ordenar.

        Returns:
            int: Tamaño mínimo de una run.

        Complejidad:
        - Tiempo: O(log n), ya que es el cálculo de un umbral basado en el tamaño de la lista.
        - Espacio: O(1), no se requiere espacio adicional.
        """
        r = 0
        while n >= TimSort.MIN_MERGE:
            r |= n & 1
            n >>= 1
        return n + r

    @staticmethod
    def insertion_sort(arr: List[int], left: int, right: int) -> None:
        """
        Ordenamiento por inserción aplicado a una parte del arreglo.

        Args:
            arr (List[int]): Arreglo a ordenar.
            left (int): Índice inicial de la parte a ordenar.
            right (int): Índice final de la parte a ordenar.

        Complejidad:
        - Tiempo: O(n^2) en el peor caso, pero eficiente para pequeñas subsecciones.
        - Espacio: O(1), ordenamiento in situ.
        """
        for i in range(left + 1, right + 1):
            temp = arr[i]
            j = i - 1
            while j >= left and arr[j] > temp:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = temp

    @staticmethod
    def merge(arr: List[int], l: int, m: int, r: int) -> None:
        """
        Fusiona dos subsecciones ordenadas de un arreglo.

        Args:
            arr (List[int]): Arreglo a ordenar.
            l (int): Índice inicial del primer segmento.
            m (int): Índice final del primer segmento.
            r (int): Índice final del segundo segmento.

        Complejidad:
        - Tiempo: O(n), donde n es el número de elementos en las subsecciones.
        - Espacio: O(n), necesita espacio para las subsecciones temporales.
        """
        len1, len2 = m - l + 1, r - m
        left = arr[l:l + len1]
        right = arr[m + 1:m + 1 + len2]

        i = j = 0
        k = l

        while i < len1 and j < len2:
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len1:
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len2:
            arr[k] = right[j]
            j += 1
            k += 1

    @staticmethod
    @performance_logger()
    def sort(arr: List[int]) -> List[int]:
        """
        Ordena una lista utilizando el algoritmo TimSort.

        Args:
            arr (List[int]): Lista de enteros a ordenar.

        Returns:
            List[int]: Lista ordenada.

        Complejidad:
        - Tiempo: O(n log n), donde n es el número de elementos en la lista.
        - Espacio: O(n), utiliza espacio adicional para fusionar subsecciones.
        """
        n = len(arr)
        min_run = TimSort.calc_min_run(n)

        for start in range(0, n, min_run):
            end = min(start + min_run - 1, n - 1)
            TimSort.insertion_sort(arr, start, end)

        size = min_run
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(n - 1, left + size - 1)
                right = min((left + 2 * size - 1), (n - 1))

                if mid < right:
                    TimSort.merge(arr, left, mid, right)

            size *= 2
        return arr