from django.shortcuts import render, redirect, get_object_or_404
from .models import System, Component
from .forms import SystemForm, ComponentForm

def home(request):
    systems = System.objects.prefetch_related('components').all()
    components = Component.objects.all()
    return render(request, 'server_deployments/home.html', {
        'systems': systems,
        'components': components,
        'system_form': SystemForm(),
        'component_form': ComponentForm(),
    })

def add_system(request):
    if request.method == 'POST':
        form = SystemForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('home')

def add_component(request):
    if request.method == 'POST':
        form = ComponentForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('home')