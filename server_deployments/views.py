from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


def home(request):
    return render(request, 'server_deployments/home.html')


def components(request):
    """View for displaying and adding components"""
    cpus = CPU.objects.all()
    form = CPUForm()
    
    # Check if we're in edit mode
    edit_mode = False
    edit_id = None
    
    if request.GET.get('edit'):
        edit_id = request.GET.get('edit')
        edit_mode = True
        cpu = get_object_or_404(CPU, id=edit_id)
        form = CPUForm(instance=cpu)
    
    context = {
        'cpus': cpus,
        'form': form,
        'edit_mode': edit_mode,
        'edit_id': edit_id
    }
    return render(request, 'server_deployments/components.html', context)

def add_cpu(request):
    if request.method == 'POST':
        form = CPUForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect('components')

def edit_cpu(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    if request.method == 'POST':
        form = CPUForm(request.POST, instance=cpu)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={cpu_id}')


def delete_cpu(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    if request.method == 'POST':
        cpu.delete()
        return redirect('components')
    return redirect('components')


def databases(request):
    return render(request, 'server_deployments/databases.html')

