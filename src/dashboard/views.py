from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Dashboard view:
@login_required
def dashboard(request):
    # Get the currently logged-in user:
    current_user = request.user

    graphs = []
    view_data = {
        "username": current_user.username,
        "graphs": graphs
    }
    return render(request, 'dashboard.html', view_data)