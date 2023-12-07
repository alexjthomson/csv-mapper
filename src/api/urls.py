from django.urls import path
from . import views

urlpatterns = [
    path('source', views.source, name='source'),
    path('graph', views.graph, name='graph')
]