from django import forms
from .models import System, Component

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['component_type', 'model', 'unit_price', 'link_justification']

class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = ['name', 'rack', 'size', 'components']
        widgets = {
            'components': forms.CheckboxSelectMultiple
        }