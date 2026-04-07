from django import forms
from .models import *

class CPUForm(forms.ModelForm):
    class Meta:
        model = CPU
        fields = '__all__'

class RAMForm(forms.ModelForm):
    class Meta:
        model = RAM
        fields = '__all__'

class MotherboardForm(forms.ModelForm):
    class Meta:
        model = Motherboard
        fields = '__all__'

class NICForm(forms.ModelForm):
    class Meta:
        model = NIC
        fields = '__all__'

class GPUForm(forms.ModelForm):
    class Meta:
        model = GPU
        fields = '__all__'

class PSUForm(forms.ModelForm):
    class Meta:
        model = PSU
        fields = '__all__'

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'

class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = '__all__'

class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = '__all__'

class StorageDeviceForm(forms.ModelForm):
    class Meta:
        model = StorageDevice
        fields = '__all__'

class HBAForm(forms.ModelForm):
    class Meta:
        model = HBA
        fields = '__all__'

class DashboardLinkForm(forms.ModelForm):
    class Meta:
        model = DashboardLink
        fields = ['name', 'url', 'icon', 'category', 'tab', 'description', 'order', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Virgin Router'}),
            'url': forms.URLInput(attrs={'placeholder': 'http://192.168.1.1'}),
            'icon': forms.TextInput(attrs={'placeholder': 'icons/router.png'}),
            'description': forms.TextInput(attrs={'placeholder': '192.168.1.1'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }