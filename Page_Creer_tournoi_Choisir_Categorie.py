import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


class Page_Creer_tournoi_Choisir_Categorie(ctk.CTkFrame):

    # Initialiser la page de selection de categorie
    def __init__(self, master=None, controlleur=None):
        super().__init__(master, fg_color="white")
        self.controlleur = controlleur
        self.show_page()

    # Afficher les elements de la page
    def show_page(self):
        self.frame_page = ctk.CTkFrame(
            self, width=768, height=432, fg_color="white"
        )
        self.frame_page.place(x=0, y=0)

        # Afficher le logo de l'application
        image = Image.open("images/logo.jpg")

        self.logo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(84, 72)
        )

        ctk.CTkLabel(
            self.frame_page,
            text="",
            image=self.logo
        ).place(x=24, y=20)

        # Afficher le titre
        ctk.CTkLabel(
            self.frame_page,
            text="Création d'un tournoi",
            font=("Arial", 21, "bold"),
            text_color="black"
        ).place(relx=0.5, rely=0.1, anchor="center")

        ctk.CTkLabel(
            self.frame_page,
            text="PAGE A - CHOISIR LA CATÉGORIE",
            text_color="black"
        ).place(relx=0.5, rely=0.2, anchor="center")

        # Nom du tournoi
        ctk.CTkLabel(
            self.frame_page,
            text="Nom du tournoi :",
            text_color="black"
        ).place(x=165, y=130)

        self.nom = ctk.CTkEntry(
            self.frame_page,
            width=240,
            placeholder_text="Nom du tournoi"
        )
        self.nom.place(x=355, y=130)

        # Recuperer les categories des joueurs existants
        categories = sorted({
            str(p.categorie)
            for p in self.controlleur.mes_participants.banqueParticipant
        })

        ctk.CTkLabel(
            self.frame_page,
            text="Catégorie existante :",
            text_color="black"
        ).place(x=165, y=195)

        self.categorie = ctk.CTkComboBox(
            self.frame_page,
            values=categories or ["Aucune"],
            width=240
        )
        self.categorie.place(x=355, y=195)

        # Permettre la creation d'une nouvelle categorie
        ctk.CTkLabel(
            self.frame_page,
            text="Nouvelle catégorie :",
            text_color="black"
        ).place(x=165, y=260)

        self.nouvelle = ctk.CTkEntry(
            self.frame_page,
            width=240,
            placeholder_text="Au besoin"
        )
        self.nouvelle.place(x=355, y=260)

        from accueil import Accueil

        # Bouton pour retourner a l'accueil
        ctk.CTkButton(
            self.frame_page,
            text="Accueil",
            command=lambda: self.controlleur.changer_page(Accueil)
        ).place(x=30, y=365)

        # Bouton pour passer a la selection des participants
        ctk.CTkButton(
            self.frame_page,
            text="Choisir les participants",
            width=180,
            command=self.suivant
        ).place(x=555, y=365)

    # Verifier les informations avant de continuer
    def suivant(self):
        nom = self.nom.get().strip()

        # Prioriser la nouvelle categorie si elle est remplie
        categorie = (
            self.nouvelle.get().strip()
            or self.categorie.get().strip()
        )

        if not nom or not categorie or categorie == "Aucune":
            messagebox.showerror(
                "Erreur",
                "Entre un nom et une catégorie."
            )
            return

        # Conserver les informations pour la page suivante
        self.controlleur.tournoi_en_creation = {
            "nom": nom,
            "categorie": categorie
        }

        from Page_Creer_tournoi_Choisir_Participants import Page_Creer_tournoi_Choisir_Participants

        self.controlleur.changer_page(
            Page_Creer_tournoi_Choisir_Participants
        )
