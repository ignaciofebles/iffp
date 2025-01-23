from django.shortcuts import render, redirect
from thing.models import Thing
from .forms import ThingForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

# Create your views here.
def thing(request):
    if request.method == 'POST':
        form = ThingForm(request.POST)
        if form.is_valid():
            thing = form.save(commit=False)
            thing.usuario = request.user
            thing.save()
            return redirect('things_list') 
    else:
        form = ThingForm()
    return render(request, 'thing.html', {'form': form})



# def things_list(request):
#     search_term = request.GET.get('search', '').strip()

#     if search_term:
#         things = Thing.objects.filter(usuario=request.user, code__icontains=search_term).order_by('code')

#         if not things.exists():
#             things = Thing.objects.filter(usuario=request.user, description__icontains=search_term).order_by('code')
#     else:
#         things = Thing.objects.filter(usuario=request.user).order_by('code')
    
        
#     context = {
#         'things': things,
#     }
#     return render(request, 'things_list.html', context)

def things_list(request):
    search_term = request.GET.get('search', '').strip()

    if search_term:
        # Usar Q para buscar en 'code' y 'description'
        things = Thing.objects.filter(
            Q(usuario=request.user) & 
            (Q(code__icontains=search_term) | Q(description__icontains=search_term))
        ).order_by('code')
    else:
        things = Thing.objects.filter(usuario=request.user).order_by('code')

    context = {
        'things': things,
    }
    return render(request, 'things_list.html', context)


class ThingEditView(UpdateView):
    model = Thing
    form_class = ThingForm
    template_name = 'thing.html'
    success_url = reverse_lazy('things_list')


class ThingDeleteView(DeleteView):
    model = Thing
    template_name = 'thing_confirm_delete.html'
    success_url = reverse_lazy('things_list') 


    from django.db.models import Q

