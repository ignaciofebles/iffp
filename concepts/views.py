from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Min, Max
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

       # Convertir a objetos datetime si son cadenas
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

    # Obtener las transacciones ordenadas por fecha de forma ascendente
    moves = Move.objects.filter(concept=concept).select_related('bank').order_by('-date')
    running_total = 0
    current_month = moves.first().date.month if moves.exists() else None
    print('primer mes: ', current_month)
    moves_with_sums = []

    # Procesar cada movimiento
    for move in moves:
        # Detectar el cambio de mes (antes de sumar el monto)
        if move.date.month != current_month:
            # Si el mes cambia, reiniciar el total acumulado
            current_month = move.date.month                   
            running_total = 0  # Reiniciar el acumulado
            running_total += move.amount
            
            # Añadir la fila de cambio de mes con un indicador
            moves_with_sums.append({
                'is_new_month': True,  # Indicador de cambio de mes
                'move': move,
                'running_total': running_total  # Reiniciado a cero
            })
        else:
            running_total += move.amount                             
            moves_with_sums.append({
                'is_new_month': False,  # No es un nuevo mes
                'move': move,
                'running_total': running_total  # Mantener el valor acumulado
            })
           
       
    return render(request, 'concept_transactions.html', {
        'concept': concept,
        'moves_with_sums': moves_with_sums  # Pasar la lista con los cálculos
    })

