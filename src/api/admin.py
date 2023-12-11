from django.contrib import admin
from .models import Source, Graph, GraphDataset

admin.site.register(Source)
admin.site.register(Graph)
admin.site.register(GraphDataset)