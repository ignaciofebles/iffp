from django.shortcuts import render, redirect
from concept.models import Concept
from .forms import ConceptForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def concept(request):
    if request.method == 'POST':
        form = ConceptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('concepts_list')  # Redirige a una página después de guardar
    else:
        form = ConceptForm()
    return render(request, 'concept.html', {'form': form})



def concepts_list(request):
    concepts = Concept.objects.all()
    return render(request, 'concepts_list.html', {'concepts': concepts})


class ConceptEditView(UpdateView):
    model = Concept
    form_class = ConceptForm
    template_name = 'concept.html'
    success_url = reverse_lazy('concepts_list')


class ConceptDeleteView(DeleteView):
    model = Concept
    template_name = 'concept_confirm_delete.html'
    success_url = reverse_lazy('concepts_list') 