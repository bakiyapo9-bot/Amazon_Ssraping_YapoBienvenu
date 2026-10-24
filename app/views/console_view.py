
def afficher_produits(produits):

    if not produits:
        print(
            "\nAucun produit."
            "Lance d'abord le scraping."
        )
        return

    for produit in produits:

        print("\nNom   :", produit["nom"])
        print("Prix  :", produit["prix"])
        print("Note  :", produit["note"])
        print("Image :", produit["image"])

        print("-" * 50)