# En tu archivo urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyzer, name='analyzer'),
]
