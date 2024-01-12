import io
import os
import sys
import inspect
import graphviz
import pandas as pd
import seaborn as sns
from typing import List

import matplotlib.pyplot as plt

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
algoritmos_path = os.path.join(root_path, 'Algoritmos')

if root_path not in sys.path:
    sys.path.append(root_path)

if algoritmos_path not in sys.path:
    sys.path.append(algoritmos_path)

from Algoritmos import log_fix
from Algoritmos import run_algorithms

class Plotter:
    """Clase que se encarga de generar las gráficas de los algoritmos que se le pasen como parámetro."""
    @staticmethod
    def plot(dot_content, out_file, dpi=300) -> io.BytesIO:
        # Crear un objeto Source y renderizar el gráfico
        dot = graphviz.Source(dot_content, format='png')
        buffer = io.BytesIO()
        buffer.write(dot.pipe())
        buffer.seek(0)

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
    def get_algorithm_complexities():
        ...
    
    @staticmethod
    def _from_dict_to_array(data):
        if data is None:
            return [None, None, None]
        complexities = Plotter.get_algorithm_complexities()
        algoritmos = [
            key.split(".")[0] + " " + complexities[key.split(".")[0]]["Time"] if "Parallel" not in key 
            else key.split(".")[0] 
            for key in data
        ]
        tiempos = [value['time'] for value in data.values()]
        memorias = [value['memory'] for value in data.values()]
        return algoritmos, tiempos, memorias
    
    @staticmethod
    def generate_plot(data: pd.DataFrame, x: str, y: str, title: str, xlabel: str, ylabel: str, hue: str) -> io.BytesIO:
        # Crear un regplot con Seaborn
        sns.barplot(x=x, y=y, data=data, hue=hue, ci=None, dodge=False)
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
        file_name_1 = os.path.join(root_path, "logs", "algorithm_performance.txt")
        file_name_2 = os.path.join(root_path, "logs", "algorithm_performance_reduced.txt")
        if os.path.exists(file_name_1):
            os.remove(file_name_1)
        if os.path.exists(file_name_2):
            os.remove(file_name_2)