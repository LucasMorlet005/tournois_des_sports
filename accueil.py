import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk




class Accueil(ctk.CTkFrame):
    def __init__ (self, master=None , controlleur= None):
        super().__init__(master)
        self.master = master
        self.controlleur = controlleur 
        self.show_accueil()



    def show_accueil(self):

        self.frame_page = ctk.CTkFrame(self , width = 768 , height = 432, fg_color= "white")
        self.frame_page.place(x=0, y=0)

        #Le fond de l'écran d'accueil 
        image_pil = Image.open("images/logo.jpg")
        self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(329, 289))

        self.label_fond = ctk.CTkLabel(self.frame_page, text="", image = self.bg_image)# Label
        self.label_fond.place(relx=0.3, rely=0.05)


        #button pour aller à la page créer tournoi
        from Page_Creer_tournoi_Choisir_Categorie import Page_Creer_tournoi_Choisir_Categorie
        self.button_changer_page = ctk.CTkButton(self.frame_page, text = "Créer un tournoi" , command =lambda: self.controlleur.changer_page(Page_Creer_tournoi_Choisir_Categorie))
        self.button_changer_page.place(relx = 0.8 , rely = 0.75, anchor="center")

        # bouton pour aller à la page gérer les joueurs
        from Page_Gerer_Participants import Page_Gerer_Participants
        self.button_aller_page_participant = ctk.CTkButton(self.frame_page, text="Gérer les joueurs", command=lambda: self.controlleur.changer_page(Page_Gerer_Participants))
        self.button_aller_page_participant.place(relx = 0.2, rely = 0.75, anchor= "center")

        # Importer la page pour rechercher les tournois existants
        from Page_Gerer_Tournoi import Page_Rechercher_Tournoi

        # Bouton pour consulter les tournois enregistres
        self.button_tournois = ctk.CTkButton(self.frame_page, text="Voir les Tournois",command=lambda: self.controlleur.changer_page(Page_Rechercher_Tournoi) )
        self.button_tournois.place(relx=0.5, rely=0.75, anchor = "center")
