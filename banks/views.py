from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from bank.models import Bank
from move.models import Move

# Create your views here.
def banks_balance(request):    
    banks = Bank.objects.filter(usuario=request.user).order_by('description')
    for banco in banks:
        ingresos = Move.objects.filter(bank=banco, concept__type='IN').aggregate(total=Sum('amount'))['total'] or 0
        egresos = Move.objects.filter(bank=banco, concept__type='EG').aggregate(total=Sum('amount'))['total'] or 0
        banco.saldo = ingresos - egresos 
    total_balance = sum(bank.saldo for bank in banks)
    return render(request, 'banks_balance.html', {'banks': banks, 'total_balance': total_balance,})


def bank_transactions(request, pk):
    bank = get_object_or_404(Bank, id=pk)
    moves = Move.objects.filter(bank=bank).select_related('concept').order_by('-date')
    return render(request, 'bank_transactions.html', {
        'bank': bank,
        'moves': moves,
    })


