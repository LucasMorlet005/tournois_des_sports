import math as math
import customtkinter
import customtkinter as ctk
import tkinter as tk 
import numpy as np
from accueil import Accueil
from PIL import Image, ImageTk
from BanqueDeParticipant import BanqueDeParticipant
from BanqueTournois import BanqueTournois




class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("768x432")
        self.title("TDS")  
        self.protocol("WM_DELETE_WINDOW", self.quit) # le protocole pour la fermeture safe
        self.page_actuelle = None   #Stocke la page visible à l'écran
        self.mes_participants = BanqueDeParticipant("listesParticipants.csv")
        self.participant_actuel = None
        

        self.mes_participants = BanqueDeParticipant("listesParticipants.csv")

        # Charger les tournois enregistres
        self.mes_tournois = BanqueTournois("tournois.json")

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


  
             



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()