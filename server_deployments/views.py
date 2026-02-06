from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *
from django.utils.timezone import now
from django.core.paginator import Paginator
from datetime import timedelta
from django.db.models import Q, Count, Sum
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
import os


@login_required
def home(request):
    return render(request, 'server_deployments/home.html')

@login_required
def systems(request):
    return render(request, 'server_deployments/home.html')


@login_required
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

@login_required
def add_cpu(request):
    if request.method == 'POST':
        form = CPUForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_cpu(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    if request.method == 'POST':
        form = CPUForm(request.POST, instance=cpu)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={cpu_id}&type=cpu&tab=cpu-tab')

@login_required
def delete_cpu(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    if request.method == 'POST':
        cpu.delete()
    return redirect('components')

@login_required
def add_ram(request):
    if request.method == 'POST':
        form = RAMForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_ram(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    if request.method == 'POST':
        form = RAMForm(request.POST, instance=ram)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={ram_id}&type=ram&tab=ram-tab')

@login_required
def delete_ram(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    if request.method == 'POST':
        ram.delete()
    return redirect('components')


# Motherboard CRUD operations
@login_required
def add_motherboard(request):
    if request.method == 'POST':
        form = MotherboardForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_motherboard(request, motherboard_id):
    motherboard = get_object_or_404(Motherboard, id=motherboard_id)
    if request.method == 'POST':
        form = MotherboardForm(request.POST, instance=motherboard)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={motherboard_id}&type=motherboard&tab=motherboard-tab')

@login_required
def delete_motherboard(request, motherboard_id):
    motherboard = get_object_or_404(Motherboard, id=motherboard_id)
    if request.method == 'POST':
        motherboard.delete()
    return redirect('components')


# NIC CRUD operations
@login_required
def add_nic(request):
    if request.method == 'POST':
        form = NICForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_nic(request, nic_id):
    nic = get_object_or_404(NIC, id=nic_id)
    if request.method == 'POST':
        form = NICForm(request.POST, instance=nic)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={nic_id}&type=nic&tab=nic-tab')

@login_required
def delete_nic(request, nic_id):
    nic = get_object_or_404(NIC, id=nic_id)
    if request.method == 'POST':
        nic.delete()
    return redirect('components')


# PSU CRUD operations
@login_required
def add_psu(request):
    if request.method == 'POST':
        form = PSUForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_psu(request, psu_id):
    psu = get_object_or_404(PSU, id=psu_id)
    if request.method == 'POST':
        form = PSUForm(request.POST, instance=psu)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={psu_id}&type=psu&tab=psu-tab')

@login_required
def delete_psu(request, psu_id):
    psu = get_object_or_404(PSU, id=psu_id)
    if request.method == 'POST':
        psu.delete()
    return redirect('components')


# Case CRUD operations
@login_required
def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={case_id}&type=case&tab=case-tab')

@login_required
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        case.delete()
    return redirect('components')


# Storage CRUD operations
@login_required
def add_storage(request):
    if request.method == 'POST':
        form = StorageDeviceForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_storage(request, storage_id):
    storage = get_object_or_404(StorageDevice, id=storage_id)
    if request.method == 'POST':
        form = StorageDeviceForm(request.POST, instance=storage)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={storage_id}&type=storage&tab=storage-tab')

@login_required
def delete_storage(request, storage_id):
    storage = get_object_or_404(StorageDevice, id=storage_id)
    if request.method == 'POST':
        storage.delete()
    return redirect('components')

# HBA CRUD operations
@login_required
def add_hba(request):
    if request.method == 'POST':
        form = HBAForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_hba(request, hba_id):
    hba = get_object_or_404(HBA, id=hba_id)
    if request.method == 'POST':
        form = HBAForm(request.POST, instance=hba)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={hba_id}&type=hba&tab=hba-tab')

@login_required
def delete_hba(request, hba_id):
    hba = get_object_or_404(HBA, id=hba_id)
    if request.method == 'POST':
        hba.delete()
    return redirect('components')


# GPU CRUD operations
@login_required
def add_gpu(request):
    if request.method == 'POST':
        form = GPUForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_gpu(request, gpu_id):
    gpu = get_object_or_404(GPU, id=gpu_id)
    if request.method == 'POST':
        form = GPUForm(request.POST, instance=gpu)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={gpu_id}&type=gpu&tab=gpu-tab')

@login_required
def delete_gpu(request, gpu_id):
    gpu = get_object_or_404(GPU, id=gpu_id)
    if request.method == 'POST':
        gpu.delete()
    return redirect('components')


# Rack CRUD operations
@login_required
def add_rack(request):
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('components')

@login_required
def edit_rack(request, rack_id):
    rack = get_object_or_404(Rack, id=rack_id)
    if request.method == 'POST':
        form = RackForm(request.POST, instance=rack)
        if form.is_valid():
            form.save()
            return redirect('components')
    return redirect(f'/components/?edit={rack_id}&type=rack&tab=rack-tab')

@login_required
def delete_rack(request, rack_id):
    rack = get_object_or_404(Rack, id=rack_id)
    if request.method == 'POST':
        rack.delete()
    return redirect('components')


@login_required
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


@login_required
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
        disk_number = request.POST.get('disk_number')
        disk_position = request.POST.get('disk_position')
        utilisation = request.POST.get('utilisation', 0)
        fragmentation = request.POST.get('fragmentation')
        actual_fragmentation = request.POST.get('actual_fragmentation')
        ideal_fragmentation = request.POST.get('ideal_fragmentation')
        free_space_gb = request.POST.get('free_space_gb')
        system_id = request.POST.get('system')
        
        # Calculate fragmentation percentage if actual and ideal fragmentation are provided
        if actual_fragmentation and ideal_fragmentation and int(actual_fragmentation) > 0:
            calculated_fragmentation = round((1 - (int(ideal_fragmentation) / int(actual_fragmentation))) * 100, 2)
        else:
            calculated_fragmentation = float(fragmentation) if fragmentation else None
        
        # Calculate free space or utilisation
        final_free_space_gb = None
        final_utilisation = float(utilisation) if utilisation else 0
        
        if capacity_tb:
            total_gb = float(capacity_tb) * 1000
            if free_space_gb:
                # If free space is manually set, recalculate utilisation
                used_gb = total_gb - float(free_space_gb)
                if total_gb > 0:
                    final_utilisation = round((used_gb / total_gb) * 100, 2)
                final_free_space_gb = int(free_space_gb)
            else:
                # Calculate free space from utilisation
                used_gb = total_gb * (final_utilisation / 100)
                final_free_space_gb = int(total_gb - used_gb)
        
        # Create and save the storage device
        storage = StorageDevice.objects.create(
            model=model,
            serial_number=serial_number,
            storage_type=storage_type,
            storage_sub_type=storage_sub_type,
            capacity_tb=float(capacity_tb) if capacity_tb else 0,
            rpm=int(rpm) if rpm else None,
            disk_number=int(disk_number) if disk_number else None,
            disk_position=int(disk_position) if disk_position else None,
            utilisation=final_utilisation,
            fragmentation=calculated_fragmentation,
            actual_fragmentation=int(actual_fragmentation) if actual_fragmentation else None,
            ideal_fragmentation=int(ideal_fragmentation) if ideal_fragmentation else None,
            fragmentation_last_updated=now() if (actual_fragmentation or ideal_fragmentation) else None,
            free_space_gb=final_free_space_gb
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
    
    # Calculate server summary statistics - ONLY drives with disk_number (data drives)
    data_drives = StorageDevice.objects.filter(disk_number__isnull=False)
    
    # Overall statistics for data drives only
    total_capacity = sum(drive.capacity_tb for drive in data_drives)
    total_used = sum((drive.capacity_tb * drive.utilisation / 100) for drive in data_drives)
    overall_utilization = (total_used / total_capacity * 100) if total_capacity > 0 else 0
    
    # CMR data drives (drives with disk numbers)
    cmr_data_drives = data_drives.filter(storage_sub_type__iexact='CMR')
    cmr_total_capacity = sum(drive.capacity_tb for drive in cmr_data_drives)
    cmr_total_used = sum((drive.capacity_tb * drive.utilisation / 100) for drive in cmr_data_drives)
    cmr_utilization = (cmr_total_used / cmr_total_capacity * 100) if cmr_total_capacity > 0 else 0
    
    # SMR data drives (drives with disk numbers)
    smr_data_drives = data_drives.filter(storage_sub_type__iexact='SMR')
    smr_total_capacity = sum(drive.capacity_tb for drive in smr_data_drives)
    smr_total_used = sum((drive.capacity_tb * drive.utilisation / 100) for drive in smr_data_drives)
    smr_utilization = (smr_total_used / smr_total_capacity * 100) if smr_total_capacity > 0 else 0
    
    # Storage type breakdown for data drives only
    storage_types = {}
    for drive in data_drives:
        storage_type = drive.storage_type
        if storage_type not in storage_types:
            storage_types[storage_type] = {'count': 0, 'capacity': 0, 'used': 0}
        storage_types[storage_type]['count'] += 1
        storage_types[storage_type]['capacity'] += drive.capacity_tb
        storage_types[storage_type]['used'] += (drive.capacity_tb * drive.utilisation / 100)
    
    # Add utilization percentage and free space to storage types
    for storage_type in storage_types:
        if storage_types[storage_type]['capacity'] > 0:
            storage_types[storage_type]['utilization'] = (
                storage_types[storage_type]['used'] / 
                storage_types[storage_type]['capacity'] * 100
            )
        else:
            storage_types[storage_type]['utilization'] = 0
        storage_types[storage_type]['free'] = round(
            storage_types[storage_type]['capacity'] - storage_types[storage_type]['used'], 2
        )
    
    # Failing drives count for data drives only
    failing_drives_count = data_drives.filter(failure=True).count()
    
    # Create summary dictionary
    server_summary = {
        'total_drives': data_drives.count(),
        'total_capacity_tb': round(total_capacity, 2),
        'total_used_tb': round(total_used, 2),
        'total_free_tb': round(total_capacity - total_used, 2),
        'overall_utilization': round(overall_utilization, 2),
        'failing_drives_count': failing_drives_count,
        'cmr_data': {
            'count': cmr_data_drives.count(),
            'capacity': round(cmr_total_capacity, 2),
            'used': round(cmr_total_used, 2),
            'free': round(cmr_total_capacity - cmr_total_used, 2),
            'utilization': round(cmr_utilization, 2),
        },
        'smr_data': {
            'count': smr_data_drives.count(),
            'capacity': round(smr_total_capacity, 2),
            'used': round(smr_total_used, 2),
            'free': round(smr_total_capacity - smr_total_used, 2),
            'utilization': round(smr_utilization, 2),
        },
        'storage_types': storage_types,
    }
    
    for system in systems:
        # Get all drives for this system
        drives = list(system.storage_devices.all())
        
        # Add disk_display_value and calculate fragmentation for each drive
        for drive in drives:
            # Use stored fragmentation percentage
            drive.calculated_fragmentation = drive.fragmentation
            
            # Calculate fragmentation difference
            if drive.actual_fragmentation and drive.ideal_fragmentation:
                drive.fragmentation_difference = drive.actual_fragmentation - drive.ideal_fragmentation
            else:
                drive.fragmentation_difference = None
                
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
                    'text': str(drive.disk_number) if drive.disk_number else '-',
                    'class': ''
                }

        # Custom sorting: None disk_numbers at top, then by disk_number
        def drive_sort_key(drive):
            if drive.disk_number is None:
                return (0, 0)  # Tuple for sorting: (priority, disk_number)
            return (1, drive.disk_number)
        
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
    
    # Separate failed drives that aren't in any system
    failed_drives = []
    active_misc_drives = []
    
    for drive in misc_drives:
        # Use stored fragmentation percentage
        drive.calculated_fragmentation = drive.fragmentation
            
        # Calculate fragmentation difference
        if drive.actual_fragmentation and drive.ideal_fragmentation:
            drive.fragmentation_difference = drive.actual_fragmentation - drive.ideal_fragmentation
        else:
            drive.fragmentation_difference = None
            
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
                'text': str(drive.disk_number) if drive.disk_number else '-',
                'class': ''
            }
        
        # Separate failed drives from active misc drives
        if drive.failure:
            failed_drives.append(drive)
        else:
            active_misc_drives.append(drive)
    
    return render(request, "server_deployments/storage_view.html", {
        "systems_with_drives": systems_with_ordered_drives,
        "misc_drives": active_misc_drives,
        "failed_drives": failed_drives,
        "systems": systems,  # For the dropdown in the add form
        "server_summary": server_summary,
    })


@login_required
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


@login_required
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
            # Calculate and save fragmentation percentage
            new_actual = form.cleaned_data.get('actual_fragmentation')
            new_ideal = form.cleaned_data.get('ideal_fragmentation')
            if new_actual and new_ideal and new_actual > 0:
                calculated_fragmentation = round((1 - (new_ideal / new_actual)) * 100, 2)
                form.instance.fragmentation = calculated_fragmentation
            else:
                form.instance.fragmentation = None
            
            # Calculate and save free space in GB or recalculate utilisation if free space is provided
            capacity_tb = form.cleaned_data.get('capacity_tb')
            utilisation = form.cleaned_data.get('utilisation')
            free_space_gb = form.cleaned_data.get('free_space_gb')
            
            if capacity_tb:
                total_gb = capacity_tb * 1000
                if free_space_gb is not None:
                    # If free space is manually set, recalculate utilisation
                    used_gb = total_gb - free_space_gb
                    if total_gb > 0:
                        calculated_utilisation = round((used_gb / total_gb) * 100, 2)
                        form.instance.utilisation = calculated_utilisation
                    form.instance.free_space_gb = free_space_gb
                elif utilisation is not None:
                    # If utilisation is set, calculate free space
                    used_gb = total_gb * (utilisation / 100)
                    free_gb = total_gb - used_gb
                    form.instance.free_space_gb = int(free_gb)
                else:
                    form.instance.free_space_gb = None
            else:
                form.instance.free_space_gb = None
            
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
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            # Redirect back to storage view
            return redirect('storage_view')
    else:
        # Check if this is an AJAX request for data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'model': storage.model,
                'serial_number': storage.serial_number,
                'storage_type': storage.storage_type,
                'storage_sub_type': storage.storage_sub_type,
                'capacity_tb': storage.capacity_tb,
                'disk_number': storage.disk_number,
                'disk_position': storage.disk_position,
                'rpm': storage.rpm,
                'utilisation': storage.utilisation,
                'free_space_gb': storage.free_space_gb,
                'fragmentation': storage.fragmentation,
                'actual_fragmentation': storage.actual_fragmentation,
                'ideal_fragmentation': storage.ideal_fragmentation,
                'cache': storage.cache,
                'parity': storage.parity,
                'failure': storage.failure,
                'system_id': current_system.id if current_system else None,
            })
        
        form = StorageDeviceForm(instance=storage)
    
    # Render the form (fallback for non-AJAX requests)
    return render(request, 'server_deployments/edit_storage.html', {
        'form': form,
        'storage': storage,
        'title': 'Edit Storage Device',
        'systems': System.objects.all(),
        'current_system': current_system
    })


@login_required
def delete_storage(request, storage_id):
    storage = get_object_or_404(StorageDevice, id=storage_id)
    
    if request.method == 'POST':
        # Remove from any systems first
        for system in System.objects.all():
            if storage in system.storage_devices.all():
                system.storage_devices.remove(storage)
        
        # Delete the storage device
        storage.delete()
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        return redirect('storage_view')
    
    # For GET requests, redirect to storage view
    return redirect('storage_view')

# Django Guides Views
@login_required
def django_guides(request):
    """Main page showing all Django guides"""
    guides = DjangoGuide.objects.all()
    return render(request, 'server_deployments/django_guides.html', {
        'guides': guides
    })


@login_required
def django_guide_detail(request, slug):
    """Detail page for a specific guide showing all steps"""
    guide = get_object_or_404(DjangoGuide, slug=slug)
    steps = guide.steps.all()
    all_guides = DjangoGuide.objects.all()
    
    return render(request, 'server_deployments/django_guide_detail.html', {
        'guide': guide,
        'steps': steps,
        'all_guides': all_guides
    })


@login_required
def django_step_add(request, guide_slug):
    """Add a new step to a guide"""
    guide = get_object_or_404(DjangoGuide, slug=guide_slug)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        step_type = request.POST.get('step_type', 'section')
        order = request.POST.get('order', 0)
        
        DjangoStep.objects.create(
            guide=guide,
            title=title,
            content=content,
            step_type=step_type,
            order=order
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        return redirect('django_guide_detail', slug=guide_slug)
    
    return redirect('django_guide_detail', slug=guide_slug)


@login_required
def django_step_edit(request, step_id):
    """Edit an existing step"""
    step = get_object_or_404(DjangoStep, id=step_id)
    
    if request.method == 'POST':
        step.title = request.POST.get('title', step.title)
        step.content = request.POST.get('content', step.content)
        step.step_type = request.POST.get('step_type', step.step_type)
        step.order = request.POST.get('order', step.order)
        step.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        return redirect('django_guide_detail', slug=step.guide.slug)
    
    # Return step data for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'id': step.id,
            'title': step.title,
            'content': step.content,
            'step_type': step.step_type,
            'order': step.order
        })
    
    return redirect('django_guide_detail', slug=step.guide.slug)


@login_required
def django_step_delete(request, step_id):
    """Delete a step"""
    step = get_object_or_404(DjangoStep, id=step_id)
    guide_slug = step.guide.slug
    
    if request.method == 'POST':
        step.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        return redirect('django_guide_detail', slug=guide_slug)
    
    return redirect('django_guide_detail', slug=guide_slug)


@login_required
def django_step_reorder(request):
    """Update step orders via AJAX"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        import json
        data = json.loads(request.body)
        
        for item in data.get('steps', []):
            step_id = item.get('id')
            new_order = item.get('order')
            if step_id and new_order is not None:
                DjangoStep.objects.filter(id=step_id).update(order=new_order)
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)
