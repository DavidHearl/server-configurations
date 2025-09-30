from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.utils.timezone import now
from django.core.paginator import Paginator
from datetime import timedelta
from django.db.models import Q, Count, Sum
from django.utils.timezone import now
import os


def home(request):
    return render(request, 'server_deployments/home.html')

def systems(request):
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
    gpus = GPU.objects.all()
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
    gpu_form = GPUForm()
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
        'gpus': gpus,
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
        'gpu_form': gpu_form,
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


# GPU CRUD operations
def add_gpu(request):
    if request.method == 'POST':
        form = GPUForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

def edit_gpu(request, gpu_id):
    gpu = get_object_or_404(GPU, id=gpu_id)
    if request.method == 'POST':
        form = GPUForm(request.POST, instance=gpu)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={gpu_id}&type=gpu&tab=gpu-tab')

def delete_gpu(request, gpu_id):
    gpu = get_object_or_404(GPU, id=gpu_id)
    if request.method == 'POST':
        gpu.delete()
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
    base_path = request.GET.get("base_path", "/mnt")
    folders = IndexedFolder.objects.filter(path__startswith=base_path).order_by("path")

    paginator = Paginator(folders, 250)
    page = request.GET.get("page", 1)
    paginated_folders = paginator.get_page(page)

    # Derive next subfolder options from current base_path
    subfolders = set()
    base_depth = len(base_path.strip("/").split("/"))
    for f in folders:
        parts = f.path.strip("/").split("/")
        if len(parts) > base_depth:
            subfolders.add(parts[base_depth])

    return render(request, "server_deployments/databases.html", {
        "folders": paginated_folders,
        "base_path": base_path,
        "subfolders": sorted(subfolders),
        "now": now(),
    })


def storage_view(request):
    # Handle form submission
    if request.method == 'POST':
        # Create new storage device
        model = request.POST.get('model')
        serial_number = request.POST.get('serial_number')
        storage_type = request.POST.get('storage_type')
        storage_sub_type = request.POST.get('storage_sub_type')
        capacity_tb = request.POST.get('capacity_tb')
        rpm = request.POST.get('rpm')
        disk_location = request.POST.get('disk_location')
        utilisation = request.POST.get('utilisation', 0)
        fragmentation = request.POST.get('fragmentation')
        actual_fragmentation = request.POST.get('actual_fragmentation')
        ideal_fragmentation = request.POST.get('ideal_fragmentation')
        system_id = request.POST.get('system')
        
        # Create and save the storage device
        storage = StorageDevice.objects.create(
            model=model,
            serial_number=serial_number,
            storage_type=storage_type,
            storage_sub_type=storage_sub_type,
            capacity_tb=float(capacity_tb) if capacity_tb else 0,
            rpm=int(rpm) if rpm else None,
            disk_location=int(disk_location) if disk_location else None,
            utilisation=float(utilisation) if utilisation else 0.0,
            fragmentation=float(fragmentation) if fragmentation else None,
            actual_fragmentation=int(actual_fragmentation) if actual_fragmentation else None,
            ideal_fragmentation=int(ideal_fragmentation) if ideal_fragmentation else None
        )
        
        # Assign to system if specified
        if system_id and system_id != '':
            try:
                system = System.objects.get(id=system_id)
                system.storage_devices.add(storage)
            except System.DoesNotExist:
                pass
                
        return redirect('storage_view')
    
    # Get all systems
    systems = System.objects.all().prefetch_related('storage_devices')
    
    # Create a system map with ordered drives
    systems_with_ordered_drives = []
    associated_storage_ids = []
    
    for system in systems:
        # Get all drives for this system
        drives = list(system.storage_devices.all())
        
        # Add disk_display_value and calculate fragmentation for each drive
        for drive in drives:
            # Calculate fragmentation percentage
            if drive.actual_fragmentation and drive.ideal_fragmentation and drive.ideal_fragmentation > 0:
                drive.calculated_fragmentation = round((1 - (drive.ideal_fragmentation / drive.actual_fragmentation)) * 100, 2)
            else:
                drive.calculated_fragmentation = None
                
            if drive.failure:
                drive.disk_display_value = {
                    'type': 'failing',
                    'text': 'Failing',
                    'class': 'disk-failing'
                }
            elif drive.cache:
                drive.disk_display_value = {
                    'type': 'cache',
                    'text': 'Cache',
                    'class': 'disk-cache'
                }
            elif drive.parity:
                drive.disk_display_value = {
                    'type': 'parity',
                    'text': 'Parity',
                    'class': 'disk-parity'
                }
            else:
                drive.disk_display_value = {
                    'type': 'number',
                    'text': str(drive.disk_location) if drive.disk_location else '-',
                    'class': ''
                }

        # Custom sorting: None disk_numbers at top, then by disk_number
        def drive_sort_key(drive):
            if drive.disk_location is None:
                return (0, 0)  # Tuple for sorting: (priority, disk_number)
            return (1, drive.disk_location)
        
        # Sort the drives
        sorted_drives = sorted(drives, key=drive_sort_key)
        
        # Track all associated storage IDs
        associated_storage_ids.extend([drive.id for drive in drives])
        
        # Add to the result list
        systems_with_ordered_drives.append({
            'system': system,
            'drives': sorted_drives
        })
    
    # Get drives that aren't associated with any system and calculate fragmentation
    misc_drives = StorageDevice.objects.exclude(id__in=associated_storage_ids)
    for drive in misc_drives:
        # Calculate fragmentation percentage
        if drive.actual_fragmentation and drive.ideal_fragmentation and drive.ideal_fragmentation > 0:
            drive.calculated_fragmentation = round(((drive.actual_fragmentation - drive.ideal_fragmentation) / drive.ideal_fragmentation) * 100, 2)
        else:
            drive.calculated_fragmentation = None
            
        if drive.failure:
            drive.disk_display_value = {
                'type': 'failing',
                'text': 'Failing',
                'class': 'disk-failing'
            }
        elif drive.cache:
            drive.disk_display_value = {
                'type': 'cache',
                'text': 'Cache',
                'class': 'disk-cache'
            }
        elif drive.parity:
            drive.disk_display_value = {
                'type': 'parity',
                'text': 'Parity',
                'class': 'disk-parity'
            }
        else:
            drive.disk_display_value = {
                'type': 'number',
                'text': str(drive.disk_location) if drive.disk_location else '-',
                'class': ''
            }
    
    return render(request, "server_deployments/storage_view.html", {
        "systems_with_drives": systems_with_ordered_drives,
        "misc_drives": misc_drives,
        "systems": systems,  # For the dropdown in the add form
    })


