from django import forms
from .models import Move, Bank, Concept
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if 'date' not in self.initial:  
            self.initial['date'] = now().date()
        if self.user:
            self.fields['bank'].queryset = Bank.objects.filter(usuario=self.user)
            self.fields['concept'].queryset = Concept.objects.filter(usuario=self.user)
        else:
            self.fields['bank'].queryset = Bank.objects.none()
            self.fields['concept'].queryset = Concept.objects.none()            