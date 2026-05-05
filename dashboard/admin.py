from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class AdminLink:
    @admin.display(description='Paramètres')
    def lien_parametres(self):
        return format_html('<a href="{}">⚙️ Paramètres généraux</a>', reverse('dashboard:parametres'))

admin.site.index_template = None