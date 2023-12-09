from django.contrib import admin
from .models import Source, SourceColumnConfig, Graph, GraphDataset

admin.site.register(Source)
admin.site.register(SourceColumnConfig)
admin.site.register(Graph)
admin.site.register(GraphDataset)