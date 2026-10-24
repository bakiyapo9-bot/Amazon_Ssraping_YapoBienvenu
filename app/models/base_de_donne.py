import sqlite3
from config import DATA_DIR


DB_PATH = DATA_DIR / "datalab.db"


def connexion():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialiser_base():
    with connexion() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prix TEXT,
                note TEXT,
                image TEXT,
                UNIQUE(nom, image)
            )
        """)


def charger_depuis_base():
    initialiser_base()
    with connexion() as conn:
        lignes = conn.execute(
            "SELECT nom, prix, note, image FROM produits ORDER BY id DESC"
        ).fetchall()
    return [dict(ligne) for ligne in lignes]


def enregistrer_dans_base(produits):
    initialiser_base()
    with connexion() as conn:
        for produit in produits:
            nom = str(produit.get("nom") or "").strip()
            if not nom:
                continue
            conn.execute("""
                INSERT INTO produits (nom, prix, note, image)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(nom, image) DO UPDATE SET
                    prix = excluded.prix,
                    note = excluded.note
            """, (
                nom,
                str(produit.get("prix") or ""),
                str(produit.get("note") or ""),
                str(produit.get("image") or ""),
            ))
