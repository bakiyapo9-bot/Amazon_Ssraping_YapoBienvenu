# scraper/parsing.py

from bs4 import BeautifulSoup


def extraire_produits(html):
    """
    Analyse le HTML et extrait les informations des produits.
    """

    soup = BeautifulSoup(html, "html.parser")

    cartes = soup.select(
        "div.a-carousel-container ol.a-carousel > li"
    )

    produits = []

    print(
        f"Nombre de cartes trouvées : {len(cartes)}"
    )

    for carte in cartes:

        lien = carte.find(
            "a",
            {
                "class":
                "a-color-base a-spacing-none a-link-normal _c2Itd_link_j7UN_"
            }
        )

        if not lien:
            continue

        nom_tag = lien.find(
            "span",
            {"class": "a-truncate-full"}
        )

        nom = (
            nom_tag.get_text(strip=True)
            if nom_tag
            else "Nom non trouvé"
        )

        bloc_prix = carte.find(
            "span",
            class_="a-price"
        )

        prix_tag = (
            bloc_prix.find(
                "span",
                class_="a-offscreen"
            )
            if bloc_prix
            else None
        )

        prix = (
            prix_tag.get_text(strip=True)
            if prix_tag
            else "Prix non trouvé"
        )

        img = carte.select_one(
            'img[src*="images/I/"]'
        )

        image = (
            img.get("src")
            if img
            else "Image non trouvée"
        )

        note_tag = carte.find(
            "span",
            {"data-rt": True}
        )

        note = (
            note_tag.get("data-rt")
            if note_tag
            else "Pas de note"
        )

        produit = {
            "nom": nom,
            "prix": prix,
            "image": image,
            "note": note
        }

        produits.append(produit)

    return produits