from django.http import HttpResponse
from django.shortcuts import render
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import io

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