import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from accueil import Accueil


# PAGE POUR RECHERCHER LES TOURNOIS EXISTANTS
class Page_Rechercher_Tournoi(ctk.CTkFrame):

    # Initialiser la page de recherche
    def __init__(self, master=None, controlleur=None):
        super().__init__(master, fg_color="white")

        self.controlleur = controlleur
        self.show_page()

    # Afficher la liste des tournois
    def show_page(self):
        ctk.CTkLabel(
            self,
            text="Tournois existants",
            font=("Arial", 22, "bold"),
            text_color="black"
        ).pack(pady=15)

        # Champ pour rechercher un tournoi
        self.recherche = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Nom ou catégorie"
        )
        self.recherche.pack(pady=7)

        # Actualiser les resultats pendant la saisie
        self.recherche.bind(
            "<KeyRelease>",
            lambda event: self.actualiser()
        )

        self.zone = ctk.CTkScrollableFrame(
            self,
            width=550,
            height=245
        )
        self.zone.pack(pady=7)

        ctk.CTkButton(
            self,
            text="Accueil",
            command=lambda: self.controlleur.changer_page(Accueil)
        ).pack(pady=5)

        self.actualiser()

    # Mettre a jour la liste des tournois trouves
    def actualiser(self):
        for widget in self.zone.winfo_children():
            widget.destroy()

        resultats = self.controlleur.mes_tournois.rechercher(
            self.recherche.get()
        )

        if not resultats:
            ctk.CTkLabel(
                self.zone,
                text="Aucun tournoi trouvé."
            ).pack(pady=10)

            

        # Creer un bouton pour chaque tournoi trouve
        for tournoi in resultats:

            if tournoi['enCours']:
                ctk.CTkButton(
                    self.zone,
                    width=510,
                    text=(
                        f"{tournoi['nom']} - "
                        f"{tournoi['categorie']} - "
                        f"Ronde {len(tournoi['rondes'])}"
                    ),
                    command=lambda t=tournoi: self.ouvrir(t)
                    ).pack(pady=4)
            else:



                ctk.CTkButton(
                    self.zone,
                    width=510,
                    text=(
                        f"{tournoi['nom']} - "
                        f"{tournoi['categorie']} - "
                        "Terminé"
                    ),
                    command=lambda t=tournoi: self.ouvrir(t)
                ).pack(pady=4)

    # Ouvrir le tournoi selectionne
    def ouvrir(self, tournoi):
        self.controlleur.tournoi_actuel = tournoi

        self.controlleur.changer_page(
            Page_Gerer_Tournoi
        )


