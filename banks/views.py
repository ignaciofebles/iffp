from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime
from bank.models import Bank
from move.models import Move
from shared.utils import get_bank_balance

def banks_balance(request):    
    banks = Bank.objects.filter(usuario=request.user).order_by('description')
    for banco in banks:
        banco.saldo = get_bank_balance(request, banco)
    total_balance = sum(bank.saldo for bank in banks)

    return render(request, 'banks_balance.html', {
        'banks': banks, 
        'total_balance': total_balance,
    })



def bank_transactions(request, pk):
    bank = get_object_or_404(Bank, id=pk)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    results_per_page = request.GET.get('results_per_page', '50')  # Valor por defecto 50
    page_number = request.GET.get('page', 1)  # Página actual

    # Filtrar las transacciones
    moves = Move.objects.filter(usuario=request.user, bank=bank).select_related('concept').order_by('-date', '-id')

    if start_date:
        moves = moves.filter(date__gte=start_date)  # Filtrar desde la fecha inicial
    if end_date:
        moves = moves.filter(date__lte=end_date)  # Filtrar hasta la fecha final

    try:
        results_per_page = int(results_per_page)
        if results_per_page not in [50, 100, 200]:
            results_per_page = 50  # Si el valor no es válido, usar el predeterminado
    except ValueError:
        results_per_page = 50  # Si no se puede convertir, usar el predeterminado

    # Paginación
    paginator = Paginator(moves, results_per_page)
    page_obj = paginator.get_page(page_number)  # Obtener la página actual

    context = {
        'bank': bank,
        'moves': page_obj,  # Página actual de movimientos
        'start_date': start_date,
        'end_date': end_date,
        'results_per_page': results_per_page
    }
    return render(request, 'bank_transactions.html', context)
