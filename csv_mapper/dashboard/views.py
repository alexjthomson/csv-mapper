from django.shortcuts import render, HttpResponse

# Dashboard view:
def dashboard(request):
    return render(request, 'dashboard.html')