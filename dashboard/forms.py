from django import forms
from .models import Citizen, CivilRecord, AdministrativeRequest, FinancialTransaction

class DateInput(forms.DateInput):
    input_type = 'date'

class CitizenForm(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = ['nom', 'prenom', 'sexe', 'date_naissance', 'lieu_naissance', 'telephone', 'adresse', 'numero_piece']
        widgets = {'date_naissance': DateInput()}

class CivilRecordForm(forms.ModelForm):
    class Meta:
        model = CivilRecord
        fields = ['numero_acte', 'type_acte', 'citoyen', 'conjoint', 'date_evenement', 'lieu_evenement', 'observations']
        widgets = {'date_evenement': DateInput(), 'observations': forms.Textarea(attrs={'rows': 3})}

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('type_acte') == 'MARIAGE' and not cleaned.get('conjoint'):
            self.add_error('conjoint', 'Veuillez sélectionner le conjoint ou la conjointe pour un mariage.')
        if cleaned.get('type_acte') != 'MARIAGE':
            cleaned['conjoint'] = None
        return cleaned

class AdministrativeRequestForm(forms.ModelForm):
    class Meta:
        model = AdministrativeRequest
        fields = ['citoyen', 'type_demande', 'description', 'statut', 'date_demande']
        widgets = {'date_demande': DateInput(), 'description': forms.Textarea(attrs={'rows': 3})}

class FinancialTransactionForm(forms.ModelForm):
    class Meta:
        model = FinancialTransaction
        fields = ['libelle', 'type_operation', 'montant', 'date_operation', 'reference', 'observations']
        widgets = {'date_operation': DateInput(), 'observations': forms.Textarea(attrs={'rows': 3})}
