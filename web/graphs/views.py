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
    print("ELPEPE DOT_FILE: ", dot_file)

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
    print("ELPEPE FILEPATH: ", filepath)
    if filepath and os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")
    else:
        return HttpResponse("No image available", status=404)

def render_graph(algorithm, dpi=300):
    actual_path = os.path.abspath(os.path.dirname(__file__))
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    dot_file = os.path.join(actual_path, 'temp', 'Grafo.dot')
    out_file = os.path.join(root_path, "temp", "plot.png")
    print("ELPEPE DOT_FILE: ", dot_file)

    print("ELPEPE ALGORITMO: ", algorithm)

    buffer = Plotter.plot(dot_file, out_file, dpi=dpi)

    return buffer