# PAGE POUR GERER LES MATCHS ET LES RONDES SUISSES
class Page_Gerer_Tournoi(ctk.CTkFrame):

    # Initialiser la page de gestion
    def __init__(self, master=None, controlleur=None):
        super().__init__(master, fg_color="white")

        self.controlleur = controlleur
        self.tournoi = controlleur.tournoi_actuel

        #conserver les scores et les choix de matchs
        self.saisies=[]


        self.show_page()

    # Retrouver le nom d'un joueur avec son ID
    def nom_joueur(self, pid):
        if pid is None:
            return "REPOS"

        banque = self.controlleur.mes_participants.banqueParticipant

        for joueur in banque:
            if int(joueur.id) == int(pid):
                return joueur.nom

        return f"Joueur #{pid}"

    # Afficher la page avec les matchs, le classement et le graphique
    def show_page(self):
        # Supprimer les anciens elements avant de les reconstruire
        for widget in self.winfo_children():
            widget.destroy()

        tournoi = self.tournoi
        banque = self.controlleur.mes_tournois

        #reinitialiser les widgets de saisie
        self.saisies = []

        ctk.CTkLabel(
            self,
            text=tournoi["nom"],
            font=("Arial", 20, "bold"),
            text_color="black"
        ).pack(pady=(5, 0))

        ctk.CTkLabel(
            self,
            text=(
                f"{tournoi['categorie']} - "
                f"Ronde {len(tournoi['rondes'])}/{tournoi['nbRondes']}"
            ),
            text_color="black"
        ).pack()

        # Creer trois onglets
        onglets = ctk.CTkTabview(
            self,
            width=730,
            height=288
        )
        onglets.pack(pady=3)

        onglets.add("Matchs")
        onglets.add("Classement")
        onglets.add("Graphique")

        # ONGLET MATCHS
        zone = ctk.CTkScrollableFrame(
            onglets.tab("Matchs")
        )
        zone.pack(fill="both", expand=True)

        if not tournoi["rondes"]:
            ctk.CTkLabel(
                zone,
                text="Aucune ronde commencée."
            ).pack()

        elif not self.tournoi["enCours"]:

            ctk.CTkLabel(
                zone,
                text="LE TOURNOI EST TERMINÉ",
                font=("Arial", 18, "bold"),
                text_color="green"
            ).pack(pady=20)
            
        else:
            # Afficher tous les matchs de la ronde actuelle
            for indice, match in enumerate(tournoi["rondes"][-1]):
                ligne = ctk.CTkFrame(zone)
                ligne.pack(fill="x", pady=3)

                self.joueur1 = self.nom_joueur(match["a"])
                self.joueur2 = self.nom_joueur(match["b"])


                #nom premier joueur
                ctk.CTkLabel(
                    ligne,
                    text=self.joueur1,
                    width=135
                ).pack(side="left", padx=3)

                # Donner 2 points automatiquement pour un repos
                if match["b"] is None:
                    ctk.CTkLabel(
                        ligne,
                        text="Repos (+2 points)"
                    ).pack(side="left")

                    self.saisies.append(None)
                    continue

                #Point marque par premier joueur
                score_a=ctk.CTkEntry(
                    ligne,
                    width=45,
                    placeholder_text="Pts"
                )
                score_a.pack(side="left", padx=2)

                #Afficher les anciens score si match enregeistre
                if match.get("points_a") is not None:
                    score_a.insert(0, str(match["points_a"]))

                ctk.CTkLabel(
                    ligne,
                    text=" - "
                ).pack(side="left")


                #Point marque par deuxieme joueur
                score_b=ctk.CTkEntry(
                    ligne,
                    width=45,
                    placeholder_text="Pts"
                )
                score_b.pack(side="left", padx=2)

                # Afficher les anciens score si match enregeistre
                if match.get("points_b") is not None:
                    score_b.insert(0, str(match["points_b"]))

                # Nom 2ieme joueur
                ctk.CTkLabel(
                    ligne,
                    text=self.joueur2,
                    width=135
                ).pack(side="left", padx=3)
                # Choix des resultats possibles
                options = {
                    None: "À jouer",
                    "A": "Victoire joueur 1",
                    "B": "Victoire joueur 2",
                    "N": "Match nul"
                }

                combo = ctk.CTkComboBox(
                    ligne,
                    values=["À jouer","Victoire de: " + self.joueur1, "Victoire de: " + self.joueur2, "Match nul"],
                    width=150,
                    state="readonly"
                )

                # Afficher le resultat deja sauvegarde
                combo.set("À jouer")
                combo.pack(side="left", padx=3)

                # Conserver widgets pour enregistrer la ronde
                self.saisies.append((combo, score_a, score_b , self.joueur1 , self.joueur2))  

        # ONGLET CLASSEMENT
        classement = banque.classement(tournoi)

        zone_classement = ctk.CTkScrollableFrame(
            onglets.tab("Classement")
        )
        zone_classement.pack(fill="both", expand=True)

        # Afficher le classement calcule par Pandas
        for rang, (_, joueur) in enumerate(classement.iterrows(), 1):
            ctk.CTkLabel(
                zone_classement,
                text=(
                    f"{rang}. {self.nom_joueur(joueur['ID'])} | "
                    f"{joueur['Points']} pts | "
                    f"{joueur['V']}V "
                    f"{joueur['N']}N "
                    f"{joueur['D']}D | "
                    f"Buchholz {joueur['Buchholz']}"
                )
            ).pack(anchor="w", pady=3)

        # ONGLET GRAPHIQUE
        # Creer un graphique a partir du classement Pandas
        figure, axe = plt.subplots(figsize=(6, 2.4))

        noms = [
            self.nom_joueur(pid)
            for pid in classement["ID"]
        ]

        points = classement["Points"].tolist()

        axe.barh(
            noms[::-1],
            points[::-1]
        )

        axe.set_xlabel("Points")
        axe.set_title("Classement du tournoi")

        figure.tight_layout()

        # Integrer le graphique Matplotlib dans CustomTkinter
        graphique = FigureCanvasTkAgg(
            figure,
            master=onglets.tab("Graphique")
        )

        graphique.draw()

        graphique.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        plt.close(figure)

        # BOUTONS DE NAVIGATION
        boutons = ctk.CTkFrame(
            self,
            fg_color="white"
        )
        boutons.pack(pady=5)

        ctk.CTkButton(
            boutons,
            text="Retour aux tournois",
            width=160,
            command=lambda: self.controlleur.changer_page(
                Page_Rechercher_Tournoi
            )
        ).pack(side="left", padx=10)

        #Enregistrer sans creer une nouvelle ronde a la derniere
        derniere_ronde = (len(tournoi["rondes"]) >= tournoi["nbRondes"])

            #Si le tournois est en cours on veut le bouton, sinon non
        if tournoi["enCours"]:
            self.bouton_enregistrer = ctk.CTkButton(
                boutons,
                text=("Enregistrer la ronde"
                    if derniere_ronde 
                    else "Ronde suivante"),
                width=175,
                command= self.prochaine_ronde
            ).pack(side="left", padx=10)

    # Enregistrer les resultats de la ronde actuelle
    def prochaine_ronde(self):

        resultats = list()

        for saisie in self.saisies:
            if saisie is None:
                resultats.append(None)

            else:
                combo, score_a, score_b, self.joueur1, self.joueur2 = saisie



                
                choix = combo.get()

                if choix == "Victoire de: " + self.joueur1:
                    self.resultat = "A"

                elif choix == "Victoire de: " + self.joueur2:
                    self.resultat = "B"

                elif choix == "Match nul":
                    self.resultat = "N"

                else:
                    self.resultat = None

            
            resultats.append((
                    self.resultat,
                    score_a.get(),
                    score_b.get()
                ))

        banque = self.controlleur.mes_tournois

        try:
            banque.enregistrer_ronde(
                self.tournoi,
                resultats
            )

                                    #mettre à jour les caractérisiques des joueurs
                #on simplifit le chemin d'accès vers les participants
            self.participant_1 = self.controlleur.mes_participants.rechercherParticipantNom(self.joueur1)
            self.participant_2 = self.controlleur.mes_participants.rechercherParticipantNom(self.joueur2)

                #On modifie les points gagnées pour les 2 participants
            self.participant_1.points[0] += int(score_a.get())
            self.participant_1.points[1] += int(score_b.get())

                #On modifie les points contres pour les 2 participants
            self.participant_2.points[0] += int(score_b.get())
            self.participant_2.points[1] += int(score_a.get())

                #Si le joueur 1 a gagné, on lui donne une victoire et on donne une défaite au participant 2
            if self.resultat == "A":
                self.participant_1.fiche[0] += 1
                self.participant_2.fiche[1] += 1

                  #Si le joueur 2 a gagné, on lui donne une victoire et on donne une défaite au participant 1
            elif self.resultat == "B":
                self.participant_2.fiche[0] += 1
                self.participant_1.fiche[1] += 1

                #Si c'est match nul, tout les 2 gagnent 1 défaite
            elif self.resultat == "N":
                self.participant_1.fiche[2] += 1
                self.participant_2.fiche[2] += 1


            if len(self.tournoi["rondes"]) < self.tournoi["nbRondes"]:
                banque.prochaine_ronde(self.tournoi)
            

            else:
                messagebox.showinfo(
                    "Tournoi",
                    "Derniere ronde enregistrée"
                )
                self.tournoi["enCours"] = False
    



            self.show_page()

        except ValueError as e:
            messagebox.showerror(
                "Erreur",
                str(e)
            )