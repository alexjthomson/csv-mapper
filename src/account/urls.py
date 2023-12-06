from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('sign-up', views.sign_up, name='sign_up')
]