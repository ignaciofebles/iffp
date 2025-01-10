from django.shortcuts import render, redirect
from thing.models import Thing
from .forms import ThingForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def thing(request):
    if request.method == 'POST':
        form = ThingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('things_list')  # Redirige a una página después de guardar
    else:
        form = ThingForm()
    return render(request, 'thing.html', {'form': form})



def things_list(request):
    things = Thing.objects.all()
    return render(request, 'things_list.html', {'things': things})


class ThingEditView(UpdateView):
    model = Thing
    form_class = ThingForm
    template_name = 'thing.html'
    success_url = reverse_lazy('things_list')


class ThingDeleteView(DeleteView):
    model = Thing
    template_name = 'thing_confirm_delete.html'
    success_url = reverse_lazy('things_list') 