from django.urls import path
from . import views

urlpatterns = [
    path('source/', views.SourceListView.as_view(), name='source_list'),
    path('source/<int:source_id>/', views.SourceDetailView.as_view(), name='source_detail'),
    path('source/<int:source_id>/data/', views.SourceDataView.as_view(), name='source_data'),
    path('graph/', views.GraphListView.as_view(), name='graph_list'),
    path('graph/<int:graph_id>/', views.GraphDetailView.as_view(), name='graph_detail'),
    path('graph/<int:graph_id>/data/', views.GraphDataView.as_view(), name='graph_data'),
    path('graph/<int:graph_id>/dataset/', views.GraphDatasetListView.as_view(), name='graph_dataset_list'),
    path('graph/<int:graph_id>/dataset/<int:dataset_id>/', views.GraphDatasetDetailView.as_view(), name='graph_dataset_detail')
]