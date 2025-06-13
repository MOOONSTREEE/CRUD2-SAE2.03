from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
import io
from .models import Categorie, Produit, Client, Commande, CommandeProduit
from .forms import (
    CategorieForm, ProduitForm, ClientForm,
    CommandeForm, CommandeProduitFormSet,
    ImportProduitForm, SelectionCommandeForm,
)
import csv

# --- Catégories ---
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


# --- Produits ---
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


# --- Clients ---
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


# --- Commandes ---
class CommandeListView(ListView):
    model = Commande
    template_name = 'drive_app/commande_list.html'

class CommandeDetailView(DetailView):
    model = Commande
    template_name = 'drive_app/fiche_commande.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = CommandeProduit.objects.filter(commande=self.object)
        total = sum(item.produit.prix * item.quantite for item in items)
        context.update({
            'items': items,
            'total': total
        })
        return context


def commande_create(request):
    # On prépare toujours une instance vide pour le formset
    empty_commande = Commande()

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        # On passe l'instance après avoir sauvegardé le form,
        # mais on peut d'emblée lier le POST à notre instance vide
        formset = CommandeProduitFormSet(request.POST, instance=empty_commande)

        if form.is_valid() and formset.is_valid():
            # Sauvegarde du parent
            commande = form.save()
            # On relie et sauve les lignes enfants
            formset.instance = commande
            formset.save()
            return redirect('commande_detail', pk=commande.pk)
    else:
        form = CommandeForm()
        formset = CommandeProduitFormSet(instance=empty_commande)

    return render(request, 'drive_app/commande_form.html', {
        'form': form,
        'formset': formset
    })


def commande_edit(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form    = CommandeForm(request.POST, instance=commande)
        formset = CommandeProduitFormSet(request.POST, instance=commande)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # ← redirection vers la liste des commandes après enregistrement
            return redirect('commande_list')
    else:
        form    = CommandeForm(instance=commande)
        formset = CommandeProduitFormSet(instance=commande)

    return render(request, 'drive_app/commande_form.html', {
        'form': form,
        'formset': formset
    })


def commande_delete(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('commande_list')
    return render(request, 'drive_app/commande_confirm_delete.html', {
        'commande': commande
    })


# --- Accueil & Import CSV ---
def accueil(request):
    return render(request, 'drive_app/accueil.html')


# drive_app/views.py

def importer_produits(request):
    """
    Importe des produits depuis un CSV. Pour chaque ligne :
    - télécharge l'image depuis la colonne 'photo' (URL)
    - crée/récupère la catégorie
    - crée le produit dans la base
    """
    if request.method == 'POST':
        form = ImportProduitForm(request.POST, request.FILES)
        if form.is_valid():
            # Lecture + nettoyage du BOM
            raw_data = form.cleaned_data['fichier_csv'].read().decode('utf-8-sig')
            lines = raw_data.splitlines()
            if not lines:
                messages.error(request, "Le fichier CSV est vide.")
                return redirect('importer_produits')

            # Détection du séparateur sur le header
            delimiter = ';' if ';' in lines[0] else ','

            stream = io.StringIO(raw_data)
            reader = csv.DictReader(stream, delimiter=delimiter)

            expected = {'nom', 'date_peremption', 'photo', 'marque', 'prix', 'categorie'}
            if not reader.fieldnames:
                messages.error(request, "Header CSV introuvable ou mal formé.")
                return redirect('importer_produits')

            missing = expected - set(reader.fieldnames)
            if missing:
                messages.error(
                    request,
                    f"Colonnes manquantes : {', '.join(missing)} (séparateur détecté : {repr(delimiter)})"
                )
                return redirect('importer_produits')

            created = 0
            for idx, row in enumerate(reader, start=1):
                # Nettoyage des champs
                nom_raw    = row['nom'].strip()
                if not nom_raw:
                    messages.warning(request, f"Ligne {idx} ignorée (nom vide).")
                    continue

                date_raw   = row['date_peremption'].strip() or None
                photo_url  = row['photo'].strip()
                marque_raw = row['marque'].strip() or "Inconnue"
                prix_raw   = row['prix'].strip() or "0"
                cat_nom    = row['categorie'].strip() or "Sans catégorie"

                # Crée ou récupère la catégorie
                cat_obj, _ = Categorie.objects.get_or_create(nom=cat_nom)

                # Prépare l'instance Produit (sans sauvegarder)
                produit = Produit(
                    nom             = nom_raw,
                    date_peremption = date_raw,
                    marque          = marque_raw,
                    prix            = prix_raw,
                    categorie       = cat_obj
                )

                # Si une URL d'image est fournie, on la télécharge et on l'enregistre
                if photo_url:
                    try:
                        resp = requests.get(photo_url, timeout=5)
                        resp.raise_for_status()
                        # Extrait un nom de fichier de l'URL
                        filename = urlparse(photo_url).path.split('/')[-1] or 'image'
                        # Sauvegarde dans le champ ImageField sans committer tout de suite
                        produit.photo.save(
                            filename,
                            ContentFile(resp.content),
                            save=False
                        )
                    except Exception as e:
                        messages.warning(request,
                            f"Ligne {idx} : impossible de télécharger l'image ({e}). Ignorée."
                        )

                # Sauvegarde définitive
                try:
                    produit.save()
                    created += 1
                except Exception as e:
                    messages.error(request,
                        f"Ligne {idx} : impossible de créer le produit ({e})."
                    )

            # Retour utilisateur
            if created:
                messages.success(request, f"{created} produit(s) importé(s) avec succès.")
            else:
                messages.info(request, "Aucun produit importé.")
            return redirect('produit_list')
    else:
        form = ImportProduitForm()

    return render(request, 'drive_app/importer.html', {'form': form})



def selection_commande(request):
    """
    Affiche un formulaire pour saisir l'ID d'une commande et redirige vers sa fiche.
    """
    if request.method == 'POST':
        form = SelectionCommandeForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data['commande_id']
            # Vérifie qu'elle existe, sinon 404
            get_object_or_404(Commande, pk=pk)
            return redirect('commande_detail', pk=pk)
    else:
        form = SelectionCommandeForm()

    return render(request, 'drive_app/selection_commande.html', {
        'form': form
    })
