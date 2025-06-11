from django.urls import path
from .views import (
    # Catégories
    CategorieListView, CategorieCreateView,
    CategorieUpdateView, CategorieDeleteView,

    # Produits
    ProduitListView, ProduitCreateView,
    ProduitUpdateView, ProduitDeleteView,

    # Clients
    ClientListView, ClientCreateView,
    ClientUpdateView, ClientDeleteView,

    #Commande
    commande_create, CommandeListView,
    CommandeDetailView,
)

urlpatterns = [
    # Catégories
    path('categories/', CategorieListView.as_view(), name='categorie_list'),
    path('categories/add/', CategorieCreateView.as_view(), name='categorie_add'),
    path('categories/<int:pk>/edit/', CategorieUpdateView.as_view(), name='categorie_edit'),
    path('categories/<int:pk>/delete/', CategorieDeleteView.as_view(), name='categorie_delete'),

    # Produits
    path('produits/', ProduitListView.as_view(), name='produit_list'),
    path('produits/add/', ProduitCreateView.as_view(), name='produit_add'),
    path('produits/<int:pk>/edit/', ProduitUpdateView.as_view(), name='produit_edit'),
    path('produits/<int:pk>/delete/', ProduitDeleteView.as_view(), name='produit_delete'),


    # Clients

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),


    # Commandes

    path('commandes/', CommandeListView.as_view(), name='commande_list'),
    path('commandes/add/', commande_create, name='commande_add'),
    path('commandes/<int:pk>/', CommandeDetailView.as_view(), name='commande_detail')

]
