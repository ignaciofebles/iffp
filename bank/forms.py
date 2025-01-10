from django import forms
from .models import Bank

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['description']  # Incluye solo los campos que quieres en el formulario
        labels = {
            'description': 'Descripción',  # Etiqueta personalizada
        }
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del banco',
            }),
        }

