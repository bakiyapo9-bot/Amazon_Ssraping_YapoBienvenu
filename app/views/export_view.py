import csv
from config import RESULTAT_CSV

def exporter_csv(produits):
    if not produits:
        print("Aucun produit à exporter.")
        return

    RESULTAT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with open(RESULTAT_CSV, "w", newline="", encoding="utf-8-sig") as fichier:
        champs = ["nom", "prix", "image", "note"]
        writer = csv.DictWriter(
            fichier,
            fieldnames=champs,
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(produits)

    print(f"Fichier CSV créé avec succès : {RESULTAT_CSV}")