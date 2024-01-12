import heapq
import re
import sys
from typing import Dict, List
from performanzer import performance_logger

from run_graphs import AlgorithmFactory
import Graphs

class ProcessGraphvizFormat:
    """
    Procesa el contenido de un archivo .dot para obtener la representación del grafo.

    Métodos:
    - read_file: Procesa el contenido del archivo .dot.
    """
    @staticmethod
    def read_file(dot_file: str) -> Dict[int, Dict[int, int]]:
        """
        Procesa el contenido del archivo .dot para obtener la representación del grafo.

        Args:
            dot_file (str): Archivo .dot.

        Returns:
            Dict[int, Dict[int, int]]: Representación del grafo como un diccionario
                                       donde las claves son los nodos y los valores
                                       son diccionarios de nodos adyacentes con sus
                                       pesos.
        """
        # Implementación del procesamiento del archivo .dot aquí
        nodes = []
        edges = {}

        with open(dot_file, "r") as f:
            for line in f:
                line = line.strip()

                if "}" in line:  # End of the graph definition
                    break

                # Check for edge definitions
                if "->" in line or "--" in line:
                    # Determine edge type
                    edge_symbol = "->" if "->" in line else "--"

                    # Parse nodes and attributes
                    parts = line.split(edge_symbol)
                    node_1 = parts[0].strip()
                    node_2 = parts[1].split()[0].strip()
                    label = re.search(r'label=(\d+)', line)
                    label = int(label.group(1)) if label else None
                    color = re.search(r'color=([a-zA-Z]+)', line)
                    color = color.group(1) if color else None

                    # Print for verification

                    # Update nodes and edges
                    if node_1 not in nodes:
                        nodes.append(node_1)
                    if node_2 not in nodes:
                        nodes.append(node_2)

                    if node_1 not in edges:
                        edges[node_1] = []
                    if node_2 not in edges:
                        edges[node_2] = []

                    edges[node_1].append([node_2, label, color])

                    if edge_symbol == "--":
                        edges[node_2].append([node_1, label, color])

        return nodes, edges

    @staticmethod
    def save_file(dot_content: Dict, out_file: str):
        """
        Procesa el contenido del diccionario para guardarlo en un archivo .dot

        Args:
            dot_content (Dict): contenido del diccionario.
        """
        # Implementación del procesamiento del archivo .dot aquí
        with open(out_file, "w") as f:
            f.write(dot_content)
        

class Dijkstra:
    Time_Complexity = "O(V^2)"
    Space_Complexity = "O(V)"
    """
    Implementa el algoritmo de Dijkstra para encontrar el camino más corto.

    Complejidad:
    - Tiempo: O(V^2), donde V es el número de vértices.
    - Espacio: O(V), para almacenar las distancias.

    Métodos:
    - find: Encuentra el shortest path.
    """
    #@performance_logger
    @staticmethod
    def find(data: Dict[int, Dict[int, int]], start: str) -> Dict[int, int]:
        """
        Encuentra el camino más corto utilizando el algoritmo de Dijkstra.

        Args:
            data (Dict[int, Dict[int, int]]): Representación del grafo como un diccionario
                                              donde las claves son los nodos y los valores
                                              son diccionarios de nodos adyacentes con sus
                                              pesos.

        Returns:
            Dict[int, int]: Diccionario con la distancia más corta desde el nodo fuente
                            a todos los demás nodos.
        """
        distances = {vertex[0]: float('infinity') for vertex in data}
        distances[start] = 0

        previous_nodes = {vertex: None for vertex in data}

        pq = [(0, start)]
        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            for neighbor, weight, _ in data[current_vertex]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

        return distances, previous_nodes

    @staticmethod
    def shortest_path(graph, start, goal):
        distances, previous_nodes = Dijkstra.find(graph, start)
        path = []
        current_node = goal
        while current_node is not None:
            path.insert(0, current_node)
            current_node = previous_nodes[current_node]

        if path[0] == start:  # Esto verifica si hay un camino conectado
            return path, distances[goal]
        else:
            return "No hay un camino conectado entre {} y {}".format(start, goal)


if __name__ == "__main__":
    # Ejemplo de datos del grafo
    graph_file = r"C:\Users\PC-04\Documents\Proyectos\Iris\web\graphs\temp\Grafo.dot"

    graph_data = ProcessGraphvizFormat.read_file(graph_file)
    _, graph_data = graph_data
    ProcessGraphvizFormat.save_file(graph_data, r"C:\Users\PC-04\Documents\Proyectos\Iris\web\graphs\temp\Grafo2.dot")

    # Obtener el algoritmo y ejecutarlo
    start = '1'
    goal = '5'
    dijkstra_algorithm = AlgorithmFactory.get_algorithm(Graphs, 'Dijkstra')
    shortest_paths = dijkstra_algorithm.execute(graph_data, start, goal)