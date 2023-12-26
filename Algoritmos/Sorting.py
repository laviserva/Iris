class BubbleSort:
    @staticmethod
    def sort(data):
        n = len(data)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class QuickSort:
    @staticmethod
    def sort(data):
        QuickSort._quick_sort_helper(data, 0, len(data)-1)
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

"""# Uso del algoritmo
arr = [12, 11, 13, 5, 6, 7]
sorted_arr = QuickSort.sort(arr)
print("Sorted array is:", sorted_arr)
"""

class MergeSort:
    @staticmethod
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
    @staticmethod
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
    def sort(data):
        bucket = [[] for _ in range(len(data))]
        for d in data:
            index = int(10 * d)
            bucket[index].append(d)
        for b in bucket:
            b.sort()
        return [item for sublist in bucket for item in sublist]

class RadixSort:
    @staticmethod
    def sort(data):
        RADIX = 10
        maxLength = False
        tmp, placement = -1, 1

        while not maxLength:
            maxLength = True
            buckets = [list() for _ in range(RADIX)]

            for i in data:
                tmp = i // placement
                buckets[tmp % RADIX].append(i)
                if maxLength and tmp > 0:
                    maxLength = False

            a = 0
            for b in range(RADIX):
                buck = buckets[b]
                for i in buck:
                    data[a] = i
                    a += 1

            placement *= RADIX
        return data

class CountingSort:
    @staticmethod
    def sort(data):
        max_val = max(data)
        m = max_val + 1
        count = [0] * m
                
        for a in data:
            count[a] += 1
        i = 0
        for a in range(m):
            for c in range(count[a]):
                data[i] = a
                i += 1
        return data

class TimSort:
    MIN_MERGE = 32

    @staticmethod
    def calc_min_run(n):
        """Calcula el tamaño mínimo de una run."""
        r = 0
        while n >= TimSort.MIN_MERGE:
            r |= n & 1
            n >>= 1
        return n + r

    @staticmethod
    def insertion_sort(arr, left, right):
        """Un simple insertion sort para ordenar un fragmento de array."""
        for i in range(left + 1, right + 1):
            temp = arr[i]
            j = i - 1
            while j >= left and arr[j] > temp:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = temp

    @staticmethod
    def merge(arr, l, m, r):
        """Fusiona dos partes del array."""
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
