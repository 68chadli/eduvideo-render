from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import LogConnexion

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telephone', 'est_actif')
    list_filter = ('est_actif', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('telephone', 'est_actif', 'session_key')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(LogConnexion)
class LogConnexionAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'date_connexion', 'ip_adresse']
    list_filter = ['date_connexion']
    search_fields = ['utilisateur__username', 'ip_adresse']
