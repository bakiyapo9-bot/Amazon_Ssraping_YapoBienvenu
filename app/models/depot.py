import csv
from config import (
    creer_dossiers,
    IMAGES_DIR,
    NOM_DIR,
    PRIX_DIR,
    NOTE_DIR,
    DATA_CSV,
    RESULTAT_CSV
)

CHAMPS = ["nom", "prix", "image", "note"]

def enregistrer_information(chemin, valeur):
    chemin.write_text(
        str(valeur or ""),
        encoding="utf-8",
    )

def enregistrer_produits(produits):
    creer_dossiers()

    # Évite de conserver les anciens fichiers individuels.
    for dossier, prefixe in (
        (NOM_DIR, "nom"),
        (PRIX_DIR, "prix"),
        (IMAGES_DIR, "image"),
        (NOTE_DIR, "note"),
    ):
        for fichier in dossier.glob(f"{prefixe}[0-9]*"):
            if fichier.is_file():
                fichier.unlink()

    for i, produit in enumerate(produits, start=1):
        enregistrer_information(
            NOM_DIR / f"nom{i}", produit.get("nom", "")
        )
        enregistrer_information(
            PRIX_DIR / f"prix{i}", produit.get("prix", "")
        )
        enregistrer_information(
            IMAGES_DIR / f"image{i}", produit.get("image", "")
        )
        enregistrer_information(
            NOTE_DIR / f"note{i}", produit.get("note", "")
        )

    for chemin in (DATA_CSV, RESULTAT_CSV):
        with chemin.open(
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as fichier:
            writer = csv.DictWriter(
                fichier,
                fieldnames=CHAMPS,
                delimiter=";",
                extrasaction="ignore",
            )
            writer.writeheader()
            writer.writerows(produits)

    return len(produits)

def charger_produits():
    if not DATA_CSV.exists():
        return []

    with DATA_CSV.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as fichier:
        return list(csv.DictReader(fichier, delimiter=";"))