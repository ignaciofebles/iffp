from django import forms
from .models import Concept


class ConceptForm(forms.ModelForm):
    class Meta:
        model = Concept
        fields = ['description', 'type', 'transfer']
        labels = {
            'description': 'Descripción',
            'type': 'Tipo',
            'transfer': 'Es transferencia'
        }
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del concepto',
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'transfer': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or len(description) < 3:
            raise forms.ValidationError("La descripción debe tener al menos 3 caracteres.")
        return description