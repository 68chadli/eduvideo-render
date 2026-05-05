from django.db import models
from django.conf import settings
from courses.models import Pack

class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('activee', 'Activée'),
        ('refusee', 'Refusée'),
    ]
    
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commandes')
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    recu = models.FileField(upload_to='recus/', blank=True, null=True)
    motif_refus = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Commande {self.id} - {self.utilisateur.username} - {self.get_statut_display()}"

class CommandePack(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='packs_commandes')
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    prix_au_moment_achat = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.commande.id} - {self.pack.nom}"

class AccesPack(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='acces_packs')
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    date_activation = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ['utilisateur', 'pack']
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.pack.nom}"