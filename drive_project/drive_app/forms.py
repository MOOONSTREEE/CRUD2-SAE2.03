from django import forms
from .models import Categorie
from .models import Produit
from .models import Client
from django.forms import inlineformset_factory
from .models import Commande, CommandeProduit

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'descriptif']


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'date_peremption', 'photo', 'marque', 'prix', 'categorie']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse']

CommandeProduitFormSet = inlineformset_factory(
    Commande,
    CommandeProduit,
    fields=('produit', 'quantite'),
    extra=1,
    can_delete=True
)

class ImportProduitForm(forms.Form):
    fichier_csv = forms.FileField(label="Fichier CSV")