from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Categorie
from .forms import CategorieForm
from .models import Produit
from .forms import ProduitForm
from .models import Client
from .forms import ClientForm
from .models import Commande, CommandeProduit
from .forms import CommandeProduitFormSet
from django.forms import ModelForm
import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImportProduitForm

class CategorieListView(ListView):
    model = Categorie
    template_name = 'drive_app/categorie_list.html'

class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'drive_app/categorie_form.html'
    success_url = reverse_lazy('categorie_list')

class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'drive_app/categorie_form.html'
    success_url = reverse_lazy('categorie_list')

class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = 'drive_app/categorie_confirm_delete.html'
    success_url = reverse_lazy('categorie_list')


class ProduitListView(ListView):
    model = Produit
    template_name = 'drive_app/produit_list.html'

class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'drive_app/produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'drive_app/produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'drive_app/produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')

class ClientListView(ListView):
    model = Client
    template_name = 'drive_app/client_list.html'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'drive_app/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'drive_app/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'drive_app/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

class CommandeForm(ModelForm):
    class Meta:
        model = Commande
        fields = ['client']

def commande_create(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        formset = CommandeProduitFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            commande = form.save()
            formset.instance = commande
            formset.save()
            return redirect('commande_detail', pk=commande.pk)
    else:
        form = CommandeForm()
        formset = CommandeProduitFormSet()
    return render(request, 'drive_app/commande_form.html', {'form': form, 'formset': formset})

class CommandeListView(ListView):
    model = Commande
    template_name = 'drive_app/commande_list.html'

class CommandeDetailView(DetailView):
    model = Commande
    template_name = 'drive_app/fiche_commande.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commande = self.get_object()
        items = CommandeProduit.objects.filter(commande=commande)
        total = sum(item.produit.prix * item.quantite for item in items)
        context['items'] = items
        context['total'] = total
        return context

def accueil(request):
    return render(request, 'drive_app/accueil.html')

def importer_produits(request):
    if request.method == 'POST':
        form = ImportProduitForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['fichier_csv']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                categorie_obj, _ = Categorie.objects.get_or_create(nom=row['categorie'])
                Produit.objects.create(
                    nom=row['nom'],
                    date_peremption=row['date_peremption'],
                    marque=row['marque'],
                    prix=row['prix'],
                    categorie=categorie_obj
                )
            messages.success(request, "Importation réussie.")
            return redirect('produit_list')
    else:
        form = ImportProduitForm()

    return render(request, 'drive_app/importer.html', {'form': form})