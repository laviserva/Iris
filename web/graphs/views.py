from django.conf import settings
import graphviz
import matplotlib
import json
import sys
import io
import os
import random

import matplotlib.image as mpimg
from PIL import Image

import matplotlib.pyplot as plt
from django.shortcuts import render
import seaborn as sns

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from Algoritmos import Graphs
from Algoritmos.Graphs import ProcessGraphvizFormat
from Algoritmos.run_graphs import AlgorithmFactory

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
algoritmos_path = os.path.join(root_path, 'Algoritmos')

if root_path not in sys.path:
    sys.path.append(root_path)

if algoritmos_path not in sys.path:
    sys.path.append(algoritmos_path)

from graphs.plotter import Plotter

matplotlib.use('Agg')
sns.set_style("whitegrid")  # Ejemplos: "darkgrid", "whitegrid", "dark", "white", "ticks"
sns.set_palette("pastel")   # Ejemplos: "deep", "muted", "bright", "pastel", "dark", "colorblind"

def graphs(request):
    return render(request, 'graphs.html')

def base_graph(request):
    actual_path = os.path.abspath(os.path.dirname(__file__))

    dot_file = os.path.join(actual_path, 'temp', 'Grafo.dot')

    with open(dot_file, 'r') as file:
            dot_content = file.read()
        
    # Crear un objeto Source y renderizar el gráfico
    dot = graphviz.Source(dot_content, format='png')

    output_path = os.path.join(actual_path, 'temp', 'graph')

    # Render and save the graph
    dot.render(filename=output_path, cleanup=True)

    img = mpimg.imread(output_path+".png")

    # Crear una figura y un eje en Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')  # Ocultar los ejes

    # Guardar la figura en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', transparent=True, dpi=200)
    buffer.seek(0)
    plt.close(fig)

    return HttpResponse(buffer, content_type="image/png")

@csrf_exempt
@require_http_methods(["POST"])
def process_algorithms(request):
    data = json.loads(request.body)
    algorithm = data.get('selectedAlgorithm', [])
    if not algorithm:
        return JsonResponse({'status': 'error', 'message': 'No algorithm selected'})
    
    buffer = render_graph(algorithm)

    # Guardar la imagen en un archivo
    filename = f"plot.png"
    filepath = os.path.join("temp", filename)
    with open(filepath, 'wb') as f:
        f.write(buffer.getvalue())

    # Almacenar la ruta del archivo en la sesión
    request.session['latest_graph_image'] = filepath

    return JsonResponse({'status': 'success'})

def latest_graph(request):
    # Obtener la ruta del archivo de la imagen más reciente
    filepath = request.session.get('latest_graph_image')
    if filepath and os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")
    else:
        return HttpResponse("No image available", status=404)

def render_graph(algorithm, dpi=300):
    actual_path = os.path.abspath(os.path.dirname(__file__))

    dot_file = os.path.join(actual_path, 'temp', 'Grafo.dot')
    nodes, graph_data = ProcessGraphvizFormat.read_file(dot_file)
    start = random.choice(nodes)
    goal = random.choice(nodes)
    while start == goal:
        goal = random.choice(nodes)

    dijkstra_algorithm = AlgorithmFactory.get_algorithm(Graphs, algorithm)
    shortest_paths = dijkstra_algorithm.execute(graph_data, start, goal)

    shortest_path, _ = shortest_paths
    buffer = process_shortest_path(dot_file, shortest_path)

    return buffer

def process_shortest_path(dot_file, shortest_path):
    actual_path = os.path.abspath(os.path.dirname(__file__))
    new_dot_content = coloryze_edges(dot_file, shortest_path)

    new_dot_file = os.path.join(actual_path, 'temp', 'Grafo 2')
    ProcessGraphvizFormat.save_file(new_dot_content, new_dot_file + ".dot")

    dot = graphviz.Source(new_dot_content, format='png')

    output_path = os.path.join(actual_path, 'temp', 'graph 2')

    # Render and save the graph
    dot.render(filename=output_path, cleanup=True)

    img = mpimg.imread(output_path+".png")

    # Crear una figura y un eje en Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')  # Ocultar los ejes

    # Guardar la figura en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', transparent=True, dpi=200)
    
    return buffer

def coloryze_edges(dot_file, shortest_path):
    with open(dot_file, 'r') as file:
        dot_content = file.read()

    for i in range(len(shortest_path)-1):
        if f"{shortest_path[i]} -- {shortest_path[i+1]}" in dot_content:
            dot_content = dot_content.replace(f"{shortest_path[i]} -- {shortest_path[i+1]}", f"{shortest_path[i]} -- {shortest_path[i+1]} [color=red]")
        elif f"{shortest_path[i+1]} -- {shortest_path[i]}" in dot_content:
            dot_content = dot_content.replace(f"{shortest_path[i+1]} -- {shortest_path[i]}", f"{shortest_path[i+1]} -- {shortest_path[i]} [color=red]")

    return dot_content