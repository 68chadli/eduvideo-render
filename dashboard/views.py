from django.shortcuts import render,  redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.utils import timezone
from orders.models import Commande, AccesPack
from accounts.models import User
from courses.models import Pack
from django.contrib import messages
from .models import Parametres


@staff_member_required
def dashboard_index(request):
    now = timezone.now()
    
    # Commandes en attente
    commandes_attente = Commande.objects.filter(statut='en_attente').count()
    
    # Clients actifs (qui ont au moins un accès)
    clients_actifs = AccesPack.objects.values('utilisateur').distinct().count()
    
    # Packs vendus
    packs_vendus = Commande.objects.filter(statut='activee').aggregate(total=Sum('montant_total'))['total'] or 0
    
    # CA mensuel
    ca_mois = Commande.objects.filter(
        statut='activee',
        date_commande__year=now.year,
        date_commande__month=now.month
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    # CA annuel
    ca_annee = Commande.objects.filter(
        statut='activee',
        date_commande__year=now.year
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    # Historique CA par mois (derniers 12 mois)
    ca_historique = []
    for i in range(11, -1, -1):
        mois = now.month - i
        annee = now.year
        if mois <= 0:
            mois += 12
            annee -= 1
        total = Commande.objects.filter(
            statut='activee',
            date_commande__year=annee,
            date_commande__month=mois
        ).aggregate(total=Sum('montant_total'))['total'] or 0
        ca_historique.append({
            'mois': f"{annee}-{mois:02d}",
            'total': float(total)
        })
    
    context = {
        'commandes_attente': commandes_attente,
        'clients_actifs': clients_actifs,
        'packs_vendus': packs_vendus,
        'ca_mois': ca_mois,
        'ca_annee': ca_annee,
        'ca_historique': ca_historique,
    }
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def parametres_view(request):
    params = Parametres.get()
    
    if request.method == 'POST':
        if 'date_fin_annee' in request.POST:
            from datetime import datetime
            date_str = request.POST.get('date_fin_annee')
            params.date_fin_annee = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
            params.save()
            messages.success(request, "Date de fin d'année mise à jour")
        
        if 'bloquer' in request.POST:
            params.acces_bloques = True
            params.save()
            messages.warning(request, "Tous les accès sont bloqués")
        
        if 'debloquer' in request.POST:
            params.acces_bloques = False
            params.save()
            messages.success(request, "Accès réactivés")
        
        return redirect('dashboard:parametres')
    
    return render(request, 'dashboard/parametres.html', {'params': params})