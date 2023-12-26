import matplotlib
import json
import io

import matplotlib.pyplot as plt
from django.shortcuts import render
import seaborn as sns

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

matplotlib.use('Agg')  # Usa el backend 'Agg' para Matplotlib

def analyzer(request):
    return render(request, 'analyzer.html')

def generate_plot(request):
    sns.set_theme(style="whitegrid")
    data = sns.load_dataset("iris")

    # Crear un regplot con Seaborn
    plot = sns.kdeplot(x="sepal_length", y="sepal_width", data=data, hue="species")

    # Guardar la gráfica en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    plt.close()

    # Devuelve la imagen como respuesta HTTP
    return HttpResponse(buffer, content_type='image/png')

@csrf_exempt
@require_http_methods(["POST"])
def process_algorithms(request):
    data = json.loads(request.body)
    sort_algorithms = data.get('sortAlgorithm', [])
    search_algorithms = data.get('searchAlgorithm', [])
    parallel_algorithms = data.get('paralellAlgorithm', [])

    # Procesa los datos aquí
    print('Los algoritmos de ordenamiento seleccionados son:')
    print(sort_algorithms)
    print("Los algoritmos de búsqueda seleccionados son:")
    print(search_algorithms)
    print("Los algoritmos paralelos seleccionados son:")
    print(parallel_algorithms)

    return JsonResponse({'status': 'success'})