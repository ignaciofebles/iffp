from django.db.models import Sum
from move.models import Move

def get_bank_balance(request, bank):
    """Calcula el saldo de un banco específico."""
    ingresos = Move.objects.filter(usuario=request.user, bank=bank, concept__type='IN').aggregate(total=Sum('amount'))['total'] or 0
    egresos = Move.objects.filter(usuario=request.user, bank=bank, concept__type='EG').aggregate(total=Sum('amount'))['total'] or 0
    # ingresos = Move.objects.filter(bank=bank, concept__type='IN').aggregate(total=Sum('amount'))['total'] or 0
    # egresos = Move.objects.filter(bank=bank, concept__type='EG').aggregate(total=Sum('amount'))['total'] or 0

    return ingresos - egresos
