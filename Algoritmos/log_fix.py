import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
actual_dir = os.path.join(parent_dir, 'logs')
file_dir = os.path.join(actual_dir, 'algorithm_performance.txt')

def fix():
    with open(file_dir, 'r') as file:
        lines = file.readlines()

    log_data = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split(', ')
        algorithm = parts[0].split(': ')[1]
        time = float(parts[1].split(': ')[1].split(' ')[0])
        memory = float(parts[2].split(': ')[1].split(' ')[0])
        if not ".sort" in algorithm and not ".search" in algorithm:
            continue
        if algorithm not in log_data:
            log_data[algorithm] = {'time': time, 'memory': memory}
        else:
            log_data[algorithm]['time'] = max(log_data[algorithm]['time'], time)
            log_data[algorithm]['memory'] = max(log_data[algorithm]['memory'], memory)

    out_dir = os.path.join(actual_dir, "algorithm_performance_reduced.txt")
    with open(out_dir, 'w') as file:
        for algorithm, data in log_data.items():
            file.write(f"Algoritmo: {algorithm}, Tiempo: {data['time']:.6f} s, Memoria: {data['memory']:.2f} MiB\n")