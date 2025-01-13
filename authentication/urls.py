from django.urls import path
from .views import VRegistro, cerrar_sesion, loguear, EditUserView


urlpatterns = [
    path('', VRegistro.as_view(), name='Autenticacion'),
    path('cerrar_sesion', cerrar_sesion, name='cerrar_sesion'),
    path('loguear', loguear, name='loguear'),
    path('<int:pk>/edit/', EditUserView.as_view(), name='edit_user'),
]

