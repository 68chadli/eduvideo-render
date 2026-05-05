from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
path('annees/', views.annee_list, name='annee_list'),
path('specialites/<int:annee_id>/', views.specialite_list, name='specialite_list'),
path('matieres/<int:annee_id>/<int:specialite_id>/', views.matiere_list, name='matiere_list'),
path('packs/<int:annee_id>/<int:specialite_id>/<int:matiere_id>/', views.pack_list, name='pack_list'),
path('pack/<int:pack_id>/', views.pack_detail, name='pack_detail'),
path('video/<int:video_id>/', views.video_player, name='video_player'),
]