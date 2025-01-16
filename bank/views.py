from django.shortcuts import render, redirect
from bank.models import Bank
from move.models import Move
from .forms import BankForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum


# Create your views here.
def bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.usuario = request.user
            bank.save()
            return redirect('banks_list')         
    else:
        form = BankForm()
    return render(request, 'bank.html', {'form': form})



def banks_list(request):    
    banks = Bank.objects.filter(usuario=request.user).order_by('description')
    for banco in banks:
        ingresos = Move.objects.filter(bank=banco, concept__type='IN').aggregate(total=Sum('amount'))['total'] or 0
        egresos = Move.objects.filter(bank=banco, concept__type='EG').aggregate(total=Sum('amount'))['total'] or 0
        banco.saldo = ingresos - egresos  # Agregar saldo como atributo temporal
    return render(request, 'banks_list.html', {'banks': banks})

# def bancos_list(request):
#     bancos = Banco.objects.filter(usuario=request.user)
#     for banco in bancos:
#         ingresos = Move.objects.filter(bank=banco, concept__tipo='ingreso').aggregate(total=Sum('amount'))['total'] or 0
#         egresos = Move.objects.filter(bank=banco, concept__tipo='egreso').aggregate(total=Sum('amount'))['total'] or 0
#         banco.saldo = ingresos - egresos  # Agregar saldo como atributo temporal
#     return render(request, 'bancos_list.html', {'bancos': bancos})


class BankEditView(UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'bank.html'
    success_url = reverse_lazy('banks_list')


class BankDeleteView(DeleteView):
    model = Bank
    template_name = 'bank_confirm_delete.html'
    success_url = reverse_lazy('banks_list') 

    