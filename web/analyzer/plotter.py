import io
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import List

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
algoritmos_path = os.path.join(root_path, 'Algoritmos')

if root_path not in sys.path:
    sys.path.append(root_path)

if algoritmos_path not in sys.path:
    sys.path.append(algoritmos_path)

from Algoritmos import log_fix
from Algoritmos import Paralelizables
from Algoritmos import Searching
from Algoritmos import Sorting
from Algoritmos import run_algorithms

from Algoritmos import Sorting, run_algorithms, Searching, Paralelizables, log_fix

class Plotter:
    """Clase que se encarga de generar las gráficas de los algoritmos que se le pasen como parámetro."""
    @staticmethod
    def plot(arr: List[float], sort_algorithms: List[str], search_algorithms: List[str], parallel_algorithms: List[str]) -> io.BytesIO:
        if sort_algorithms != []:
            run_algorithms.run_algorithms(arr, sort_algorithms, Sorting)
            if search_algorithms != []:
                run_algorithms.run_algorithms(arr, search_algorithms, Searching)
            if parallel_algorithms != []:
                sort_aux = [alg for alg in parallel_algorithms if "Sort" in alg]
                search_aux = [alg for alg in parallel_algorithms if "Search" in alg]
                if sort_aux != []:
                    run_algorithms.run_algorithms(arr, sort_aux, Paralelizables)
                if search_aux != []:
                    run_algorithms.run_algorithms(arr, search_aux, Paralelizables)

        # Limpiando los logs
        log_fix.fix()
        data = Plotter._load_performance()
        algorithm, time, memory = Plotter._from_dict_to_array(data)
        Plotter._delete_logs()
        if algorithm is None:
            return Plotter._base_plot()
        
        data = pd.DataFrame({'Algoritmo': algorithm, 'Tiempo': time, 'Memoria': memory})
        data_sorted = data.sort_values(by='Tiempo', ascending=False)

        buffer = Plotter.generate_plot(data = data_sorted, x = 'Algoritmo', y = 'Tiempo',
                                       title = 'Comparación de Tiempo por Algoritmo',
                                       xlabel = 'Algoritmo',
                                       ylabel = 'Tiempo (s)')
        return buffer
    
    @staticmethod
    def _load_performance():
        file_name = os.path.join(root_path, "logs", "algorithm_performance_reduced.txt")
        if not os.path.exists(file_name):
            return None
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        data = {}
        for line in lines:
            if not line.strip():
                continue
            parts = line.strip().split(', ')
            algorithm = parts[0].split(': ')[1]
            time = float(parts[1].split(': ')[1].split(' ')[0])
            memory = float(parts[2].split(': ')[1].split(' ')[0])
            if not ".sort" in algorithm and not ".search" in algorithm:
                continue
            if algorithm not in data:
                data[algorithm] = {'time': time, 'memory': memory}
            else:
                data[algorithm]['time'] = max(data[algorithm]['time'], time)
                data[algorithm]['memory'] = max(data[algorithm]['memory'], memory)

        return data
    
    @staticmethod
    def _from_dict_to_array(data):
        if data is None:
            return [None, None, None]
        algoritmos = [key for key in data]
        tiempos = [value['time'] for value in data.values()]
        memorias = [value['memory'] for value in data.values()]
        return algoritmos, tiempos, memorias
    
    @staticmethod
    def generate_plot(data: pd.DataFrame, x: str, y: str, title: str, xlabel: str, ylabel: str) -> io.BytesIO:
        # Crear un regplot con Seaborn
        sns.barplot(x=x, y=y, data=data)
        plt.xticks(rotation=45, ha='right')

        # Ajustar títulos y etiquetas
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # Mostrar la gráfica
        plt.tight_layout() 

        # Guardar la gráfica en un buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300)
        buffer.seek(0)
        plt.close()

        return buffer
    
    @staticmethod
    def _delete_logs():
        file_name_1 = os.path.join(root_path, "logs", "algorithm_performance_reduced.txt")
        file_name_2 = os.path.join(root_path, "logs", "algorithm_performance_reduced.txt")
        if os.path.exists(file_name_1):
            os.remove(file_name_1)
        if os.path.exists(file_name_2):
            os.remove(file_name_2)