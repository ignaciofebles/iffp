from django import forms
from .models import Move
from django.utils.timezone import now

class MoveForm(forms.ModelForm):
    class Meta:
        model = Move
        fields = ['date', 'comentary', 'amount', 'bank', 'concept']
        labels = {
            'date': 'Fecha',
            'comentary': 'Comentario',
            'amount': 'Monto',
            'bank': 'Banco',
            'concept': 'Concepto'
        }
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',

            }),
            'comentary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un comentario',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),
            'bank': forms.Select(attrs={
                'class': 'form-control',
            }),
            'concept': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

