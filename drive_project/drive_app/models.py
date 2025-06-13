from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    descriptif = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    date_peremption = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to='photos/',
        null=True,
        blank=True
    )
    marque = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"{self.nom} ({self.marque})"

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_inscription = models.DateField(auto_now_add=True)
    adresse = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

