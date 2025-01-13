from django.shortcuts import render, redirect, get_object_or_404
from move.models import Move
from .forms import MoveForm
from django.views.generic import UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy


# Create your views here.
def move_detail_view(request, move_id):
    move = get_object_or_404(Move, id=move_id)
    return render(request, 'move_detail.html', {'move': move})


def move(request):
   form = MoveForm(request.POST, user=request.user)  # Pasar el usuario al formulario
   if form.is_valid():
      form.instance.usuario = request.user  # Asegura que el movimiento tiene el usuario
      form.save()
      return redirect('move_detail', move_id=form.instance.id)  # Redirigir al detalle del movimiento
   else:
      form = MoveForm(user=request.user)
   return render(request, 'move.html', {'form': form})


def moves_list(request):
    moves = Move.objects.filter(usuario=request.user)
    return render(request, 'moves_list.html', {'moves': moves})


class MoveEditView(UpdateView):
    model = Move
    form_class = MoveForm
    template_name = 'move.html'
    success_url = reverse_lazy('moves_list')

    def get_object(self, queryset=None):
        return Move.objects.get(id=self.kwargs['move_id'])


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
    



# def move(request):
#     if request.method == 'POST':
#         form = MoveForm(request.POST, user=request.user)  # Pasar el usuario al formulario
#         if form.is_valid():
#             form.instance.usuario = request.user  # Asegura que el movimiento tiene el usuario
#             form.save()
#             return redirect('move_detail', move_id=form.instance.id)  # Redirigir al detalle del movimiento
#     else:
#         form = MoveForm(user=request.user)  # Pasar el usuario al formulario

#     return render(request, 'move.html', {'form': form})    