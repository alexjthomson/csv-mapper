from django.urls import path
from . import views

urlpatterns = [
    path('source/', views.source_list, name='source_list'),
    path('source/<int:source_id>/', views.source_detail, name='source_detail'),
    path('source/<int:source_id>/data/', views.source_data, name='source_data'),
    path('graph/', views.graph_list, name='graph_list'),
    path('graph/<int:graph_id>/', views.graph_detail, name='graph_detail')
]