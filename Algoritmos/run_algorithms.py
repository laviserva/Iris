from abc import ABC, abstractmethod
import Sorting
import Searching
import Paralelizables
import random

# Interfaz común para todos los algoritmos
class Algorithm(ABC):
    @abstractmethod
    def execute(self, data, args=None):
        pass

# Clases envoltorio para los algoritmos de ordenamiento, búsqueda y paralelización
class SortAlgorithm(Algorithm):
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def execute(self, data, args=None):
        self.algorithm.sort(data)

class SearchAlgorithm(Algorithm):
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def execute(self, data, args):
        self.algorithm.search(data, *args)

class ParallelAlgorithm(Algorithm):
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def execute(self, data, kind):
        if kind == "sort":
            self.algorithm.sort(data)
        elif kind == "search":
            self.algorithm.search(data)

class DataStructureAlgorithm(Algorithm):
    def __init__(self, algorithm_class):
        self.algorithm_class = algorithm_class

    def execute(self, data, args=None):
        instance = self.algorithm_class()
        # Aquí puedes insertar los datos en la estructura
        for item in data:
            instance.insert(item)
        # Luego realiza la búsqueda
        return instance.search(*args)

# Factoría para crear instancias de algoritmos
class AlgorithmFactory:
    @staticmethod
    def get_algorithm(module, class_name):
        print(class_name)
        class_method = getattr(module, class_name)
        if "Sort" in class_name:
            return SortAlgorithm(class_method)
        elif "Search" in class_name:
            return SearchAlgorithm(class_method)
        else:
            return DataStructureAlgorithm(class_method)

# Función para ejecutar algoritmos
def run_algorithms(arr, algorithms_array, module):
    element_to_search = random.choice(arr)
    for class_name in algorithms_array:
        algorithm = AlgorithmFactory.get_algorithm(module, class_name)
        if isinstance(algorithm, SortAlgorithm):
            algorithm.execute(arr.copy())
        elif isinstance(algorithm, SearchAlgorithm):
            algorithm.execute(arr, [element_to_search])
        elif isinstance(algorithm, DataStructureAlgorithm):
            search_result = algorithm.execute(arr, [element_to_search])
            if search_result:
                print(f"El elemento {element_to_search} está en la estructura: {class_name}")
            else:
                print(f"El elemento {element_to_search} no está en la estructura: {class_name}")
        

"""# Ejemplo de uso
arr = [12, 11, 13, 5, 6, 7]
run_algorithms(arr, ["SkipList", "BinaryTree", "RedBlackTree"], Searching)
"""