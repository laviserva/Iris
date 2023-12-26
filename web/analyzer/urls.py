# En tu archivo urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyzer, name='analyzer'),
    path('process_algorithms/', views.process_algorithms, name='process-algorithms'),
]
