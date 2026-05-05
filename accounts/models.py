from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)
    est_actif = models.BooleanField(default=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    # db_constraint=False pour éviter l'erreur errno:150 sur MariaDB
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        db_constraint=False,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        db_constraint=False,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    class LogConnexion(models.Model):
        utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logs')
        date_connexion = models.DateTimeField(auto_now_add=True)
        ip_adresse = models.GenericIPAddressField(null=True, blank=True)

        def __str__(self):
            return f"{self.utilisateur.username} - {self.date_connexion}"
class LogConnexion(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logs')
    date_connexion = models.DateTimeField(auto_now_add=True)
    ip_adresse = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.date_connexion}"