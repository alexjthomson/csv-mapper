from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Dashboard view:
@login_required
def dashboard_view(request):
    """
    Displays the application dashboard.
    """

    graphs = []
    view_data = {
        'graphs': graphs
    }
    return render(request, 'dashboard.html', view_data)

def graphs_view(request):
    return render(request, 'graphs.html')

def sources_view(request):
    return render(request, 'sources.html')