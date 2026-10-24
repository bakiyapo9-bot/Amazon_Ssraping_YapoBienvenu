from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
TECH_DIR = DATA_DIR / "tech"
TELEPHONES_DIR = TECH_DIR / "telephones"
IPHONE_DIR = TELEPHONES_DIR / "iphone"

IMAGES_DIR = IPHONE_DIR / "images"
NOM_DIR = IPHONE_DIR / "nom"
PRIX_DIR = IPHONE_DIR / "prix"
NOTE_DIR = IPHONE_DIR / "note"

DATA_CSV = IPHONE_DIR / "data.csv"
RESULTAT_CSV = DATA_DIR / "resultat.csv"

def creer_dossiers():
    for dossier in (
        IMAGES_DIR,
        NOM_DIR,
        PRIX_DIR,
        NOTE_DIR,
    ):
        dossier.mkdir(parents=True, exist_ok=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)