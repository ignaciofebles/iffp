from django.urls import path
from . import views


urlpatterns = [
    path('', views.thing, name="Thing"),
    path('things_list/', views.things_list, name="things_list"),
    path('<int:pk>/edit/', views.ThingEditView.as_view(), name='Thing'),
    path('<int:pk>/delete/', views.ThingDeleteView.as_view(), name='thing_delete'),
    path('<int:pk>/show/', views.ThingDetailView.as_view(), name='thing_detail'),
    path('pdf/', views.ver_pdf, name='ver_pdf'),
]

