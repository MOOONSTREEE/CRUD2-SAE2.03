from django import forms
from django.forms import inlineformset_factory
from django.forms import ClearableFileInput
from .models import (
    Categorie,
    Produit,
    Client,
    Commande,
    CommandeProduit
)

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'descriptif']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'date_peremption', 'photo', 'marque', 'prix', 'categorie']
        widgets = {
            'photo': forms.ClearableFileInput(),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse']

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['client']

# Inline formset pour gérer les produits d'une commande
CommandeProduitFormSet = inlineformset_factory(
    parent_model=Commande,
    model=CommandeProduit,
    fields=['produit', 'quantite'],
    extra=1,
    can_delete=True
)

class ImportProduitForm(forms.Form):
    fichier_csv = forms.FileField(label="Fichier CSV")

class SelectionCommandeForm(forms.Form):
    commande_id = forms.IntegerField(
        label="Numéro de commande",
        min_value=1,
        help_text="Entrez l'ID de la commande à consulter"
    )