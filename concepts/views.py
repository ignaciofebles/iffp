from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from concept.models import Concept
from move.models import Move

# Create your views here.

def concepts_balance(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filtrar las transacciones
    moves = Move.objects.filter(usuario=request.user).order_by('-date')

    if start_date:
        moves = moves.filter(date__gte=start_date)  # Filtrar desde la fecha inicial
    if end_date:
        moves = moves.filter(date__lte=end_date)  # Filtrar hasta la fecha final

    # return render(request, 'moves_list.html', context)    
    concepts = Concept.objects.filter(usuario=request.user).order_by('description')    
    total_ingresos = 0
    total_egresos = 0
    for concepto in concepts:
        # ingresos = Move.objects.filter(concept=concepto, concept__type='IN', concept__transfer=False).aggregate(total=Sum('amount'))['total'] or 0
        # egresos = Move.objects.filter(concept=concepto, concept__type='EG', concept__transfer=False).aggregate(total=Sum('amount'))['total'] or 0
        ingresos = moves.filter(concept=concepto, concept__type='IN', concept__transfer=False).aggregate(total=Sum('amount'))['total'] or 0
        egresos = moves.filter(concept=concepto, concept__type='EG', concept__transfer=False).aggregate(total=Sum('amount'))['total'] or 0
        concepto.saldo = ingresos - egresos
        total_ingresos += ingresos or 0
        total_egresos += egresos or 0

    total_general = sum(concepto.saldo for concepto in concepts)
    return render(request, 'concepts_balance.html', {'concepts': concepts, 'total_general': total_general,'total_ingresos': total_ingresos, 'total_egresos': total_egresos})
   
   

def concept_transactions(request, pk):
    concept = get_object_or_404(Concept, id=pk)

    moves = Move.objects.filter(concept=concept).select_related('bank').order_by('-date')
    return render(request, 'concept_transactions.html', {
        'concept': concept,
        'moves': moves,
    })
