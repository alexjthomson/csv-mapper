from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def login_view(request):
    # Check if the user is currently logged in, if they are, we should log them
    # out:
    if request.user.is_authenticated:
        return redirect('/account/logout')

    # Check if POST data was sent to the view:
    if request.method == 'POST':
        # Construct a new authentication form from the POST request data:
        form = AuthenticationForm(request, data=request.POST)
        # Validate that the form data is valid, we can then create the user:
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', { 'form': form })

@login_required
def logout_view(request):
    logout(request)
    return redirect('/account/login')

def register_view(request):
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
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', { 'form': form })