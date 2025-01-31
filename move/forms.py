from django import forms
from .models import Move, Bank, Concept
from django.utils import timezone
from shared.utils import get_bank_balance


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
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy'}),
            'comentary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un comentario'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bank': forms.Select(attrs={'class': 'form-control'}),
            'concept': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        # Inicializar la fecha con formato dd/mm/yyyy
        if not self.instance.pk and 'date' not in self.initial:
            today = timezone.now().date()
            self.fields['date'].initial = today.strftime('%d/%m/%Y')

        if user:
            # Filtrar los bancos por el usuario
            banks = Bank.objects.filter(usuario=user).order_by('description')

            # Crear una lista de tuplas con el nombre del banco y su saldo
            banks_with_balance = []
            for bank in banks:
                saldo = get_bank_balance(bank)  # Obtener saldo del banco
                banks_with_balance.append((bank.id, f"{bank.description},  (€ {saldo})"))

            # Asignar el queryset modificado a los campos del formulario
            self.fields['bank'].queryset = banks

            # Modificar el label para mostrar el nombre del banco y su saldo
            self.fields['bank'].choices = banks_with_balance

            self.fields['concept'].queryset = Concept.objects.filter(usuario=user).order_by('description')
        else:
            self.fields['bank'].queryset = Bank.objects.none()
            self.fields['concept'].queryset = Concept.objects.none()

