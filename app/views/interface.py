
import os
import threading
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

from app.controllers.scraping_controller import lancer_scraping
from app.models.depot import charger_produits, enregistrer_produits
from config import DATA_DIR, IPHONE_DIR, RESULTAT_CSV
from app.models.base_de_donne import (
    initialiser_base, charger_depuis_base, enregistrer_dans_base
)


# Couleurs
BLANC = "#FFFFFF"
CIEL = "#EAF5FF"
BLEU = "#2563EB"
BLEU_SURVOL = "#1D4ED8"
TEXTE = "#172033"
GRIS = "#64748B"
VERT = "#059669"
ROUGE = "#DC2626"
POLICE = "Segoe UI"


def etiquette(parent, texte, couleur=GRIS, taille=13, gras=False, **options):
    label = ctk.CTkLabel(
        parent,
        text=texte,
        text_color=couleur,
        font=(POLICE, taille, "bold" if gras else "normal"),
    )
    options.setdefault("anchor", "w")
    label.pack(**options)
    return label


def nombre_prix(texte):
    for caractere in ("\u202f", "\xa0", " ", "€"):
        texte = texte.replace(caractere, "")
    return float(texte.replace(",", "."))


def nombre_note(texte):
    return float(texte.replace(",", ".").split()[0])


def nombres_produits(produits, champ, conversion):
    nombres = []
    for produit in produits:
        try:
            nombres.append(conversion(str(produit.get(champ, ""))))
        except (ValueError, IndexError):
            pass
    return nombres


class AmazonScrapingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("DATALAB | Amazon Scraping")
        self.geometry("1200x760")
        self.minsize(950, 620)
        self.configure(fg_color=BLANC)

        initialiser_base()
        # Au premier lancement, importer les anciens produits CSV dans SQLite.
        self.produits = charger_depuis_base()
        if not self.produits:
            self.produits = charger_produits()
            if self.produits:
                enregistrer_dans_base(self.produits)
        self.zone = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        self.creer_menu()
        self.zone.pack(side="left", fill="both", expand=True, padx=28, pady=25)
        self.dashboard()

    def creer_menu(self):
        menu = ctk.CTkFrame(self, width=230, fg_color=CIEL, corner_radius=0)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)

        etiquette(menu, "◈  DATA LAB", BLEU, 24, True, padx=22, pady=(30, 4))
        etiquette(menu, "AMAZON SCRAPING", GRIS, 11, True, padx=24, pady=(0, 30))

        pages = [
            ("⌂", "Tableau de bord", self.dashboard),
            ("⌕", "Scraping", self.page_scraping),
            ("▦", "Catalogue", self.page_catalogue),
            ("⇩", "Export CSV", self.page_export),
        ]
        for icone, texte, action in pages:
            ctk.CTkButton(
                menu, text=f"{icone}   {texte}", anchor="w", height=44,
                fg_color="transparent", hover_color="#D4E9FF",
                text_color=TEXTE, font=(POLICE, 14), command=action,
            ).pack(fill="x", padx=12, pady=4)

        etiquette(
            menu, "PROJET PYTHON\nSelenium • BeautifulSoup", GRIS, 11,
            side="bottom", padx=22, pady=24
        )

    def vider_page(self):
        for widget in self.zone.winfo_children():
            widget.destroy()

    def titre(self, texte, description):
        etiquette(self.zone, texte, TEXTE, 28, True)
        etiquette(self.zone, description, GRIS, 13, pady=(4, 22))

    def bouton(self, texte, commande, **options):
        bouton = ctk.CTkButton(
            self.zone, text=texte, command=commande, height=44,
            fg_color=BLEU, hover_color=BLEU_SURVOL,
            font=(POLICE, 13, "bold"),
        )
        options.setdefault("pady", 10)
        bouton.pack(anchor="w", **options)
        return bouton

    def carte(self, parent, titre, valeur, detail):
        bloc = ctk.CTkFrame(parent, fg_color=CIEL, corner_radius=14)
        bloc.pack(side="left", fill="both", expand=True, padx=(0, 12))
        etiquette(bloc, titre, GRIS, 12, padx=16, pady=(16, 5))
        etiquette(bloc, valeur, TEXTE, 25, True, padx=16)
        etiquette(bloc, detail, BLEU, 11, padx=16, pady=(4, 15))

    def dashboard(self):
        self.vider_page()
        self.titre("Tableau de bord", "Résumé de vos produits collectés.")

        prix = nombres_produits(self.produits, "prix", nombre_prix)
        notes = nombres_produits(self.produits, "note", nombre_note)
        prix_moyen = f"{sum(prix) / len(prix):.2f} €" if prix else "—"
        meilleure_note = f"{max(notes):g}/5" if notes else "—"

        stats = ctk.CTkFrame(self.zone, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 22))
        self.carte(stats, "PRODUITS COLLECTÉS", len(self.produits), "Catalogue enregistré")
        self.carte(stats, "PRIX MOYEN", prix_moyen, "Prix interprétables")
        self.carte(stats, "MEILLEURE NOTE", meilleure_note, "Note maximale trouvée")

        etiquette(self.zone, "Derniers produits", TEXTE, 19, True, pady=(5, 10))
        if not self.produits:
            etiquette(self.zone, "Aucun produit. Lance ton premier scraping.", pady=15)

        for produit in self.produits[:5]:
            ligne = ctk.CTkFrame(self.zone, fg_color=CIEL, corner_radius=10)
            ligne.pack(fill="x", pady=4)
            ctk.CTkLabel(
                ligne, text=produit.get("nom") or "Sans nom",
                text_color=TEXTE, anchor="w", wraplength=520,
                font=(POLICE, 12),
            ).pack(side="left", fill="x", expand=True, padx=13, pady=12)
            etiquette(
                ligne, produit.get("prix") or "—", VERT, 12, True,
                side="right", padx=13, anchor="center"
            )
        self.bouton("＋  Lancer un scraping", self.page_scraping)

    def page_scraping(self):
        self.vider_page()
        self.titre("Nouveau scraping", "Saisis l’adresse de la page à analyser.")

        formulaire = ctk.CTkFrame(self.zone, fg_color=CIEL, corner_radius=14)
        formulaire.pack(fill="x", pady=8)
        etiquette(formulaire, "URL du site web", TEXTE, 14, True,
                  padx=20, pady=(20, 8))

        self.url = ctk.CTkEntry(
            formulaire, height=45, placeholder_text="https://www.amazon.fr/..."
        )
        self.url.pack(fill="x", padx=20, pady=(0, 15))
        self.url.insert(0, "https://www.amazon.fr/s?k=iphone")

        self.btn_scraping = ctk.CTkButton(
            formulaire, text="▶  Démarrer la collecte", height=44,
            fg_color=BLEU, hover_color=BLEU_SURVOL,
            command=self.demarrer_scraping,
        )
        self.btn_scraping.pack(anchor="w", padx=20, pady=(0, 20))

        self.progression = ctk.CTkProgressBar(self.zone, progress_color=BLEU)
        self.progression.pack(fill="x", pady=(20, 8))
        self.progression.set(0)
        self.statut = etiquette(self.zone, "En attente du lancement.")
        ctk.CTkLabel(
            self.zone,
            text="Les données seront enregistrées dans data/tech/telephones/iphone/ et data/resultat.csv.",
            text_color=GRIS, wraplength=700, justify="left",
        ).pack(anchor="w", pady=20)

    def demarrer_scraping(self):
        url = self.url.get().strip()
        if not url.startswith(("http://", "https://")):
            messagebox.showerror(
                "URL invalide",
                "L'adresse doit commencer par http:// ou https://."
            )
            return

        self.url_a_scraper = url
        self.btn_scraping.configure(state="disabled", text="Collecte en cours...")
        self.progression.configure(mode="indeterminate")
        self.progression.start()
        self.statut.configure(text="Connexion à Amazon en cours…", text_color=BLEU)

        threading.Thread(
            target=self.executer_scraping,
            args=(url,),
            daemon=True,
        ).start()

    def executer_scraping(self, url):
        try:
            produits = lancer_scraping(url)
            self.after(0, lambda: self.fin_scraping(produits, None))
        except Exception as erreur:
            message = str(erreur)
            self.after(0, lambda message=message: self.fin_scraping(None, message))

    def fin_scraping(self, produits, erreur):
        self.progression.stop()
        self.progression.configure(mode="determinate")
        self.progression.set(0 if erreur else 1)
        self.btn_scraping.configure(state="normal", text="▶  Démarrer la collecte")

        if erreur:
            self.statut.configure(text="La collecte a échoué.", text_color=ROUGE)
            messagebox.showerror("Erreur de scraping", erreur)
            return

        nouveaux_produits = produits or []
        try:
            enregistrer_dans_base(nouveaux_produits)
            self.produits = charger_depuis_base()
        except Exception as erreur_base:
            self.statut.configure(text="Erreur d’enregistrement SQLite.", text_color=ROUGE)
            messagebox.showerror("Erreur SQLite", str(erreur_base))
            self.produits = nouveaux_produits
        self.statut.configure(
            text=f"Collecte terminée : {len(self.produits)} produit(s).",
            text_color=VERT,
        )

        try:
            enregistrer_produits(self.produits)
        except Exception as erreur_export:
            messagebox.showwarning(
                "Enregistrement",
                f"Les produits ont été récupérés, mais l'enregistrement a échoué :\n{erreur_export}",
            )

        messagebox.showinfo(
            "Scraping terminé",
            f"{len(self.produits)} produit(s) récupéré(s)."
        )

    def page_catalogue(self):
        self.vider_page()
        self.titre(
            "Catalogue des produits",
            f"{len(self.produits)} produit(s) enregistrés."
        )
        recherche = ctk.CTkEntry(
            self.zone, placeholder_text="Rechercher un produit…", height=42
        )
        recherche.pack(fill="x", pady=(0, 12))
        liste = ctk.CTkScrollableFrame(self.zone, fg_color="transparent")
        liste.pack(fill="both", expand=True)

        def remplir(terme=""):
            for widget in liste.winfo_children():
                widget.destroy()
            trouves = [
                produit for produit in self.produits
                if terme.lower() in (produit.get("nom") or "").lower()
            ]
            if not trouves:
                etiquette(liste, "Aucun produit correspondant.", pady=25, anchor="center")
            for produit in trouves:
                self.fiche_produit(liste, produit)

        recherche.bind("<KeyRelease>", lambda event: remplir(recherche.get()))
        remplir()

    def fiche_produit(self, parent, produit):
        bloc = ctk.CTkFrame(parent, fg_color=CIEL, corner_radius=12)
        bloc.pack(fill="x", pady=5)
        ctk.CTkLabel(
            bloc, text=produit.get("nom") or "Sans nom",
            text_color=TEXTE, font=(POLICE, 13, "bold"),
            anchor="w", wraplength=650, justify="left",
        ).pack(fill="x", padx=15, pady=(12, 5))
        ctk.CTkLabel(
            bloc,
            text=f"Prix : {produit.get('prix') or '—'}     Note : {produit.get('note') or '—'}",
            text_color=BLEU, anchor="w",
        ).pack(fill="x", padx=15, pady=3)
        ctk.CTkButton(
            bloc, text="Ouvrir l’image ↗", width=130, height=30,
            fg_color=BLANC, hover_color="#D4E9FF", text_color=BLEU,
            command=lambda: self.ouvrir_url(produit.get("image")),
        ).pack(anchor="w", padx=15, pady=(5, 12))

    @staticmethod
    def ouvrir_url(url):
        if url and url.startswith(("http://", "https://")):
            webbrowser.open(url)

    def page_export(self):
        self.vider_page()
        self.titre("Export des données", "Les produits sont conservés dans SQLite et exportables en CSV.")
        fichiers = [
            ("CSV de la catégorie iPhone", IPHONE_DIR / "data.csv"),
            ("CSV récapitulatif", RESULTAT_CSV),
        ]

        for titre, chemin in fichiers:
            bloc = ctk.CTkFrame(self.zone, fg_color=CIEL, corner_radius=12)
            bloc.pack(fill="x", pady=7)
            etiquette(bloc, titre, TEXTE, 14, True, padx=16, pady=(14, 4))
            ctk.CTkLabel(
                bloc, text=str(chemin), text_color=GRIS, wraplength=700
            ).pack(anchor="w", padx=16, pady=(0, 14))

        self.bouton("💾  Enregistrer les CSV", self.exporter_csv)
        self.bouton("📁  Ouvrir le dossier des données", self.ouvrir_dossier)
        ctk.CTkLabel(
            self.zone,
            text="Base SQLite : data/datalab.db. Les exports CSV restent disponibles.",
            text_color=GRIS, wraplength=700,
        ).pack(anchor="w", pady=15)

    def exporter_csv(self):
        try:
            enregistrer_produits(self.produits)
            messagebox.showinfo(
                "Export terminé",
                "Les fichiers CSV et individuels ont été enregistrés."
            )
        except Exception as erreur:
            messagebox.showerror("Erreur d’export", str(erreur))

    def ouvrir_dossier(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            os.startfile(str(DATA_DIR))
        except OSError as erreur:
            messagebox.showerror("Impossible d’ouvrir le dossier", str(erreur))


def lancer_interface():
    AmazonScrapingApp().mainloop()


if __name__ == "__main__":
    lancer_interface()
