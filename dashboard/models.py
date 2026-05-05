from django.db import models

class Parametres(models.Model):
    date_fin_annee = models.DateField(null=True, blank=True)
    acces_bloques = models.BooleanField(default=False)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def __str__(self):
        return f"Paramètres (bloqué: {self.acces_bloques})"