from django.shortcuts import render, redirect
from bank.models import Bank
from .forms import BankForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


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
    return render(request, 'banks_list.html', {'banks': banks})

class BankEditView(UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'bank.html'
    success_url = reverse_lazy('banks_list')


class BankDeleteView(DeleteView):
    model = Bank
    template_name = 'bank_confirm_delete.html'
    success_url = reverse_lazy('banks_list') 

    