from django.contrib import admin
from .models import Citizen, CivilRecord, AdministrativeRequest, FinancialTransaction

@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe', 'telephone', 'adresse')
    search_fields = ('nom', 'prenom', 'telephone', 'numero_piece')

@admin.register(CivilRecord)
class CivilRecordAdmin(admin.ModelAdmin):
    list_display = ('numero_acte', 'type_acte', 'citoyen', 'date_evenement', 'lieu_evenement')
    list_filter = ('type_acte', 'date_evenement')
    search_fields = ('numero_acte', 'citoyen__nom', 'citoyen__prenom')

@admin.register(AdministrativeRequest)
class AdministrativeRequestAdmin(admin.ModelAdmin):
    list_display = ('numero', 'citoyen', 'type_demande', 'statut', 'date_demande')
    list_filter = ('statut', 'type_demande', 'date_demande')
    search_fields = ('numero', 'citoyen__nom', 'citoyen__prenom')

@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'type_operation', 'montant', 'date_operation')
    list_filter = ('type_operation', 'date_operation')
