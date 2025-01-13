from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import EditUserForm


# Create your views here.
class VRegistro(View):
    
    def get(self, request):
        form=UserCreationForm()
        return render(request, 'registro.html', {"form":form})

    def post(self, request):
        form=UserCreationForm(request.POST)
        
        if form.is_valid():
            usuario=form.save()
            login(request, usuario)
            return redirect('Home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, 'registro.html', {"form":form})
        

def cerrar_sesion(request):
    logout(request)
    return redirect('Home')


def loguear(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get('username')
            contra=form.cleaned_data.get('password')
            usuario=authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect('Home')
            else:
                messages.error(request, 'Usuario no válido')
        else:
            messages.error(request, 'Información incorrecta')


    form=AuthenticationForm()
    return render(request, 'login.html', {"form":form})


class EditUserView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'edit_user.html'
    success_url = reverse_lazy('Home') 