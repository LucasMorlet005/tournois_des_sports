import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk





class page_visualiser_participant(ctk.CTkFrame):
    def __init__ (self, master=None , controlleur= None):
                super().__init__(master)
                self.master = master
                self.controlleur = controlleur 
                self.show_page()


            ######LE participant actuel, donc celui choisi lors
                          #  de la recherche par l'utilisateur peut etre appelé par :
                          #  self.controlleur.participant_actuel, comme j'ai fait dans le label pour son nom
    def show_page(self):
          self.frame_page = ctk.CTkFrame(self, width = 768 , height = 432, fg_color = "white")
          self.frame_page.place(x=0 , y=0 )

              #    ICI :    nom Du participant
            
          self.label_titre_page = ctk.CTkLabel(self.frame_page, text = self.controlleur.participant_actuel.nom ,text_color="black" , font=("Arial",30 ,"bold"))
          self.label_titre_page.place(relx =0.5 ,rely =  0.23 , anchor = "center")

            
    
          #Le logo en haut à gauche
          image_pil = Image.open("images/logo.jpg")
          self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(84, 72))
          self.label_logo = ctk.CTkLabel(self.frame_page, text="", image = self.bg_image )
          self.label_logo.place(relx=0.05, rely=0.05)
          
          #titre de la page
          self.label_titre_page = ctk.CTkLabel(self.frame_page, text ="Visualiser les statistiques du joueur",text_color="black" , font=("Arial",30 ,"bold"))
          self.label_titre_page.place(relx =0.53 ,rely =  0.13 , anchor = "center")






          #bouton pour retourner à l'accueil
          from accueil import Accueil
          self.button_accueil = ctk.CTkButton(self.frame_page, text = "Aller à l'ACCUEIL" , command = lambda: self.controlleur.changer_page( Accueil) , fg_color= "blue")
          self.button_accueil.place(relx = 0.15 ,rely = 0.85, anchor = "center")
