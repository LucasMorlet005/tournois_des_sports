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

        frame_page = ctk.CTkFrame(self , width = 768 , height = 432, fg_color= "white")
        frame_page.place(x=0, y=0)

        #Le fond de l'écran d'accueil 
        image_pil = Image.open("images/logo.jpg")
        self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(329, 289))

        self.label_fond = ctk.CTkLabel(frame_page, text="", image = self.bg_image)# Label
        self.label_fond.place(relx=0.3, rely=0.05)

         #Le logo en haut à gauche
        #image_pil = Image.open(images/logo.jpg")
        self.image_logo = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(84, 72))
        self.label_logo = ctk.CTkLabel(frame_page, text="", image = self.image_logo )
        self.label_logo.place(relx=0.05, rely=0.05)

        #button pour aller à la page créer tournoi
        from Page_Creer_tournoi_Choisir_Categorie import Page_Creer_tournoi_Choisir_Categorie
        button_changer_page = ctk.CTkButton(frame_page, text = "Créer un tournoi" , command =lambda: self.controlleur.changer_page(Page_Creer_tournoi_Choisir_Categorie))
        button_changer_page.place(relx = 0.7 , rely = 0.7)

        # bouton pour aller à la page gérer les joueurs
        from Page_Gerer_Participants import Page_Gerer_Participants
        button_aller_page_participant = ctk.CTkButton(frame_page, text="Gérer les joueurs", command=lambda: self.controlleur.changer_page(Page_Gerer_Participants))
        button_aller_page_participant.place(relx = 0.1, rely = 0.7)