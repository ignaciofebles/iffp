from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Min, Max
from datetime import datetime
from dateutil.relativedelta import relativedelta
from concept.models import Concept
from move.models import Move
from django.core.paginator import Paginator

# Create your views here.
def concepts_balance(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    moves = Move.objects.filter(usuario=request.user).order_by('-date')

    if start_date:
        moves = moves.filter(date__gte=start_date) 
    if end_date:
        moves = moves.filter(date__lte=end_date)  

    concepts = Concept.objects.filter(usuario=request.user).order_by('description')    
    total_ingresos = 0
    total_egresos = 0
    for concepto in concepts:
        ingresos = moves.filter(concept=concepto, concept__type='IN', concept__transfer=False).aggregate(total=Sum('amount'))['total'] or 0
        egresos = moves.filter(concept=concepto, concept__type='EG', concept__transfer=False).aggregate(total=Sum('amount'))['total'] or 0
        concepto.saldo = ingresos - egresos
        total_ingresos += ingresos or 0
        total_egresos += egresos or 0

        if not moves.exists():            
            concepto.media_mensual = 0
            continue

        # Determinar fechas mínima y máxima si no hay filtro
        first_transaction = moves.aggregate(first_date=Min("date"))["first_date"]
        last_transaction = moves.aggregate(last_date=Max("date"))["last_date"]

        if not start_date:
            start_date = first_transaction
        if not end_date:
            end_date = last_transaction

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()            

        # Filtrar movimientos por el rango de fechas
        filtered_moves = moves.filter(date__range=[start_date, end_date])

        # Calcular la cantidad de meses en el rango
        months_count = max(1, (relativedelta(end_date, start_date).years * 12) + relativedelta(end_date, start_date).months + 1)

        # Calcular la media mensual
        concepto.num_meses = months_count
        concepto.media_mensual = concepto.saldo / months_count

    total_general = sum(concepto.saldo for concepto in concepts)
    return render(request, 'concepts_balance.html', {'concepts': concepts, 'total_general': total_general,'total_ingresos': total_ingresos, 'total_egresos': total_egresos})
   
   

def concept_transactions(request, pk):
    concept = get_object_or_404(Concept, id=pk)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    results_per_page = request.GET.get('results_per_page', '50')  
    page_number = request.GET.get('page', 1)  

    moves = Move.objects.filter(usuario=request.user, concept=concept).select_related('bank').order_by('-date')

    if start_date:
        moves = moves.filter(date__gte=start_date)
    if end_date:
        moves = moves.filter(date__lte=end_date)

    try:
        results_per_page = int(results_per_page)
        if results_per_page not in [50, 100, 200]:
            results_per_page = 50
    except ValueError:
        results_per_page = 50


    moves_with_sums = []
    current_month = None
    running_total = 0

    for move in moves:
        if move.date.month != current_month:
            current_month = move.date.month                   
            running_total = 0 
            running_total += move.amount
            
            moves_with_sums.append({
                'is_new_month': True,  
                'move': move,
                'running_total': running_total
            })
        else:
            running_total += move.amount                             
            moves_with_sums.append({
                'is_new_month': False,  
                'move': move,
                'running_total': running_total 
            })
           
    paginator = Paginator(moves_with_sums, results_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        'concept': concept,
        'moves_with_sums': page_obj,  
        'start_date': start_date,
        'end_date': end_date,
        'results_per_page': results_per_page
    }
    return render(request, 'concept_transactions.html', context)

