import math as math
import customtkinter
import customtkinter as ctk
import tkinter as tk 
import numpy as np
from accueil import Accueil
from PIL import Image, ImageTk
from BanqueDeParticipant import BanqueDeParticipant
from Participant import Participant
import pandas as pd
from BanqueTournois import BanqueTournois


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("768x432")
        self.title("TDS")  
        self.protocol("WM_DELETE_WINDOW", lambda: self.quit("listesParticipants.csv")) # le protocole pour la fermeture safe
        self.page_actuelle = None   #Stocke la page visible à l'écran
        self.mes_participants = BanqueDeParticipant("listesParticipants.csv")
        self.participant_actuel = None

        # Charger les tournois et leurs matchs depuis les fichiers CSV
        self.mes_tournois = BanqueTournois("tournois.csv", "matchs.csv")

        # Conserver le tournoi actuellement selectionne
        self.tournoi_actuel = None

        # Conserver les informations pendant la creation
        self.tournoi_en_creation = {}

        # Chemin du fichier des participants
        self.fichier_participants = "listesParticipants.csv"

        self.changer_page(Accueil)

    def changer_page(self, classe_nouvelle_page):

        #détruire la page actuelle
        if self.page_actuelle is not None:
            self.page_actuelle.destroy()

        #créer la nouvelle page
        self.page_actuelle = classe_nouvelle_page(master = self, controlleur =self)
        self.page_actuelle.pack(fill="both", expand=True)


    def quit(self,fichier):
           # Crée une liste de dictionnaires avec les attributs bruts dans l'ordre exact
        liste_dicts = []
        for p in self.mes_participants.banqueParticipant:
            d = {
                "id": p.id,
                "nom": p.nom,
                "categorie": p.categorie,
                "nbTournoi": p.nbTournoi,
                "victoire": p.fiche[0],
                "defaite": p.fiche[1],
                "nulle": p.fiche[2],
                "pointsPour": p.points[0],
                "pointsContre": p.points[1]
            }
            liste_dicts.append(d)

        #  Crée le DataFrame à partir de cette liste
        df_modifie = pd.DataFrame(liste_dicts)

        #  Réécrit le fichier proprement (écrase l'ancien contenu)
        df_modifie.to_csv(fichier, index=False, sep=",")
        
        self.destroy()


    


        


  
             



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()