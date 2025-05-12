from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

def home(request):
    # Handle all forms
    forms = {
        'cpu_form': CPUForm(prefix='cpu'),
        'ram_form': RAMForm(prefix='ram'),
        'motherboard_form': MotherboardForm(prefix='mb'),
        'nic_form': NICForm(prefix='nic'),
        'psu_form': PSUForm(prefix='psu'),
        'case_form': CaseForm(prefix='case'),
        'rack_form': RackForm(prefix='rack'),
        'system_form': SystemForm(prefix='system'),
        'storage_device_form': StorageDeviceForm(prefix='sd')
    }

    if request.method == 'POST':
        # Check which form was submitted
        if 'cpu-submit' in request.POST:
            forms['cpu_form'] = CPUForm(request.POST, prefix='cpu')
            if forms['cpu_form'].is_valid():
                forms['cpu_form'].save()
                return redirect('home')
        elif 'ram-submit' in request.POST:
            forms['ram_form'] = RAMForm(request.POST, prefix='ram')
            if forms['ram_form'].is_valid():
                forms['ram_form'].save()
                return redirect('home')
        elif 'mb-submit' in request.POST:
            forms['motherboard_form'] = MotherboardForm(request.POST, prefix='mb')
            if forms['motherboard_form'].is_valid():
                forms['motherboard_form'].save()
                return redirect('home')
        elif 'nic-submit' in request.POST:
            forms['nic_form'] = NICForm(request.POST, prefix='nic')
            if forms['nic_form'].is_valid():
                forms['nic_form'].save()
                return redirect('home')
        elif 'psu-submit' in request.POST:
            forms['psu_form'] = PSUForm(request.POST, prefix='psu')
            if forms['psu_form'].is_valid():
                forms['psu_form'].save()
                return redirect('home')
        elif 'case-submit' in request.POST:
            forms['case_form'] = CaseForm(request.POST, prefix='case')
            if forms['case_form'].is_valid():
                forms['case_form'].save()
                return redirect('home')
        elif 'rack-submit' in request.POST:
            forms['rack_form'] = RackForm(request.POST, prefix='rack')
            if forms['rack_form'].is_valid():
                forms['rack_form'].save()
                return redirect('home')
        elif 'system-submit' in request.POST:
            forms['system_form'] = SystemForm(request.POST, prefix='system')
            if forms['system_form'].is_valid():
                forms['system_form'].save()
                return redirect('home')


    systems = System.objects.all().prefetch_related('storage_devices')
    for system in systems:
        # RAM line total
        system.ram_line_total = (system.ram.price_each * system.ram_qty) if system.ram and system.ram.price_each else 0
        # Storage line totals
        system.storage_line_totals = [
            sd.price_each for sd in system.storage_devices.all() if sd.price_each
        ]
        # Calculate total price for all components
        system.total_price = (
            (system.cpu.price_each if system.cpu and system.cpu.price_each else 0) +
            system.ram_line_total +
            (system.motherboard.price_each if system.motherboard and system.motherboard.price_each else 0) +
            sum(system.storage_line_totals) +
            (system.nic.price_each if system.nic and system.nic.price_each else 0) +
            (system.psu.price_each if system.psu and system.psu.price_each else 0) +
            (system.case.price_each if system.case and system.case.price_each else 0)
        )

    return render(request, 'server_deployments/home.html', {
        **forms,
        'systems': systems,
    })

def edit_system(request, pk):
    system = get_object_or_404(System, pk=pk)
    if request.method == 'POST':
        form = SystemForm(request.POST, instance=system, prefix='system')
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SystemForm(instance=system, prefix='system')
    return render(request, 'server_deployments/edit_system.html', {'form': form, 'system': system})