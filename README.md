# Amazon Scraper

Projet d'extraction de données (Scraping) Amazon structuré selon une architecture modulaire MVC (Modèle-Vue-Contrôleur).

# Architecture du projet
Amazon_Scrapping/
│
├── README.md
├── requirements.txt
├── main.py
├── config.py
│
├── app/
│   ├── __init__.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── scraping_controller.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── produit.py
│   │   ├── depot.py
│   │   └── base_donnees.py
│   │
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── amazon_scraper.py
│   │   ├── driver.py
│   │   └── parsing.py
│   │
│   └── views/
│       ├── __init__.py
│       ├── interface.py
│       ├── console_view.py
│       └── export_view.py
│
└── data/
    ├── datalab.db
    ├── resultat.csv
    │
    └── tech/
        └── telephones/
            └── iphone/
                ├── data.csv
                ├── images/
                ├── nom/
                ├── prix/
                └── note/
