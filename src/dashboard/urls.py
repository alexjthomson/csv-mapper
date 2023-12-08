from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('graphs', views.graphs_view, name='graphs'),
    path('sources', views.sources_view, name='sources')
]