import time
from pathlib import Path

from app.scraper.driver import creer_driver
from app.scraper.parsing import extraire_produits


# Racine du projet : dossier contenant main.py
BASE_DIR = Path(__file__).resolve().parents[2]


def scraper_produits(url):
    """
    Ouvre Amazon, récupère le HTML et extrait les produits.
    L'animation doit être lancée séparément par l'interface.
    """

    browser = creer_driver()

    try:
        # 1. Ouvrir Amazon
        browser.get(url)

        # 2. Attendre le chargement de la page
        time.sleep(5)

        # 3. Récupérer le HTML
        html = browser.page_source

        # 4. Sauvegarder le HTML pour le débogage
        dossier_data = BASE_DIR / "data"
        dossier_data.mkdir(parents=True, exist_ok=True)

        fichier_html = dossier_data / "page.html"

        with open(fichier_html, "w", encoding="utf-8") as fichier:
            fichier.write(html)

        # 5. Extraire les produits
        produits = extraire_produits(html)

        print("\nScraping terminé !")
        print(f"Produits extraits : {len(produits)}")
        print(f"HTML sauvegardé dans : {fichier_html}")

        return produits

    finally:
        # 6. Toujours fermer le navigateur
        browser.quit()