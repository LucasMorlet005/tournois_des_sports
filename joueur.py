import math as math
import customtkinter
import customtkinter as ctk
import tkinter as tk 
import numpy as np

from PIL import Image, ImageTk


class Joueur(ctk.CTkFrame):
    def __init__(self, master, controlleur):
        super().__init__(master)
        self.master = master
        self.controlleur = controlleur
        self.show_page_joueur()



    def show_page_joueur(self):
    


        frame_page = ctk.CTkFrame(self, width = 800 , height = 600)
        frame_page.place(x=0 , y=0 )

         #Le fond de l'écran d'accueil 
        image_pil = Image.open("images/logo.jpg")
        self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(354, 302))

        self.label_fond = ctk.CTkLabel(frame_page, text="", image = self.bg_image)# Label
        self.label_fond.place(relx=0.3, rely=0.05)
        

        label_1 = ctk.CTkLabel(frame_page, text ="JOUEURS", font=("Arial", 40, "bold"))
        label_1.place(relx =0.1 ,rely =  0.5)

        from accueil import Accueil

        button_changer_page = ctk.CTkButton(frame_page, text = "Aller à l'ACCUEIL" , command = lambda: self.controlleur.changer_page( Accueil))
        button_changer_page.place(relx = 0.7 ,rely = 0.7)


