from django.conf import settings
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

from analyzer.plotter import Plotter

matplotlib.use('Agg')
sns.set_style("whitegrid")  # Ejemplos: "darkgrid", "whitegrid", "dark", "white", "ticks"
sns.set_palette("pastel")   # Ejemplos: "deep", "muted", "bright", "pastel", "dark", "colorblind"

def analyzer(request):
    return render(request, 'analyzer.html')

def base_plot(request):


    print(__file__)
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    image_path = os.path.join(root_path, 'web', 'static', 'iris.png')

    img = mpimg.imread(image_path)

    # Crear una figura y un eje en Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')  # Ocultar los ejes

    # Guardar la figura en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', transparent=True, dpi=300)
    buffer.seek(0)
    plt.close(fig)

    return HttpResponse(buffer, content_type="image/png")

@csrf_exempt
@require_http_methods(["POST"])
def process_algorithms(request):
    data = json.loads(request.body)
    sort_algorithms = data.get('sortAlgorithm', [])
    search_algorithms = data.get('searchAlgorithm', [])
    parallel_algorithms = data.get('paralellAlgorithm', [])

    buffer = render_plot(sort_algorithms, search_algorithms, parallel_algorithms)

    # Guardar la imagen en un archivo
    filename = f"plot.png"
    filepath = os.path.join("temp", filename)
    with open(filepath, 'wb') as f:
        f.write(buffer.getvalue())

    # Almacenar la ruta del archivo en la sesión
    request.session['latest_plot_image'] = filepath

    return JsonResponse({'status': 'success'})

def latest_plot(request):
    # Obtener la ruta del archivo de la imagen más reciente
    filepath = request.session.get('latest_plot_image')
    if filepath and os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")
    else:
        return HttpResponse("No image available", status=404)

def render_plot(sort_algorithms, search_algorithms, parallel_algorithms):
    if sort_algorithms == [] and search_algorithms == [] and parallel_algorithms == []:
        return base_plot()
    n = 10_000
    arr = [i+1 for i in range(n)]
    random.shuffle(arr)
    buffer = Plotter.plot(arr, sort_algorithms, search_algorithms, parallel_algorithms)
    return buffer