# models/produit.py

class Produit:
    def __init__(self, nom, prix, image, note):
        self.nom = nom
        self.prix = prix
        self.image = image
        self.note = note

    def vers_dictionnaire(self):
        return {
            "nom": self.nom,
            "prix": self.prix,
            "image": self.image,
            "note": self.note
        }