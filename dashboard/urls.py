from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('parametres/', views.parametres_view, name='parametres'),
    path('', views.dashboard_index, name='dashboard_index'),
]