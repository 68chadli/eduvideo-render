from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Annee, Specialite, Matiere, Pack, Video, PackVideo
from orders.models import AccesPack  # ← Ajoutez cet import en haut
from django.db import models  # Pour les Q objects
from django.utils import timezone

def annee_list(request):
    annees = Annee.objects.all()
    breadcrumbs = [
        {'name': 'Accueil', 'url': '/'},
        {'name': 'Années', 'url': request.path},
    ]
    return render(request, 'courses/annee_list.html', {
        'annees': annees,
        'breadcrumbs': breadcrumbs,
    })
def specialite_list(request, annee_id):
    annee = get_object_or_404(Annee, id=annee_id)
    specialites = annee.specialites.all()
    breadcrumbs = [
        {'name': 'Accueil', 'url': '/'},
        {'name': 'Années', 'url': '/courses/annees/'},
        {'name': annee.nom, 'url': request.path},
    ]
    return render(request, 'courses/specialite_list.html', {
        'annee': annee,
        'specialites': specialites,
        'breadcrumbs': breadcrumbs,
    })
def matiere_list(request, annee_id, specialite_id):
    annee = get_object_or_404(Annee, id=annee_id)
    specialite = get_object_or_404(Specialite, id=specialite_id)
    matieres = specialite.matieres.all()
    
    breadcrumbs = [
        {'name': 'Accueil', 'url': '/'},
        {'name': 'Années', 'url': '/courses/annees/'},
        {'name': annee.nom, 'url': f'/courses/specialites/{annee.id}/'},
        {'name': specialite.nom, 'url': f'/courses/matieres/{annee.id}/{specialite.id}/'},  # ← Spécialité
        {'name': 'Matières', 'url': request.path},  # Optionnel
    ]
    
    return render(request, 'courses/matiere_list.html', {
        'annee': annee,
        'specialite': specialite,
        'matieres': matieres,
        'breadcrumbs': breadcrumbs,
    })
def pack_list(request, annee_id, specialite_id, matiere_id):
    annee = get_object_or_404(Annee, id=annee_id)
    specialite = get_object_or_404(Specialite, id=specialite_id)
    matiere = get_object_or_404(Matiere, id=matiere_id)
    packs = Pack.objects.filter(annee=annee, specialite=specialite, matiere=matiere)
    
    breadcrumbs = [
        {'name': 'Accueil', 'url': '/'},
        {'name': 'Années', 'url': '/courses/annees/'},
        {'name': annee.nom, 'url': f'/courses/specialites/{annee.id}/'},
        {'name': specialite.nom, 'url': f'/courses/matieres/{annee.id}/{specialite.id}/'},
        {'name': matiere.nom, 'url': request.path},
    ]
    
    return render(request, 'courses/pack_list.html', {
        'annee': annee,
        'specialite': specialite,
        'matiere': matiere,
        'packs': packs,
        'breadcrumbs': breadcrumbs,
    })
def pack_detail(request, pack_id):
    pack = get_object_or_404(Pack, id=pack_id)
    pack_videos = pack.packvideo_set.all().order_by('ordre')
    
    # Première vidéo gratuite (essai)
    premiere_video = None
    if pack_videos.exists():
        premiere_video = pack_videos.first().video
    
    return render(request, 'courses/pack_detail.html', {
        'pack': pack,
        'pack_videos': pack_videos,
        'premiere_video': premiere_video,
    })

def video_player(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Vérifier si la vidéo est gratuite (essai)
    pack_video = PackVideo.objects.filter(video=video, est_video_explicative=True).first()
    if pack_video:
        return render(request, 'courses/video_player.html', {'video': video})
    
    # Vérifier si l'utilisateur a acheté le pack
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # Trouver le pack qui contient cette vidéo
    pack_video_item = PackVideo.objects.filter(video=video).first()
    if pack_video_item:
        pack = pack_video_item.pack
        # Vérifier si l'utilisateur a un accès actif à ce pack et si date expiration pas encore atteinte
        acces = AccesPack.objects.filter(utilisateur=request.user, pack=pack).filter(
            models.Q(date_expiration__isnull=True) | models.Q(date_expiration__gte=timezone.now().date())
        ).first()
        if acces:
            # L'utilisateur a acheté le pack → vidéo accessible
            return render(request, 'courses/video_player.html', {'video': video})
        else:
            messages.error(request, "Vous n'avez plus accès au pack '{pack.nom}'.(Expiration ou non acheté)" )
            return redirect('courses:pack_detail', pack_id=pack.id)
    
    messages.error(request, "Cette vidéo n'est pas disponible.")
    return redirect('courses:annee_list')
def accueil(request):
    packs_populaires = Pack.objects.filter(est_visible=True)[:3]
    return render(request, 'accueil.html', {'packs_populaires': packs_populaires})