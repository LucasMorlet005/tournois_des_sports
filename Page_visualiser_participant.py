import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

from CerclePourcentage import CerclePourcentage





class page_visualiser_participant(ctk.CTkFrame):
    def __init__ (self, master=None , controlleur= None):
                super().__init__(master)
                self.master = master
                self.controlleur = controlleur 
                self.show_page()

   
    def show_page(self):
        self.frame_page = ctk.CTkFrame(self, width = 768 , height = 432, fg_color = "white")
        self.frame_page.place(x=0 , y=0 )


        #Le logo en haut à gauche
        image_pil = Image.open("images/logo.jpg")
        self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(84, 72))
        self.label_logo = ctk.CTkLabel(self.frame_page, text="", image = self.bg_image )
        self.label_logo.place(relx=0.05, rely=0.05)

        #Label pour le nom Du participant
        self.label_titre_page = ctk.CTkLabel(self.frame_page, text = self.controlleur.participant_actuel.nom ,text_color="#00ffff", font=("Arial", 28, "bold"))
        self.label_titre_page.place(relx =0.5 ,rely =  0.13 , anchor = "center")

        #Affichage du pourcentage de victoire
        self.label_pourcent_victoire = ctk.CTkLabel(self.frame_page, text="Pourcentage\nde victoire.", text_color="#000000", font=("Arial", 18, "bold"))
        self.label_pourcent_victoire.place(relx = 0.85, rely=0.17, anchor="center")
        pourcentage_actuel = self.controlleur.participant_actuel.calculerPourcentageVictoire()

        self.cercle_victoire = CerclePourcentage(
            self.frame_page, 
            pourcentage=pourcentage_actuel, 
            width=180, 
            height=180,
        )
        self.cercle_victoire.place(relx=0.85, rely=0.5, anchor="center")

        #fiches
        self.label_fiche = ctk.CTkLabel(self.frame_page,font=("Arial", 20, "bold") , text_color = "#000000" , text = f"Victoire : {self.controlleur.participant_actuel.fiche[0]}\n\nDéfaite : {self.controlleur.participant_actuel.fiche[1]}\n\nÉgalité : {self.controlleur.participant_actuel.fiche[2]}")
        self.label_fiche.place(relx = 0.15, rely=0.35)

        #autre statistiques
        self.label_autres_stats = ctk.CTkLabel(self.frame_page,font=("Arial", 20, "bold") , text_color = "#000000"  ,text = f"Tournois Joués : {self.controlleur.participant_actuel.nbTournoi}\n\n\nDifférenciel : {self.controlleur.participant_actuel.calculerDifferenciel()}")
        self.label_autres_stats.place(relx = 0.35, rely=0.35)



            # bouton pour aller à la page gérer les joueurs
        from Page_Gerer_Participants import Page_Gerer_Participants
        button_aller_page_participant = ctk.CTkButton(self.frame_page, text="Gérer les joueurs", command=lambda: self.controlleur.changer_page(Page_Gerer_Participants), fg_color= "blue" , width=140, height=28)
        button_aller_page_participant.place(relx = 0.8, rely = 0.85, anchor = "center")


            #bouton pour retourner à l'accueil
        from accueil import Accueil
        self.button_accueil = ctk.CTkButton(self.frame_page, text = "Aller à l'ACCUEIL" , command = lambda: self.controlleur.changer_page( Accueil) , fg_color= "blue")
        self.button_accueil.place(relx = 0.15 ,rely = 0.85, anchor = "center")
