from abc import ABC, abstractmethod
from typing import Any, List
import random
import sys

# Interfaz común para todos los algoritmos
class Algorithm(ABC):
    @abstractmethod
    def execute(self, data: List[Any], args: Any = None) -> Any:
        """
        Método abstracto para ejecutar el algoritmo.

        Args:
            data (List[Any]): Los datos sobre los que operar.
            args (Any, opcional): Argumentos adicionales necesarios para el algoritmo.

        Returns:
            Any: El resultado de la ejecución del algoritmo.
        """
        pass

# Clases envoltorio para los algoritmos de ordenamiento, búsqueda y paralelización
class SortAlgorithm(Algorithm):
    def __init__(self, algorithm: Any) -> None:
        """
        Inicializa una instancia de SortAlgorithm.

        Args:
            algorithm (Any): Una instancia de un algoritmo de ordenamiento.
        """
        self.algorithm = algorithm

    def execute(self, data: List[Any], args: Any = None) -> None:
        """
        Ejecuta el algoritmo de ordenamiento en los datos proporcionados.

        Args:
            data (List[Any]): Lista de elementos a ordenar.
            args (Any, opcional): No se utiliza en este contexto.
        """
        self.algorithm.sort(data)

class SearchAlgorithm(Algorithm):
    def __init__(self, algorithm: Any) -> None:
        """
        Inicializa una instancia de SearchAlgorithm.

        Args:
            algorithm (Any): Una instancia de un algoritmo de búsqueda.
        """
        self.algorithm = algorithm

    def execute(self, data: List[Any], args: List[Any]) -> int:
        """
        Ejecuta el algoritmo de búsqueda en los datos proporcionados.

        Args:
            data (List[Any]): Lista de elementos en los que buscar.
            args (List[Any]): Argumentos adicionales para el algoritmo de búsqueda, 
                              como el elemento objetivo.

        Returns:
            int: El resultado de la búsqueda.
        """
        return self.algorithm.search(data, *args)


class ParallelAlgorithm(Algorithm):
    def __init__(self, algorithm: Any) -> None:
        """
        Inicializa una instancia de ParallelAlgorithm.

        Args:
            algorithm (Any): Una instancia de un algoritmo que se puede ejecutar en paralelo.
        """
        self.algorithm = algorithm

    def execute(self, data: List[Any], kind: str) -> Any:
        """
        Ejecuta el algoritmo paralelo dependiendo del tipo.

        Args:
            data (List[Any]): Lista de elementos a ordenar o buscar.
            kind (str): Tipo de operación ('sort' o 'search').

        Returns:
            Any: El resultado de la ejecución del algoritmo.
        """
        if kind == "sort":
            return self.algorithm.sort(data)
        elif kind == "search":
            return self.algorithm.search(data)

class DataStructureAlgorithm(Algorithm):
    def __init__(self, algorithm_class: Any) -> None:
        """
        Inicializa una instancia de DataStructureAlgorithm.

        Args:
            algorithm_class (Any): La clase del algoritmo que maneja una estructura de datos.
        """
        self.algorithm_class = algorithm_class

    def execute(self, data: List[Any], args: List[Any] = None) -> Any:
        """
        Ejecuta el algoritmo sobre una estructura de datos.

        Args:
            data (List[Any]): Lista de elementos para insertar en la estructura de datos.
            args (List[Any], opcional): Argumentos para la búsqueda en la estructura de datos.

        Returns:
            Any: El resultado de la búsqueda en la estructura de datos.
        """
        instance = self.algorithm_class()
        for item in data:
            instance.insert(item)
        return instance.search(*args)

class AlgorithmFactory:
    @staticmethod
    def get_algorithm(module: sys.modules, class_name: str) -> Algorithm:
        """
        Crea y devuelve una instancia de un algoritmo.

        Args:
            module (sys.modules): El módulo donde se encuentra la clase del algoritmo.
            class_name (str): El nombre de la clase del algoritmo a instanciar.

        Returns:
            Algorithm: Una instancia del algoritmo especificado.
        """
        class_method = getattr(module, class_name)
        if "Sort" in class_name:
            return SortAlgorithm(class_method)
        elif "Search" in class_name:
            return SearchAlgorithm(class_method)
        else:
            return DataStructureAlgorithm(class_method)


import random

def run_algorithms(arr: List[Any], algorithms_array: List[str], module: sys.modules, 
                   verbose: bool = False) -> None:
    """
    Ejecuta una serie de algoritmos en una lista de datos.

    Args:
        arr (List[Any]): Lista de datos sobre los cuales ejecutar los algoritmos.
        algorithms_array (List[str]): Array de nombres de clases de algoritmos a ejecutar.
        module (sys.modules): Módulo donde se encuentran las clases de algoritmos.
        verbose (bool, opcional): Si es True, imprime resultados detallados.
    """
    element_to_search = random.choice(arr)
    for class_name in algorithms_array:
        algorithm = AlgorithmFactory.get_algorithm(module, class_name)
        if isinstance(algorithm, SortAlgorithm):
            algorithm.execute(arr.copy())
        elif isinstance(algorithm, SearchAlgorithm):
            algorithm.execute(arr, [element_to_search])
        elif isinstance(algorithm, DataStructureAlgorithm):
            search_result = algorithm.execute(arr, [element_to_search])
            if verbose:
                if search_result:
                    print(f"El elemento {element_to_search} está en la estructura: {class_name}")
                else:
                    print(f"El elemento {element_to_search} no está en la estructura: {class_name}")
