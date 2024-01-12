# En tu archivo urls.py
from django.urls import path
from . import views

print(dir(views))

urlpatterns = [
    path('', views.graphs, name='graphs'),
    path('process_algorithms/', views.process_algorithms, name='process-algorithms'),
    path('latest_graph/', views.latest_graph, name='latest-graph'),
]