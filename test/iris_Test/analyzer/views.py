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
    # Aquí puedes añadir lógica para seleccionar diferentes gráficos basado en la entrada del usuario

    # Ejemplo de gráfico Seaborn
    sns.set_theme(style="darkgrid")
    tips = sns.load_dataset("tips")
    ax = sns.barplot(x="day", y="total_bill", data=tips)

    # Guarda la gráfica en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=400)  # Aumentar DPI para una mejor resolución
    buffer.seek(0)
    plt.close()

    # Devuelve la imagen como respuesta HTTP
    return HttpResponse(buffer, content_type='image/png')