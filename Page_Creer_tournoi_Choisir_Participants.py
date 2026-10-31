import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


class Page_Creer_tournoi_Choisir_Participants(ctk.CTkFrame):

    # Initialiser les informations de la page
    def __init__(self, master=None, controlleur=None):
        super().__init__(master, fg_color="white")

        self.controlleur = controlleur

        self.categorie = controlleur.tournoi_en_creation["categorie"]

        # Liste contenant les identifiants des joueurs selectionnes
        self.selection = []

        self.show_page()

    # Afficher les elements de la page
    def show_page(self):
        self.frame_page = ctk.CTkFrame(
            self, width=768, height=432, fg_color="white"
        )
        self.frame_page.place(x=0, y=0)

        # Afficher le logo
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

        ctk.CTkLabel(
            self.frame_page,
            text="Création d'un tournoi",
            font=("Arial", 21, "bold"),
            text_color="black"
        ).place(relx=0.5, rely=0.1, anchor="center")

        ctk.CTkLabel(
            self.frame_page,
            text="PAGE B - CHOISIR LES JOUEURS",
            text_color="black"
        ).place(relx=0.5, rely=0.2, anchor="center")

        # Selectionner un joueur existant
        ctk.CTkLabel(
            self.frame_page,
            text="Joueur existant :",
            text_color="black"
        ).place(x=25, y=140)

        self.combo = ctk.CTkComboBox(
            self.frame_page,
            width=195
        )
        self.combo.place(x=170, y=140)

        ctk.CTkButton(
            self.frame_page,
            text="Ajouter",
            width=75,
            command=self.ajouter
        ).place(x=380, y=140)

        # Entrer le nom d'un nouveau joueur
        ctk.CTkLabel(
            self.frame_page,
            text="Nouveau joueur :",
            text_color="black"
        ).place(x=25, y=220)

        self.nom = ctk.CTkEntry(
            self.frame_page,
            width=195,
            placeholder_text="Nom du joueur"
        )
        self.nom.place(x=170, y=220)

        ctk.CTkButton(
            self.frame_page,
            text="Créer",
            width=75,
            command=self.creer_joueur
        ).place(x=380, y=220)

        # Afficher les participants selectionnes a droite
        ctk.CTkLabel(
            self.frame_page,
            text="Participants",
            text_color="black",
            font=("Arial", 14, "bold")
        ).place(x=565, y=110)

        self.zone = ctk.CTkScrollableFrame(
            self.frame_page,
            width=170,
            height=190
        )
        self.zone.place(x=540, y=140)

        # Choisir le nombre de rondes suisses
        ctk.CTkLabel(
            self.frame_page,
            text="Nombre de rondes :",
            text_color="black"
        ).place(x=25, y=305)

        self.rondes = ctk.CTkEntry(
            self.frame_page,
            width=70
        )
        self.rondes.insert(0, "3")
        self.rondes.place(x=170, y=305)

        from Page_Creer_tournoi_Choisir_Categorie import Page_Creer_tournoi_Choisir_Categorie

        # Retourner a la page des categories
        ctk.CTkButton(
            self.frame_page,
            text="Retour",
            command=lambda: self.controlleur.changer_page(
                Page_Creer_tournoi_Choisir_Categorie
            )
        ).place(x=30, y=365)

        # Creer le tournoi et commencer la premiere ronde
        ctk.CTkButton(
            self.frame_page,
            text="Commencer",
            command=self.commencer
        ).place(x=580, y=365)

        self.actualiser_combo()

    # Actualiser les joueurs disponibles selon la categorie
    def actualiser_combo(self):
        joueurs = [
            p for p in self.controlleur.mes_participants.banqueParticipant
            if str(p.categorie) == self.categorie
            and int(p.id) not in self.selection
        ]

        # Utiliser les ID pour differencier les joueurs
        self.options = {
            f"{p.nom} (#{p.id})": int(p.id)
            for p in joueurs
        }

        valeurs = list(self.options)

        self.combo.configure(
            values=valeurs or ["Aucun joueur"]
        )

        self.combo.set(
            valeurs[0] if valeurs else "Aucun joueur"
        )

    # Ajouter le joueur selectionne dans la liste
    def ajouter(self):
        pid = self.options.get(self.combo.get())

        if pid is not None:
            self.selection.append(pid)
            self.actualiser_combo()
            self.actualiser_liste()

    # Creer un joueur en utilisant la banque des coequipiers
    def creer_joueur(self):
        nom = self.nom.get().strip()

        if not nom:
            messagebox.showerror(
                "Erreur",
                "Entre le nom du joueur."
            )
            return

        banque = self.controlleur.mes_participants.banqueParticipant

        # Verifier si le joueur existe deja dans cette categorie
        for p in banque:
            if (
                p.nom.casefold() == nom.casefold()
                and str(p.categorie) == self.categorie
            ):
                messagebox.showerror(
                    "Erreur",
                    "Ce joueur existe déjà dans cette catégorie."
                )
                return

        # Generer un nouvel identifiant unique
        nouveau_id = max(
            (int(p.id) for p in banque),
            default=0
        ) + 1

        # Utiliser la methode deja creee par les coequipiers
        self.controlleur.mes_participants.creerParticipant(
            nouveau_id,
            nom,
            self.categorie,
            banque
        )

        # Ajouter directement le joueur au tournoi
        self.selection.append(nouveau_id)

        self.nom.delete(0, "end")

        self.actualiser_combo()
        self.actualiser_liste()

    # Mettre a jour la liste visible des joueurs selectionnes
    def actualiser_liste(self):
        for widget in self.zone.winfo_children():
            widget.destroy()

        banque = self.controlleur.mes_participants.banqueParticipant

        for pid in self.selection:
            joueur = next(
                (p for p in banque if int(p.id) == pid),
                None
            )

            if joueur is None:
                continue

            ligne = ctk.CTkFrame(self.zone)
            ligne.pack(fill="x", pady=2)

            ctk.CTkLabel(
                ligne,
                text=joueur.nom,
                width=105
            ).pack(side="left")

            ctk.CTkButton(
                ligne,
                text="X",
                width=24,
                command=lambda i=pid: self.retirer(i)
            ).pack(side="right")

    # Retirer le joueur du tournoi sans le supprimer de la banque
    def retirer(self, pid):
        self.selection.remove(pid)

        self.actualiser_combo()
        self.actualiser_liste()

    # Enregistrer le tournoi et generer sa premiere ronde
    def commencer(self):
        try:
            nb_rondes = int(self.rondes.get())

            donnees = self.controlleur.tournoi_en_creation

            # Enregistrer le tournoi dans le CSV
            tournoi = self.controlleur.mes_tournois.enregistrer(
                donnees["nom"],
                donnees["categorie"],
                self.selection,
                nb_rondes
            )

            # Generer automatiquement les premiers matchs
            self.controlleur.mes_tournois.prochaine_ronde(tournoi)

            # Conserver le tournoi actif dans le controleur
            self.controlleur.tournoi_actuel = tournoi

            from Page_Gerer_Tournoi import Page_Gerer_Tournoi

            self.controlleur.changer_page(Page_Gerer_Tournoi)

        except ValueError as erreur:
            messagebox.showerror(
                "Erreur",
                str(erreur)
            )
