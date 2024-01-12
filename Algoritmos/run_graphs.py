from abc import ABC, abstractmethod
from typing import Any, Dict

# Interfaz común para todos los algoritmos de camino más corto
class Algorithm(ABC):
    @abstractmethod
    def execute(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Método abstracto para ejecutar el algoritmo.

        Args:
            data (Dict[Any, Any]): Los datos sobre los que operar.

        Returns:
            Dict[Any, Any]: El resultado de la ejecución del algoritmo.
        """
        pass

# Clase envoltorio para algoritmos de camino más corto
class PathFindingAlgorithm(Algorithm):
    def __init__(self, algorithm: Any) -> None:
        """
        Inicializa una instancia de PathFindingAlgorithm.

        Args:
            algorithm (Any): Una instancia de un algoritmo de camino más corto.
        """
        self.algorithm = algorithm

    def execute(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Ejecuta el algoritmo de camino más corto en los datos proporcionados.

        Args:
            data (Dict[Any, Any]): Diccionario de datos para encontrar el camino más corto.

        Returns:
            Dict[Any, Any]: El resultado del algoritmo de camino más corto.
        """
        return self.algorithm.find(data)

# Fábrica de algoritmos
class AlgorithmFactory:
    @staticmethod
    def get_algorithm(module: Any, class_name: str) -> Algorithm:
        """
        Crea y devuelve una instancia de un algoritmo de camino más corto.

        Args:
            module (Any): El módulo donde se encuentra la clase del algoritmo.
            class_name (str): El nombre de la clase del algoritmo a instanciar.

        Returns:
            Algorithm: Una instancia del algoritmo especificado.
        """
        class_method = getattr(module, class_name)
        return PathFindingAlgorithm(class_method)