def add_storage(request):
    system_id = request.GET.get('system')
    
    if request.method == 'POST':
        form = StorageDeviceForm(request.POST)
        if form.is_valid():
            storage = form.save()
            return redirect('storage_view')  # Redirect to storage view instead of components
    else:
        # Pre-select the system if passed in URL
        initial_data = {}
        if system_id:
            try:
                system = System.objects.get(pk=system_id)
                initial_data = {'system': system}
            except System.DoesNotExist:
                pass
                
        form = StorageDeviceForm(initial=initial_data)
    
    return render(request, 'server_deployments/add_storage.html', {
        'form': form,
        'title': 'Add Storage Device'
    })


def edit_storage(request, storage_id):
    storage = get_object_or_404(StorageDevice, id=storage_id)
    
    # Find the current system if any
    current_system = None
    for system in System.objects.all():
        if storage in system.storage_devices.all():
            current_system = system
            break
    
    if request.method == 'POST':
        form = StorageDeviceForm(request.POST, instance=storage)
        if form.is_valid():
            # Save the storage device
            storage = form.save()
            
            # Handle system assignment
            new_system_id = request.POST.get('system')
            
            # If the storage was in a system, remove it
            if current_system:
                current_system.storage_devices.remove(storage)
            
            # Add to new system if specified
            if new_system_id and new_system_id != '':
                try:
                    new_system = System.objects.get(id=new_system_id)
                    new_system.storage_devices.add(storage)
                except System.DoesNotExist:
                    pass
            
            # Redirect back to storage view
            return redirect('storage_view')
    else:
        form = StorageDeviceForm(instance=storage)
    
    # Render the form
    return render(request, 'server_deployments/edit_storage.html', {
        'form': form,
        'storage': storage,
        'title': 'Edit Storage Device',
        'systems': System.objects.all(),
        'current_system': current_system
    })