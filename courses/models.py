from django.db import models

class Annee(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.nom


class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    annees = models.ManyToManyField(Annee, related_name='specialites')

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    specialites = models.ManyToManyField(Specialite, related_name='matieres')

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Enseignant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    lycee = models.CharField(max_length=200, blank=True)
    biographie = models.TextField(blank=True)
    photo = models.ImageField(upload_to='enseignants/', blank=True, null=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True, blank=True, related_name='enseignants')

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Video(models.Model):
    TYPE_CHOICES = [
        ('cours', 'Cours'),
        ('exercice', 'Exercice corrigé'),
        ('bac', 'Correction d\'épreuve'),
    ]
    
    titre = models.CharField(max_length=200)
    type_video = models.CharField(max_length=20, choices=TYPE_CHOICES, default='cours')
    duree = models.CharField(max_length=20, blank=True)
    url_hebergement = models.URLField()
    description = models.TextField(blank=True)
    ordre = models.IntegerField(default=0)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.titre


class Pack(models.Model):
    TYPE_PACK_CHOICES = [
        ('annuel', 'Pack annuel'),
        ('semestriel', 'Pack semestriel'),
        ('trimestriel', 'Pack trimestriel'),
        ('chapitre', 'Pack chapitre'),
        ('exercices', 'Pack exercices'),
        ('bac', 'Pack résolution d\'épreuves'),
    ]
    
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    type_pack = models.CharField(max_length=20, choices=TYPE_PACK_CHOICES, default='annuel')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='packs')  # ← clé étrangère simple
    annee = models.ForeignKey(Annee, on_delete=models.CASCADE, related_name='packs')     # ← nouveau champ
    videos = models.ManyToManyField(Video, through='PackVideo', related_name='packs')
    est_visible = models.BooleanField(default=True)
    est_populaire = models.BooleanField(default=False)
    est_nouveau = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} - {self.prix} DA"


class PackVideo(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    ordre = models.IntegerField(default=0)
    est_video_explicative = models.BooleanField(default=False)

    class Meta:
        ordering = ['ordre']
        unique_together = ['pack', 'video']

    def __str__(self):
        return f"{self.pack.nom} - {self.video.titre}"