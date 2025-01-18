from django.urls import path
from . import views


urlpatterns = [
    path('banks_balance/', views.banks_balance, name="banks_balance"),
    path('<int:pk>/transactions/', views.bank_transactions, name='bank_transactions'),
    # path('<int:pk>/delete/', views.BankDeleteView.as_view(), name='bank_delete'),
]

