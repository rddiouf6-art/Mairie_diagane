from django.contrib import messages
from django.db.models import Q, Sum
from django.db.models.deletion import ProtectedError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CitizenForm, CivilRecordForm, AdministrativeRequestForm, FinancialTransactionForm
from .models import Citizen, CivilRecord, AdministrativeRequest, FinancialTransaction


def accueil(request):
    context = {
        'citoyens_count': Citizen.objects.count(),
        'demandes_count': AdministrativeRequest.objects.count(),
        'demandes_traitees': AdministrativeRequest.objects.filter(statut='TRAITEE').count(),
        'demandes_attente': AdministrativeRequest.objects.filter(statut='ATTENTE').count(),
        'dernieres_demandes': AdministrativeRequest.objects.select_related('citoyen')[:6],
    }
    return render(request, 'accueil.html', context)


def citoyens_liste(request):
    q = request.GET.get('q', '').strip()
    citoyens = Citizen.objects.all()
    if q:
        citoyens = citoyens.filter(Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(telephone__icontains=q) | Q(numero_piece__icontains=q))
    return render(request, 'dashboard/citoyens.html', {'citoyens': citoyens, 'q': q})


def citoyen_ajouter(request):
    form = CitizenForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Le citoyen a été enregistré.'); return redirect('citoyens')
    return render(request, 'dashboard/form.html', {'form': form, 'titre': 'Ajouter un citoyen', 'retour': 'citoyens'})


def citoyen_modifier(request, pk):
    citoyen = get_object_or_404(Citizen, pk=pk)
    form = CitizenForm(request.POST or None, instance=citoyen)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Les informations du citoyen ont été modifiées.'); return redirect('citoyens')
    return render(request, 'dashboard/form.html', {'form': form, 'titre': 'Modifier un citoyen', 'retour': 'citoyens'})


def citoyen_supprimer(request, pk):
    citoyen = get_object_or_404(Citizen, pk=pk)
    if request.method == 'POST':
        try:
            citoyen.delete()
            messages.success(request, 'Le citoyen a été supprimé.')
        except ProtectedError:
            messages.error(request, 'Suppression impossible : ce citoyen est lié à un acte d’état civil ou à une demande. Conservez son dossier ou supprimez d’abord les éléments liés.')
        return redirect('citoyens')
    return render(request, 'dashboard/confirm_delete.html', {'objet': citoyen, 'titre': 'Supprimer ce citoyen ?', 'retour': 'citoyens'})


def etat_civil(request):
    q = request.GET.get('q', '').strip()
    type_acte = request.GET.get('type', '')
    actes = CivilRecord.objects.select_related('citoyen', 'conjoint')
    if q:
        actes = actes.filter(Q(numero_acte__icontains=q) | Q(citoyen__nom__icontains=q) | Q(citoyen__prenom__icontains=q))
    if type_acte in ['NAISSANCE', 'MARIAGE', 'DECES']:
        actes = actes.filter(type_acte=type_acte)
    return render(request, 'dashboard/etat_civil.html', {'actes': actes, 'q': q, 'type_acte': type_acte})


def acte_ajouter(request):
    form = CivilRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'L’acte a été enregistré.'); return redirect('etat_civil')
    return render(request, 'dashboard/form.html', {'form': form, 'titre': 'Enregistrer un acte d’état civil', 'retour': 'etat_civil'})


def acte_modifier(request, pk):
    acte = get_object_or_404(CivilRecord, pk=pk)
    form = CivilRecordForm(request.POST or None, instance=acte)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'L’acte a été modifié.'); return redirect('etat_civil')
    return render(request, 'dashboard/form.html', {'form': form, 'titre': 'Modifier un acte', 'retour': 'etat_civil'})


def acte_supprimer(request, pk):
    acte = get_object_or_404(CivilRecord, pk=pk)
    if request.method == 'POST':
        acte.delete(); messages.success(request, 'L’acte a été supprimé.'); return redirect('etat_civil')
    return render(request, 'dashboard/confirm_delete.html', {'objet': acte, 'titre': 'Supprimer cet acte ?', 'retour': 'etat_civil'})


def demandes_liste(request):
    q = request.GET.get('q', '').strip()
    statut = request.GET.get('statut', '')
    demandes = AdministrativeRequest.objects.select_related('citoyen')
    if q:
        demandes = demandes.filter(Q(numero__icontains=q) | Q(citoyen__nom__icontains=q) | Q(citoyen__prenom__icontains=q))
    if statut in ['ATTENTE', 'EN_COURS', 'TRAITEE', 'REJETEE']:
        demandes = demandes.filter(statut=statut)
    return render(request, 'dashboard/demandes.html', {'demandes': demandes, 'q': q, 'statut': statut})


