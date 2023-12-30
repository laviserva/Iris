import matplotlib
import json
import sys
import io
import os

import random

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
sns.set_theme(style="whitegrid")

def analyzer(request):
    return render(request, 'analyzer.html')

def base_plot(request):
    data = sns.load_dataset("iris")

    # Crear un regplot con Seaborn
    plot = sns.kdeplot(x="sepal_length", y="sepal_width", data=data, hue="species")

    # Guardar la gráfica en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer, content_type='image/png')

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
    
    arr = [random.randint(0, 100) for _ in range(100)]
    buffer = Plotter.plot(arr, sort_algorithms, search_algorithms, parallel_algorithms)
    return buffer