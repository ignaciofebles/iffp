from django import forms
from .models import Move, Bank, Concept
from django.utils import timezone

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
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'dd/mm/yyyy'
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
        user = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if not self.instance.pk and 'date' not in self.initial:
            self.fields['date'].initial = timezone.now().date()
            today = timezone.now().date()
            formatted_date = today.strftime('%d/%m/%Y')  # Formato 'dd/mm/yyyy'
            self.fields['date'].initial = formatted_date
        
        if user:
            self.fields['bank'].queryset = Bank.objects.filter(usuario=user).order_by('description')
            self.fields['concept'].queryset = Concept.objects.filter(usuario=user).order_by('description')
        else:
            self.fields['bank'].queryset = Bank.objects.none()
            self.fields['concept'].queryset = Concept.objects.none()            

            