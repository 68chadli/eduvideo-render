from django.contrib import admin
from .models import Annee, Specialite, Matiere, Enseignant, Video, Pack, PackVideo

@admin.register(Annee)
class AnneeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre']
    list_editable = ['ordre']

@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    filter_horizontal = ['annees']

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    filter_horizontal = ['specialites']

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'matiere']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_video', 'enseignant', 'ordre']
    list_filter = ['type_video']

class PackVideoInline(admin.TabularInline):
    model = PackVideo
    extra = 1

@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prix', 'type_pack', 'matiere', 'annee', 'est_populaire', 'est_nouveau', 'est_visible']
    list_filter = ['type_pack', 'est_populaire', 'est_nouveau', 'est_visible']
    list_editable = ['est_populaire', 'est_nouveau', 'prix']
    inlines = [PackVideoInline]  # ← Gère les vidéos via PackVideo
    fieldsets = (
        (None, {
            'fields': ('nom', 'description', 'prix', 'type_pack', 'matiere', 'annee', 'est_visible')
        }),
        ('Mise en avant', {
            'fields': ('est_populaire', 'est_nouveau'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PackVideo)
class PackVideoAdmin(admin.ModelAdmin):
    list_display = ['pack', 'video', 'ordre', 'est_video_explicative']
    list_editable = ['ordre', 'est_video_explicative']