from django.shortcuts import render, redirect, get_object_or_404
from move.models import Move
from .forms import MoveForm
from django.views.generic import UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Sum
from shared.utils import get_bank_balance  
# import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import plotly.express as px
import plotly.io as pio
import pandas as pd


# Create your views here.
def move(request):
    if request.method == 'POST':
        form = MoveForm(request.POST, request=request, usuario=request.user)  
        if form.is_valid():
            form.instance.usuario = request.user  
            form.save()
            return redirect('move_detail', move_id=form.instance.id)  
    else:
        form = MoveForm(usuario=request.user, request=request)  

    return render(request, 'move.html', {'form': form})


def moves_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_commentary = request.GET.get('search_commentary', '').strip()
    results_per_page = request.GET.get('results_per_page', '50')  # Valor por defecto 50

    # Filtrar las transacciones
    moves = Move.objects.filter(usuario=request.user).order_by('-date')

    if start_date:
        moves = moves.filter(date__gte=start_date)  # Filtrar desde la fecha inicial
    if end_date:
        moves = moves.filter(date__lte=end_date)  # Filtrar hasta la fecha final
    if search_commentary:
        moves = moves.filter(comentary__icontains=search_commentary)  # Filtrar por comentario

    # Paginación
    paginator = Paginator(moves, results_per_page)  # Paginador con los resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'moves': page_obj,  # Usar el objeto de la página
    }
    return render(request, 'moves_list.html', context) 
    

class MoveEditView(UpdateView):
    model = Move
    form_class = MoveForm
    template_name = 'move.html'
    success_url = reverse_lazy('moves_list')
    
    def get_object(self, queryset=None):
        return Move.objects.get(id=self.kwargs['pk'])
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        kwargs['request'] = self.request  
        return kwargs


class MoveDeleteView(DeleteView):
    model = Move
    template_name = 'move_confirm_delete.html'
    success_url = reverse_lazy('moves_list') 



class MoveDetailView(DetailView):
    model = Move
    template_name = 'move_detail.html'  
    context_object_name = 'move'

    def get_object(self):
        return get_object_or_404(Move, id=self.kwargs['move_id'])    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        move = self.get_object()

        saldo = get_bank_balance(self.request, move.bank)
        context['saldo'] = saldo

        context['form'] = MoveForm(request=self.request, usuario=self.request.user)  
        
        return context



def move_chart_view(request):
    # Obtener los datos del modelo y transformarlos en un DataFrame
    data = (
        Move.objects.values("concept__description")  # Agrupar por concepto
        .annotate(total_amount=Sum("amount"))       # Sumar los montos por concepto
        .order_by("-total_amount")                  # Ordenar de mayor a menor
    )
    df = pd.DataFrame(data)  # Convertir a DataFrame de Pandas

    # Crear el gráfico con Plotly
    fig = px.bar(
        df,
        x="concept__description",
        y="total_amount",
        labels={"concept__description": "Concepto", "total_amount": "Monto Total (€)"},
        title="Transacciones por Concepto",
    )

    # Guardar el gráfico como imagen
    buffer = io.BytesIO()
    pio.write_image(fig, buffer, format="png", width=800, height=600)
    buffer.seek(0)

    # Retornar la imagen como respuesta HTTP
    return HttpResponse(buffer, content_type="image/png")
