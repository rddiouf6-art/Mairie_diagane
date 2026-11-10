from django.db import models
from django.utils import timezone


class Citizen(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    nom = models.CharField('Nom', max_length=100)
    prenom = models.CharField('Prénom', max_length=100)
    sexe = models.CharField('Sexe', max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField('Date de naissance', null=True, blank=True)
    lieu_naissance = models.CharField('Lieu de naissance', max_length=150, blank=True)
    telephone = models.CharField('Téléphone', max_length=30, blank=True)
    adresse = models.CharField('Adresse / village', max_length=200, blank=True)
    numero_piece = models.CharField('N° pièce d’identité', max_length=80, blank=True)
    created_at = models.DateTimeField('Date d’enregistrement', auto_now_add=True)

    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = 'Citoyen'
        verbose_name_plural = 'Citoyens'

    def __str__(self):
        return f'{self.prenom} {self.nom}'


class CivilRecord(models.Model):
    TYPE_CHOICES = [('NAISSANCE', 'Naissance'), ('MARIAGE', 'Mariage'), ('DECES', 'Décès')]
    numero_acte = models.CharField('Numéro de l’acte', max_length=60, unique=True)
    type_acte = models.CharField('Type d’acte', max_length=12, choices=TYPE_CHOICES)
    citoyen = models.ForeignKey(Citizen, on_delete=models.PROTECT, related_name='actes', verbose_name='Citoyen principal')
    conjoint = models.ForeignKey(Citizen, on_delete=models.PROTECT, null=True, blank=True, related_name='mariages', verbose_name='Conjoint(e)')
    date_evenement = models.DateField('Date de l’événement')
    lieu_evenement = models.CharField('Lieu de l’événement', max_length=180)
    observations = models.TextField('Observations', blank=True)
    created_at = models.DateTimeField('Date de saisie', auto_now_add=True)

    class Meta:
        ordering = ['-date_evenement', '-id']
        verbose_name = 'Acte d’état civil'
        verbose_name_plural = 'Actes d’état civil'

    def __str__(self):
        return f'{self.get_type_acte_display()} – {self.numero_acte}'


class AdministrativeRequest(models.Model):
    TYPE_CHOICES = [
        ('RESIDENCE', 'Certificat de résidence'),
        ('NAISSANCE', 'Copie / extrait d’acte de naissance'),
        ('MARIAGE', 'Copie / extrait d’acte de mariage'),
        ('DECES', 'Copie / extrait d’acte de décès'),
        ('LEGALISATION', 'Légalisation de document'),
        ('AUTRE', 'Autre demande'),
    ]
    STATUS_CHOICES = [('ATTENTE', 'En attente'), ('EN_COURS', 'En cours'), ('TRAITEE', 'Traitée'), ('REJETEE', 'Rejetée')]
    numero = models.CharField('Numéro de demande', max_length=30, unique=True, blank=True)
    citoyen = models.ForeignKey(Citizen, on_delete=models.PROTECT, related_name='demandes', verbose_name='Citoyen')
    type_demande = models.CharField('Type de demande', max_length=20, choices=TYPE_CHOICES)
    description = models.TextField('Détails / motif', blank=True)
    statut = models.CharField('Statut', max_length=12, choices=STATUS_CHOICES, default='ATTENTE')
    date_demande = models.DateField('Date de demande', default=timezone.localdate)
    updated_at = models.DateTimeField('Dernière mise à jour', auto_now=True)

    class Meta:
        ordering = ['-date_demande', '-id']
        verbose_name = 'Demande administrative'
        verbose_name_plural = 'Demandes administratives'

    def save(self, *args, **kwargs):
        if not self.numero:
            super().save(*args, **kwargs)
            self.numero = f'DB-{self.date_demande:%Y%m%d}-{self.pk:04d}'
            return super().save(update_fields=['numero'])
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.numero or f'Demande {self.pk}'


class FinancialTransaction(models.Model):
    TYPE_CHOICES = [('RECETTE', 'Recette'), ('DEPENSE', 'Dépense')]
    libelle = models.CharField('Libellé', max_length=180)
    type_operation = models.CharField('Type', max_length=8, choices=TYPE_CHOICES)
    montant = models.DecimalField('Montant (FCFA)', max_digits=14, decimal_places=2)
    date_operation = models.DateField('Date', default=timezone.localdate)
    reference = models.CharField('Référence', max_length=80, blank=True)
    observations = models.TextField('Observations', blank=True)

    class Meta:
        ordering = ['-date_operation', '-id']
        verbose_name = 'Opération financière'
        verbose_name_plural = 'Opérations financières'

    def __str__(self):
        return f'{self.libelle} – {self.montant} FCFA'
