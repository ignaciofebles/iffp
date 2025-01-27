from django.urls import path
from . import views


urlpatterns = [
    path('', views.move, name="Move"),
    path('moves_list/', views.moves_list, name="moves_list"),
    path('<int:pk>/edit/', views.MoveEditView.as_view(), name='Move'),
    path('<int:pk>/delete/', views.MoveDeleteView.as_view(), name='move_delete'),
    path('<int:move_id>/view/', views.MoveDetailView.as_view(), name='move_detail'),
    path('move-chart/', views.move_chart_view, name='move_chart'),
]

