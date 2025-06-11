from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Categorie
from .forms import CategorieForm
from .models import Produit
from .forms import ProduitForm
from .models import Client
from .forms import ClientForm
from django.shortcuts import render, redirect
from .models import Commande, CommandeProduit
from .forms import CommandeProduitFormSet
from django.forms import ModelForm

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
    template_name = 'drive_app/commande_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = sum(
            item.produit.prix * item.quantite
            for item in self.object.commandeproduit_set.all()
        )
        context['total'] = total
        return context