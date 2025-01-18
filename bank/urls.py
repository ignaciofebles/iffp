from django.urls import path
from . import views


urlpatterns = [
    path('', views.bank, name="Bank"),
    path('banks_list/', views.banks_list, name="banks_list"),
    path('<int:pk>/edit/', views.BankEditView.as_view(), name='Bank'),
    path('<int:pk>/delete/', views.BankDeleteView.as_view(), name='bank_delete'),
    
]

