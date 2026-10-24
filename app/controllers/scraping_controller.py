from app.scraper.amazon_scraper import scraper_produits
from app.models.depot import enregistrer_produits


def lancer_scraping(url):
    """
    Lance le scraping puis enregistre les produits.
    """

    produits = scraper_produits(url)

    if produits:
        enregistrer_produits(produits)

    return produits