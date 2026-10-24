from app.scraper.amazon_scraper import scraper_produits
from app.models.depot import enregistrer_produits


def lancer_scraping(url):
   
    produits = scraper_produits(url)

    if produits:
        enregistrer_produits(produits)

    return produits