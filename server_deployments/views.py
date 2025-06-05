from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


def home(request):
    return render(request, 'server_deployments/home.html')


def components(request):
    return render(request, 'server_deployments/components.html')


def databases(request):
    return render(request, 'server_deployments/databases.html')

