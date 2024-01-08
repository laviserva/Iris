import time
from memory_profiler import memory_usage

import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_dir = os.path.join(parent_dir, "logs", "algorithm_performance.txt")

def performance_logger(algorithm_name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Medir tiempo de inicio y memoria antes de la ejecución
            start_time = time.time()
            mem_before = memory_usage()[0]

            result = func(*args, **kwargs)

            # Medir tiempo de finalización y memoria después de la ejecución
            end_time = time.time()
            mem_after = memory_usage()[0]

            # Calcular el tiempo y el uso de memoria
            time_elapsed = end_time - start_time
            mem_used = mem_after - mem_before

            # Determinar el nombre del algoritmo
            algo_name = algorithm_name if algorithm_name else func.__qualname__

            # Información de rendimiento
            performance_info = f"Algoritmo: {algo_name}, Tiempo: {time_elapsed:.6f} s, Memoria: {mem_used:.6f} MiB\n"
            
            if not os.path.exists(file_dir):
                with open(file_dir, "w") as file:
                    file.write(performance_info)
            else:
                # Escribir en un archivo
                with open(file_dir, "a") as file:
                    file.write(performance_info)

            return result

        return wrapper
    return decorator