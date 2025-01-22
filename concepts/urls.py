from django.urls import path
from . import views


urlpatterns = [
    path('concepts_balance/', views.concepts_balance, name="concepts_balance"),
    path('<int:pk>/transactions/', views.concept_transactions, name='concept_transactions'),
]

