from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('citoyens/', views.citoyens_liste, name='citoyens'),
    path('citoyens/ajouter/', views.citoyen_ajouter, name='citoyen_ajouter'),
    path('citoyens/<int:pk>/modifier/', views.citoyen_modifier, name='citoyen_modifier'),
    path('citoyens/<int:pk>/supprimer/', views.citoyen_supprimer, name='citoyen_supprimer'),
    path('etat-civil/', views.etat_civil, name='etat_civil'),
    path('etat-civil/ajouter/', views.acte_ajouter, name='acte_ajouter'),
    path('etat-civil/<int:pk>/modifier/', views.acte_modifier, name='acte_modifier'),
    path('etat-civil/<int:pk>/supprimer/', views.acte_supprimer, name='acte_supprimer'),
    path('demandes/', views.demandes_liste, name='demandes'),
    path('demandes/ajouter/', views.demande_ajouter, name='demande_ajouter'),
    path('demandes/<int:pk>/modifier/', views.demande_modifier, name='demande_modifier'),
    path('demandes/<int:pk>/supprimer/', views.demande_supprimer, name='demande_supprimer'),
    path('demandes/<int:pk>/pdf/', views.demande_pdf, name='demande_pdf'),
    path('finances/', views.finances, name='finances'),
    path('rapports/', views.rapports, name='rapports'),
    path('parametres/', views.parametres, name='parametres'),
]
