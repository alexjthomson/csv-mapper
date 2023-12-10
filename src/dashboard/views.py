from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Dashboard view:
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def graphs_view(request):
    return render(request, 'graphs.html')

def sources_view(request):
    return render(request, 'sources.html')