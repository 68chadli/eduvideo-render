from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import Commande, CommandePack, AccesPack
import mailtrap as mt
import os

class CommandePackInline(admin.TabularInline):
    model = CommandePack
    extra = 1

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'utilisateur', 'date_commande', 'statut', 'montant_total', 'afficher_recu']
    list_filter = ['statut', 'date_commande']
    actions = ['activer_commandes', 'desactiver_commandes', 'refuser_commandes']
    inlines = [CommandePackInline]
    readonly_fields = ['recu_preview']
    
    def afficher_recu(self, obj):
        if obj.recu:
            return format_html('<a href="{}" target="_blank">Voir le reçu</a>', obj.recu.url)
        return "Pas de reçu"
    afficher_recu.short_description = "Reçu"
    
    def recu_preview(self, obj):
        if obj.recu:
            return format_html('<a href="{}" target="_blank">📄 Télécharger le reçu</a>', obj.recu.url)
        return "Aucun fichier"
    recu_preview.short_description = "Reçu"
    
    fieldsets = (
        (None, {
            'fields': ('utilisateur', 'date_commande', 'statut', 'montant_total', 'recu_preview', 'motif_refus')
        }),
    )
    
    def activer_commandes(self, request, queryset):
        for commande in queryset:
            if commande.statut != 'activee':
                commande.statut = 'activee'
                commande.save()
                for cp in commande.packs_commandes.all():
                    AccesPack.objects.get_or_create(
                        utilisateur=commande.utilisateur,
                        pack=cp.pack
                    )
                # self.envoyer_email_confirmation(commande)
        self.message_user(request, f"{queryset.count()} commande(s) activée(s)")
    activer_commandes.short_description = "Activer les commandes sélectionnées"
    
    def envoyer_email_confirmation(self, commande):
        client = mt.MailtrapClient(token=os.getenv('MAILTRAP_API_TOKEN'))
        
        packs_liste = "\n".join([f"- {cp.pack.nom} : {cp.prix_au_moment_achat} DA" for cp in commande.packs_commandes.all()])
        
        message = f"""
Bonjour {commande.utilisateur.first_name} {commande.utilisateur.last_name},

Nous vous confirmons que votre commande n°{commande.id} a été activée.

📦 Détail de votre commande :
{packs_liste}

💰 Montant total : {commande.montant_total} DA

Vous pouvez maintenant accéder à vos vidéos en vous connectant à votre espace client :
🔗 http://127.0.0.1:8000/orders/my-videos/

Merci de votre confiance et bon apprentissage !

Cordialement,
L'équipe EduVideo
"""
        
        mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.co", name="EduVideo"),
            to=[mt.Address(email=commande.utilisateur.email)],
            subject=f"Votre commande #{commande.id} a été activée - EduVideo",
            text=message,
        )
        client.send(mail)
    
    def desactiver_commandes(self, request, queryset):
        for commande in queryset:
            if commande.statut == 'activee':
                commande.statut = 'en_attente'
                commande.save()
                for cp in commande.packs_commandes.all():
                    AccesPack.objects.filter(
                        utilisateur=commande.utilisateur,
                        pack=cp.pack
                    ).delete()
        self.message_user(request, f"{queryset.count()} commande(s) désactivée(s)")
    desactiver_commandes.short_description = "Désactiver les commandes sélectionnées"
    
    def refuser_commandes(self, request, queryset):
        for commande in queryset:
            if commande.statut != 'refusee':
                commande.statut = 'refusee'
                commande.save()
                for cp in commande.packs_commandes.all():
                    AccesPack.objects.filter(
                        utilisateur=commande.utilisateur,
                        pack=cp.pack
                    ).delete()
        self.message_user(request, f"{queryset.count()} commande(s) refusée(s)")
    refuser_commandes.short_description = "Refuser les commandes sélectionnées"

@admin.register(AccesPack)
class AccesPackAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'pack', 'date_activation', 'date_expiration']
    list_editable = ['date_expiration']
    fields = ['utilisateur', 'pack', 'date_activation', 'date_expiration']