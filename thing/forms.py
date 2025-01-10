from django import forms
from .models import Thing


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ['code', 'description']
        labels = {
            'code': 'Código',
            'description': 'Descripción'            
        }
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código',
            })
        }
