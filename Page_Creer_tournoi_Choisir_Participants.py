import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class Page_Creer_tournoi_Choisir_Participants(ctk.CTkFrame):
    def __init__ (self, master=None , controlleur= None):
            super().__init__(master)
            self.master = master
            self.controlleur = controlleur 
            self.show_page()


    def combobox_participants_callback(self,choice):
         print(choice)
         return
         


    def show_page(self):
        self.frame_page = ctk.CTkFrame(self, width = 768 , height = 432, fg_color = "white")
        self.frame_page.place(x=0 , y=0 )

        #Le logo en haut à gauche
        image_pil = Image.open("images/logo.jpg")
        self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(84, 72))
        self.label_logo = ctk.CTkLabel(self.frame_page, text="", image = self.bg_image )
        self.label_logo.place(relx=0.05, rely=0.05)
        
        #titre de la page
        self.label_titre_page = ctk.CTkLabel(self.frame_page, text ="Création d'un tournois ",text_color="black" , font=("Arial", 20, "bold"))
        self.label_titre_page.place(relx =0.5 ,rely =  0.1 , anchor = "center")

        #choisir la catégorie
        self.label_sous_titre = ctk.CTkLabel(self.frame_page, text ="CHOISIR LES PARTICIPANTS ", text_color="black" , font=("Arial", 12, "bold"))
        self.label_sous_titre.place(relx =0.5 ,rely =  0.2 , anchor = "center")


            #combobox choisir participants
        combobox_var = ctk.StringVar(value="option 2")
        self.label_choisir_participant = ctk.CTkLabel(self.frame_page, text ="Chosir parmis ceux\n déjà enregistrés:", text_color="black" , font=("Arial", 14, "bold"))
        self.label_choisir_participant.place(relx =0.3 ,rely =  0.45 , anchor = "center")
        self.combobox_participants =  ctk.CTkComboBox(self.frame_page, values=["option 1", "option 2"],command=self.combobox_participants_callback(combobox_var))
        self.combobox_participants.place(relx =0.5 ,rely =  0.45 , anchor = "center")




        #bouton pour retourner à l'accueil
        from accueil import Accueil
        self.button_accueil = ctk.CTkButton(self.frame_page, text = "Aller à l'ACCUEIL" , command = lambda: self.controlleur.changer_page( Accueil) , fg_color= "blue")
        self.button_accueil.place(relx = 0.05 ,rely = 0.85)


        #from Visualiser_Le_Tournois import Visualiser_Le_Tournois
        #self.bouton_choisir_participants = ctk.CTkButton(self.frame_page, text = "Choisir les participants" , command = lambda: self.controlleur.changer_page( Page_Choisir_Categorie) , fg_color= "blue")
        #self.bouton_choisir_participants.place(relx = 0.8 ,rely = 0.85)