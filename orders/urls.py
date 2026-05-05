from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    # Nous ajouterons les URLs plus tard
    path('add-to-cart/<int:pack_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-videos/', views.my_videos, name='my_videos'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('upload-recu/<int:commande_id>/', views.upload_recu, name='upload_recu'),
    path('remove-from-cart/<int:pack_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('export/excel/', views.export_excel, name='export_excel'),
]