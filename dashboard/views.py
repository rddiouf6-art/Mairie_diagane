
from django.shortcuts import render


def accueil(request):
    """
    Affiche la page d'accueil de la plateforme municipale.
    """
    return render(request, 'accueil.html')
