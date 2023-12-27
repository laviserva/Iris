# En tu archivo urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyzer, name='analyzer'),
    path('process_algorithms/', views.process_algorithms, name='process-algorithms'),
    path('latest_plot/', views.latest_plot, name='latest-plot'),  # Agregar esta línea
]