from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


def home(request):
    return render(request, 'server_deployments/home.html')


def components(request):
    """View for displaying and adding components"""
    # Get all component types
    cpus = CPU.objects.all()
    rams = RAM.objects.all()
    motherboards = Motherboard.objects.all()
    nics = NIC.objects.all()
    psus = PSU.objects.all()
    cases = Case.objects.all()
    storage_devices = StorageDevice.objects.all()
    hba_devices = HBA.objects.all()
    racks = Rack.objects.all()
    
    # Create forms for each component type
    cpu_form = CPUForm()
    ram_form = RAMForm()
    motherboard_form = MotherboardForm()
    nic_form = NICForm()
    psu_form = PSUForm()
    case_form = CaseForm()
    storage_form = StorageDeviceForm()
    hba_form = HBAForm()
    rack_form = RackForm()
    
    # Check if we're in edit mode
    edit_mode = False
    edit_id = None
    component_type = None
    
    # Check for edit parameters in the URL
    if request.GET.get('edit'):
        edit_id = request.GET.get('edit')
        component_type = request.GET.get('type', 'cpu')  # Default to CPU if not specified
        edit_mode = True
        
        # Based on component type, get the correct instance and form
        if component_type == 'cpu':
            cpu = get_object_or_404(CPU, id=edit_id)
            cpu_form = CPUForm(instance=cpu)
        elif component_type == 'ram':
            ram = get_object_or_404(RAM, id=edit_id)
            ram_form = RAMForm(instance=ram)
        elif component_type == 'motherboard':
            motherboard = get_object_or_404(Motherboard, id=edit_id)
            motherboard_form = MotherboardForm(instance=motherboard)
        elif component_type == 'nic':
            nic = get_object_or_404(NIC, id=edit_id)
            nic_form = NICForm(instance=nic)
        elif component_type == 'psu':
            psu = get_object_or_404(PSU, id=edit_id)
            psu_form = PSUForm(instance=psu)
        elif component_type == 'case':
            case = get_object_or_404(Case, id=edit_id)
            case_form = CaseForm(instance=case)
        elif component_type == 'storage':
            storage = get_object_or_404(StorageDevice, id=edit_id)
            storage_form = StorageDeviceForm(instance=storage)
        elif component_type == 'rack':
            rack = get_object_or_404(Rack, id=edit_id)
            rack_form = RackForm(instance=rack)
    
    context = {
        # All component data
        'cpus': cpus,
        'rams': rams,
        'motherboards': motherboards,
        'nics': nics,
        'psus': psus,
        'cases': cases,
        'storage_devices': storage_devices,
        'hba_devices': hba_devices,
        'racks': racks,
        
        # All forms
        'cpu_form': cpu_form,
        'ram_form': ram_form,
        'motherboard_form': motherboard_form,
        'nic_form': nic_form,
        'psu_form': psu_form,
        'case_form': case_form,
        'storage_form': storage_form,
        'hba_form': hba_form,
        'rack_form': rack_form,
        
        # Edit mode info
        'edit_mode': edit_mode,
        'edit_id': edit_id,
        'component_type': component_type
    }
    
    return render(request, 'server_deployments/components.html', context)

def add_cpu(request):
    if request.method == 'POST':
        form = CPUForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_cpu(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    if request.method == 'POST':
        form = CPUForm(request.POST, instance=cpu)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={cpu_id}&type=cpu&tab=cpu-tab')

def delete_cpu(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    if request.method == 'POST':
        cpu.delete()
    return redirect('components')

def add_ram(request):
    if request.method == 'POST':
        form = RAMForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_ram(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    if request.method == 'POST':
        form = RAMForm(request.POST, instance=ram)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={ram_id}&type=ram&tab=ram-tab')

def delete_ram(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    if request.method == 'POST':
        ram.delete()
    return redirect('components')


# Motherboard CRUD operations
def add_motherboard(request):
    if request.method == 'POST':
        form = MotherboardForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_motherboard(request, motherboard_id):
    motherboard = get_object_or_404(Motherboard, id=motherboard_id)
    if request.method == 'POST':
        form = MotherboardForm(request.POST, instance=motherboard)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={motherboard_id}&type=motherboard&tab=motherboard-tab')

def delete_motherboard(request, motherboard_id):
    motherboard = get_object_or_404(Motherboard, id=motherboard_id)
    if request.method == 'POST':
        motherboard.delete()
    return redirect('components')


# NIC CRUD operations
def add_nic(request):
    if request.method == 'POST':
        form = NICForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_nic(request, nic_id):
    nic = get_object_or_404(NIC, id=nic_id)
    if request.method == 'POST':
        form = NICForm(request.POST, instance=nic)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={nic_id}&type=nic&tab=nic-tab')

def delete_nic(request, nic_id):
    nic = get_object_or_404(NIC, id=nic_id)
    if request.method == 'POST':
        nic.delete()
    return redirect('components')


# PSU CRUD operations
def add_psu(request):
    if request.method == 'POST':
        form = PSUForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_psu(request, psu_id):
    psu = get_object_or_404(PSU, id=psu_id)
    if request.method == 'POST':
        form = PSUForm(request.POST, instance=psu)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={psu_id}&type=psu&tab=psu-tab')

def delete_psu(request, psu_id):
    psu = get_object_or_404(PSU, id=psu_id)
    if request.method == 'POST':
        psu.delete()
    return redirect('components')


# Case CRUD operations
def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={case_id}&type=case&tab=case-tab')

def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        case.delete()
    return redirect('components')


# Storage CRUD operations
def add_storage(request):
    if request.method == 'POST':
        form = StorageDeviceForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_storage(request, storage_id):
    storage = get_object_or_404(StorageDevice, id=storage_id)
    if request.method == 'POST':
        form = StorageDeviceForm(request.POST, instance=storage)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={storage_id}&type=storage&tab=storage-tab')

def delete_storage(request, storage_id):
    storage = get_object_or_404(StorageDevice, id=storage_id)
    if request.method == 'POST':
        storage.delete()
    return redirect('components')

# HBA CRUD operations
def add_hba(request):
    if request.method == 'POST':
        form = HBAForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_hba(request, hba_id):
    hba = get_object_or_404(HBA, id=hba_id)
    if request.method == 'POST':
        form = HBAForm(request.POST, instance=hba)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={hba_id}&type=hba&tab=hba-tab')

def delete_hba(request, hba_id):
    hba = get_object_or_404(HBA, id=hba_id)
    if request.method == 'POST':
        hba.delete()
    return redirect('components')


# Rack CRUD operations
def add_rack(request):
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_rack(request, rack_id):
    rack = get_object_or_404(Rack, id=rack_id)
    if request.method == 'POST':
        form = RackForm(request.POST, instance=rack)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={rack_id}&type=rack&tab=rack-tab')

def delete_rack(request, rack_id):
    rack = get_object_or_404(Rack, id=rack_id)
    if request.method == 'POST':
        rack.delete()
    return redirect('components')


def databases(request):
    return render(request, 'server_deployments/databases.html')