def demande_ajouter(request):
    form = AdministrativeRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        demande = form.save(); messages.success(request, f'Demande {demande.numero} enregistrée.'); return redirect('demandes')
    return render(request, 'dashboard/form.html', {'form': form, 'titre': 'Nouvelle demande administrative', 'retour': 'demandes'})


def demande_modifier(request, pk):
    demande = get_object_or_404(AdministrativeRequest, pk=pk)
    form = AdministrativeRequestForm(request.POST or None, instance=demande)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'La demande a été mise à jour.'); return redirect('demandes')
    return render(request, 'dashboard/form.html', {'form': form, 'titre': 'Traiter une demande', 'retour': 'demandes'})


def demande_supprimer(request, pk):
    demande = get_object_or_404(AdministrativeRequest, pk=pk)
    if request.method == 'POST':
        demande.delete(); messages.success(request, 'La demande a été supprimée.'); return redirect('demandes')
    return render(request, 'dashboard/confirm_delete.html', {'objet': demande, 'titre': 'Supprimer cette demande ?', 'retour': 'demandes'})


def demande_pdf(request, pk):
    demande = get_object_or_404(AdministrativeRequest.objects.select_related('citoyen'), pk=pk)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm
    except ImportError:
        return HttpResponse('La bibliothèque ReportLab manque. Installez-la avec : pip install reportlab', status=500, content_type='text/plain; charset=utf-8')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="demande_{demande.numero}.pdf"'
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    pdf.setTitle(f'Fiche de demande {demande.numero}')
    pdf.setFont('Helvetica-Bold', 16); pdf.drawCentredString(width/2, height-25*mm, 'MAIRIE DE DIAGANE BARKA')
    pdf.setFont('Helvetica-Bold', 13); pdf.drawCentredString(width/2, height-36*mm, 'FICHE DE DEMANDE ADMINISTRATIVE')
    pdf.line(20*mm, height-42*mm, width-20*mm, height-42*mm)
    y = height-60*mm
    lines = [
        ('Numéro de demande', demande.numero), ('Date de dépôt', demande.date_demande.strftime('%d/%m/%Y')),
        ('Nom du citoyen', f'{demande.citoyen.prenom} {demande.citoyen.nom}'),
        ('Téléphone', demande.citoyen.telephone or 'Non renseigné'),
        ('Type de demande', demande.get_type_demande_display()), ('Statut', demande.get_statut_display()),
        ('Détails / motif', demande.description or 'Aucun détail fourni'),
    ]
    for label, value in lines:
        pdf.setFont('Helvetica-Bold', 10); pdf.drawString(22*mm, y, f'{label} :')
        pdf.setFont('Helvetica', 10)
        text = str(value)
        if len(text) > 85:
            text = text[:82] + '...'
        pdf.drawString(65*mm, y, text)
        y -= 12*mm
    pdf.setFont('Helvetica-Oblique', 9)
    pdf.drawString(22*mm, 35*mm, 'Document de suivi de demande — ne constitue pas un acte officiel.')
    pdf.drawString(22*mm, 27*mm, f'Édité le {timezone.localdate():%d/%m/%Y}')
    pdf.showPage(); pdf.save()
    return response


def finances(request):
    operations = FinancialTransaction.objects.all()
    recettes = operations.filter(type_operation='RECETTE').aggregate(total=Sum('montant'))['total'] or 0
    depenses = operations.filter(type_operation='DEPENSE').aggregate(total=Sum('montant'))['total'] or 0
    form = FinancialTransactionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Opération financière enregistrée.'); return redirect('finances')
    return render(request, 'dashboard/finances.html', {'operations': operations, 'recettes': recettes, 'depenses': depenses, 'solde': recettes-depenses, 'form': form})


def rapports(request):
    return render(request, 'dashboard/rapports.html', {
        'citoyens_count': Citizen.objects.count(), 'actes_count': CivilRecord.objects.count(),
        'demandes_count': AdministrativeRequest.objects.count(),
        'demandes_traitees': AdministrativeRequest.objects.filter(statut='TRAITEE').count(),
        'demandes_attente': AdministrativeRequest.objects.filter(statut='ATTENTE').count(),
    })


def parametres(request):
    return render(request, 'dashboard/parametres.html')
