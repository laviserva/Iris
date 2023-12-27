from performanzer import performance_logger

class BubbleSort:
    @staticmethod
    @performance_logger()
    def sort(data):
        n = len(data)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class QuickSort:
    @staticmethod
    @performance_logger()
    def sort(data):
        QuickSort._quick_sort_helper(data, 0, len(data)-1)
        return data

    @staticmethod
    @performance_logger()
    def _quick_sort_helper(data, low, high):
        if low < high:
            pi = QuickSort._partition(data, low, high)
            QuickSort._quick_sort_helper(data, low, pi-1)
            QuickSort._quick_sort_helper(data, pi+1, high)

    @staticmethod
    @performance_logger()
    def _partition(data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i = i + 1
                data[i], data[j] = data[j], data[i]
        data[i+1], data[high] = data[high], data[i+1]
        return i+1

class MergeSort:
    @staticmethod
    @performance_logger()
    def sort(data):
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
    @staticmethod
    @performance_logger()
    def sort(data):
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
    @performance_logger()
    def _heapify(data, n, i):
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
    @staticmethod
    @performance_logger()
    def sort(data):
        for i in range(1, len(data)):
            key = data[i]
            j = i-1
            while j >=0 and key < data[j]:
                data[j+1] = data[j]
                j -= 1
            data[j+1] = key
        return data

    @staticmethod
    @performance_logger()
    def _quick_sort_helper(data, low, high):
        if low < high:
            pi = QuickSort._partition(data, low, high)
            QuickSort._quick_sort_helper(data, low, pi-1)
            QuickSort._quick_sort_helper(data, pi+1, high)

    @staticmethod
    @performance_logger()
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
    @staticmethod
    @performance_logger()
    def sort(data):
        for i in range(len(data)):
            min_idx = i
            for j in range(i+1, len(data)):
                if data[min_idx] > data[j]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
        return data

class BucketSort:
    @staticmethod
    @performance_logger()
    def sort(data):
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
    @staticmethod
    @performance_logger()
    def sort(data):
        # Calcula el número máximo de dígitos decimales en los números
        decimal_places = max([len(str(number).split('.')[-1]) for number in data if '.' in str(number)], default=0)
        scale_factor = 10 ** decimal_places
        scaled_data = [int(x * scale_factor) for x in data]

        # Separar números negativos y positivos
        negative_nums = [-x for x in scaled_data if x < 0]
        non_negative_nums = [x for x in scaled_data if x >= 0]

        # Aplicar counting sort a cada subconjunto
        sorted_negatives = CountingSort._counting_sort(negative_nums)
        sorted_non_negatives = CountingSort._counting_sort(non_negative_nums)

        # Combinar los resultados y desescalar
        combined = [-x for x in reversed(sorted_negatives)] + sorted_non_negatives
        return [x / scale_factor for x in combined]

    @staticmethod
    def _counting_sort(data):
        if not data:
            return data

        min_val = min(data)
        max_val = max(data)
        range_of_elements = max_val - min_val + 1
        count = [0] * range_of_elements
        output = [0] * len(data)

        for number in data:
            count[number - min_val] += 1

        for i in range(1, len(count)):
            count[i] += count[i - 1]

        for number in reversed(data):
            output[count[number - min_val] - 1] = number
            count[number - min_val] -= 1

        return output

class TimSort:
    MIN_MERGE = 32

    @staticmethod
    @performance_logger()
    def calc_min_run(n):
        """Calcula el tamaño mínimo de una run."""
        r = 0
        while n >= TimSort.MIN_MERGE:
            r |= n & 1
            n >>= 1
        return n + r

    @staticmethod
    @performance_logger()
    def insertion_sort(arr, left, right):
        for i in range(left + 1, right + 1):
            temp = arr[i]
            j = i - 1
            while j >= left and arr[j] > temp:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = temp

    @staticmethod
    @performance_logger()
    def merge(arr, l, m, r):
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
    def sort(arr):
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