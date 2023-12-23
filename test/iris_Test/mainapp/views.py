# views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import CssUploadForm
from .models import CssFile
from .forms import CsvUploadForm

import pandas as pd

def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('csvfile')
        print("El libro es: ", uploaded_file.name)
        if uploaded_file:

            return JsonResponse({'message': 'Archivo procesado exitosamente'})

        else:
            return JsonResponse({'error': 'No se proporcionó ningún archivo'}, status=400)

    return render(request, 'home.html')


def upload_csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesar el archivo CSV aquí
            return render(request, 'success.html')
    else:
        form = CsvUploadForm()
    return render(request, 'upload.html', {'form': form})

import pandas as pd

def cargar_csv(request):
    if request.method == 'POST':
        csvfile = request.FILES.get('csvfile')
        if not csvfile:
            return JsonResponse({'error': 'No se proporcionó ningún archivo.'}, status=400)

        # Cargar el archivo CSV en un DataFrame de Pandas
        try:
            df = pd.read_csv(csvfile)
            # Aquí puedes procesar el DataFrame como necesites
            # Por ejemplo, imprimirlo en la consola del servidor
            print(df)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Archivo cargado exitosamente.'})

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def upload_css(request):
    if request.method == 'POST':
        form = CssUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = CssFile(file=request.FILES['file'])
            new_file.save()
            return HttpResponse("Archivo CSS cargado con éxito.")
    else:
        form = CssUploadForm()
    return render(request, 'upload.html', {'form': form})