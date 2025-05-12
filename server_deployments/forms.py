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