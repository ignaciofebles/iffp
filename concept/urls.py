from django.urls import path
from . import views


urlpatterns = [
    path('', views.concept, name="Concept"),
    path('concepts_list/', views.concepts_list, name="concepts_list"),
    path('<int:pk>/edit/', views.ConceptEditView.as_view(), name='Concept'),
    path('<int:pk>/delete/', views.ConceptDeleteView.as_view(), name='concept_delete'),    
]

