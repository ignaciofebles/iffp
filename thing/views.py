from django.shortcuts import render, redirect
from thing.models import Thing
from .forms import ThingForm
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.db.models import Q, Func
from django.core.paginator import Paginator

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



class Unaccent(Func):
    function = 'unaccent'
    template = '%(function)s(%(expressions)s)'



def things_list(request):
    search_term = request.GET.get('search', '').strip()
    results_per_page = request.GET.get('results_per_page', '50')
    page_number = request.GET.get('page', '1')

    # Filtrar objetos por usuario
    things = Thing.objects.filter(usuario=request.user)

    # Aplicar filtro de búsqueda
    if search_term:
        normalized_search_term = normalize_search_term(search_term)
        things = things.annotate(
            unaccented_code=Unaccent('code'),
            unaccented_description=Unaccent('description')
        ).filter(
            Q(unaccented_code__icontains=normalized_search_term) | 
            Q(unaccented_description__icontains=normalized_search_term)
        )

    # Ordenar resultados por código
    things = things.order_by('code')

    # Manejo de paginación
    paginator = Paginator(things, int(results_per_page))
    page_obj = paginator.get_page(page_number)

    context = {
        'things': page_obj,
        'search_term': search_term,
        'results_per_page': results_per_page,
    }

    return render(request, 'things_list.html', context)



def normalize_search_term(term):
    """
    Normaliza el término de búsqueda eliminando acentos.
    """
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }
    for accented_char, unaccented_char in replacements.items():
        term = term.replace(accented_char, unaccented_char)
    return term



class ThingEditView(UpdateView):
    model = Thing
    form_class = ThingForm
    template_name = 'thing.html'
    success_url = reverse_lazy('things_list')



class ThingDeleteView(DeleteView):
    model = Thing
    template_name = 'thing_confirm_delete.html'
    success_url = reverse_lazy('things_list') 
    


class ThingDetailView(DetailView):
    model = Thing
    template_name = 'thing_detail.html'  # Asegúrate de cambiar esto por el nombre de tu archivo
    success_url = reverse_lazy('things_list') 


def ver_pdf(request):
    return render(request, 'ver_pdf.html')