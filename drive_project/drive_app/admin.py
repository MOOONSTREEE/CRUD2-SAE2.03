from django.contrib import admin
from .models import Categorie, Produit, Client, Commande, CommandeProduit

admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Client)
admin.site.register(Commande)
admin.site.register(CommandeProduit)
