from django.shortcuts import render, redirect, get_object_or_404
from .models import System, Component

def home(request):

    return render(request, 'server_deployments/home.html')
