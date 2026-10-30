
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Page_Rechercher_Tournoi(ctk.CTkFrame):

    # Constructeur de la page de recherche
    def __init__(self, master=None, controlleur=None):
        super().__init__(master, fg_color="white")
        self.controlleur = controlleur
        self.show_page()

    # Afficher la recherche et la liste des tournois
    def show_page(self):
        ctk.CTkLabel(
            self,
            text="Tournois existants",
            font=("Arial", 22, "bold"),
            text_color="black"
        ).pack(pady=18)

        self.recherche = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="Rechercher par nom ou catégorie"
        )
        self.recherche.pack(pady=8)

        # Actualiser la recherche quand l'utilisateur tape
        self.recherche.bind(
            "<KeyRelease>",
            lambda event: self.actualiser()
        )

        self.zone = ctk.CTkScrollableFrame(
            self, width=550, height=235
        )
        self.zone.pack(pady=8)

        from accueil import Accueil

        ctk.CTkButton(
            self,
            text="Accueil",
            command=lambda: self.controlleur.changer_page(Accueil)
        ).pack(pady=5)

        self.actualiser()

    # Mettre a jour les tournois affichés selon la recherche
    def actualiser(self):
        for widget in self.zone.winfo_children():
            widget.destroy()

        tournois = self.controlleur.mes_tournois.rechercher(
            self.recherche.get()
        )

        if not tournois:
            ctk.CTkLabel(
                self.zone,
                text="Aucun tournoi trouvé"
            ).pack(pady=10)

        for tournoi in tournois:
            ctk.CTkButton(
                self.zone,
                width=500,
                text=(
                    f"{tournoi['nom']} | {tournoi['categorie']} | "
                    f"Ronde {len(tournoi['rondes'])}"
                ),
                command=lambda t=tournoi: self.ouvrir(t)
            ).pack(pady=5)

    # Ouvrir un tournoi deja enregistre
    def ouvrir(self, tournoi):
        self.controlleur.tournoi_actuel = tournoi
        self.controlleur.changer_page(Page_Gerer_Tournoi)


class Page_Gerer_Tournoi(ctk.CTkFrame):

    # Constructeur de la page de gestion du tournoi
    def __init__(self, master=None, controlleur=None):
        super().__init__(master, fg_color="white")

        self.controlleur = controlleur
        self.tournoi = controlleur.tournoi_actuel

        self.show_page()

    # Retrouver le nom d'un joueur a partir de son identifiant
    def nom_joueur(self, pid):
        if pid is None:
            return "REPOS"

        for p in self.controlleur.mes_participants.banqueParticipant:
            if int(p.id) == int(pid):
                return p.nom

        return f"Joueur {pid}"

    # Construire les onglets de matchs, classement et graphique
    def show_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        banque = self.controlleur.mes_tournois
        tournoi = self.tournoi

        ctk.CTkLabel(
            self,
            text=tournoi["nom"],
            font=("Arial", 21, "bold"),
            text_color="black"
        ).pack(pady=(8, 2))

        ctk.CTkLabel(
            self,
            text=(
                f"{tournoi['categorie']} | "
                f"Ronde {len(tournoi['rondes'])}/{tournoi['nbRondes']}"
            ),
            text_color="black"
        ).pack()

        onglets = ctk.CTkTabview(
            self, width=725, height=280
        )
        onglets.pack(pady=5)

        onglets.add("Matchs")
        onglets.add("Classement")
        onglets.add("Graphique")

        # Afficher les matchs de la ronde en cours
        zone_matchs = ctk.CTkScrollableFrame(
            onglets.tab("Matchs")
        )
        zone_matchs.pack(fill="both", expand=True)

        if not tournoi["rondes"]:
            ctk.CTkLabel(
                zone_matchs,
                text="Aucune ronde commencée."
            ).pack(pady=10)

        else:
            for indice, match in enumerate(tournoi["rondes"][-1]):
                ligne = ctk.CTkFrame(zone_matchs)
                ligne.pack(fill="x", pady=3)

                joueur1 = self.nom_joueur(match["a"])
                joueur2 = self.nom_joueur(match["b"])

                ctk.CTkLabel(
                    ligne,
                    text=f"{joueur1} VS {joueur2}",
                    width=300
                ).pack(side="left", padx=5)

                # Un repos ne demande aucun resultat
                if match["b"] is None:
                    ctk.CTkLabel(
                        ligne, text="+2 points"
                    ).pack(side="left")
                    continue

                # Convertir le resultat sauvegarde en texte
                choix = {
                    None: "À jouer",
                    "A": "Victoire joueur 1",
                    "B": "Victoire joueur 2",
                    "N": "Match nul"
                }

                combo = ctk.CTkComboBox(
                    ligne,
                    values=[
                        "À jouer",
                        "Victoire joueur 1",
                        "Victoire joueur 2",
                        "Match nul"
                    ],
                    width=165
                )
                combo.set(choix[match["resultat"]])
                combo.pack(side="left", padx=5)

                ctk.CTkButton(
                    ligne,
                    text="OK",
                    width=45,
                    command=lambda i=indice, c=combo: self.resultat(
                        i, c.get()
                    )
                ).pack(side="left")

        # Recuperer le classement calcule par la banque
        classement = banque.classement(tournoi)

        zone_classement = ctk.CTkScrollableFrame(
            onglets.tab("Classement")
        )
        zone_classement.pack(fill="both", expand=True)

        for _, joueur in classement.iterrows():
            ctk.CTkLabel(
                zone_classement,
                text=(
                    f"{int(joueur['Rang'])}. "
                    f"{self.nom_joueur(joueur['ID'])} | "
                    f"{int(joueur['Points'])} pts | "
                    f"{int(joueur['Victoires'])}V "
                    f"{int(joueur['Nulles'])}N "
                    f"{int(joueur['Defaites'])}D | "
                    f"Buchholz : {int(joueur['Buchholz'])}"
                )
            ).pack(anchor="w", pady=3)

        # Creer un graphique avec Matplotlib a partir du DataFrame
        noms = [
            self.nom_joueur(pid)
            for pid in classement["ID"]
        ]

        points = classement["Points"].tolist()

        figure, axe = plt.subplots(figsize=(6, 2.5))
        axe.barh(noms[::-1], points[::-1])
        axe.set_xlabel("Points")
        axe.set_title("Classement du tournoi")
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=onglets.tab("Graphique")
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

        plt.close(figure)

         # Boutons de navigation
        boutons = ctk.CTkFrame(self, fg_color="white")
        boutons.pack(pady=6)

        ctk.CTkButton(
            boutons,
            text="Retour aux tournois",
            width=165,
            command=lambda: self.controlleur.changer_page(
                Page_Rechercher_Tournoi
            )
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            boutons,
            text="Ronde suivante",
            width=165,
            command=self.prochaine_ronde
        ).pack(side="left", padx=10)

     # Enregistrer le resultat choisi pour un match
    def resultat(self, indice, choix):
        codes = {
            "À jouer": None,
            "Victoire joueur 1": "A",
            "Victoire joueur 2": "B",
            "Match nul": "N"
        }

        try:
            self.controlleur.mes_tournois.enregistrer_resultat(
                self.tournoi,
                indice,
                codes[choix]
            )

            # Actualiser les points et le classement
            self.show_page()

        except (ValueError, KeyError) as erreur:
            messagebox.showerror("Erreur", str(erreur))

     # Generer la ronde suivante si tous les matchs sont termines
    def prochaine_ronde(self):
        try:
            self.controlleur.mes_tournois.prochaine_ronde(
                self.tournoi
            )
            self.show_page()

        except ValueError as erreur:
            messagebox.showinfo("Tournoi", str(erreur))


                    
