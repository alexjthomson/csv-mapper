from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from .forms import RegisterForm

def register(request):
    # Check if POST data was sent to the view:
    if request.method == 'POST':
        # Construct a new registration form from the POST request data:
        form = RegisterForm(request.POST)
        # Validate that the form data is valid. This is also done in the clients
        # browser; however, client-side validation is never a secure way of
        # validating data since the user can craft a POST request to bypass
        # client-side validation:
        if form.is_valid():
            # The form fields are valid. We can now create a new user:
            user = form.save()
            # We can now login the user:
            login(request, user)
            # We should redirect the user to the dashboard:
            return redirect('/dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', { 'form': form })