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

        
        #fond_canvas = tk.Canvas(self , width = 800, height = 600, highlightthickness=0)
        #fond_canvas.pack(fill="both", expand=True)

        #if self.bg_image:
        #    fond_canvas.create_image(175,75, image= self.bg_image, anchor="nw")
       # else:
         #   print("MOIO VEUT PAS")

        frame_page = ctk.CTkFrame(self , width = 800 , height = 600, fg_color= "white")
        frame_page.place(x=0, y=0)

        #Le fond de l'écran d'accueil 
        image_pil = Image.open("logo.jpg")
        self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(329, 289))

        self.label_fond = ctk.CTkLabel(frame_page, text="", image = self.bg_image)# Label
        self.label_fond.place(relx=0.3, rely=0.05)


        label_1 = ctk.CTkLabel(frame_page, text ="Page d'accueil", font=("Arial", 20, "bold") , fg_color= "black")
        label_1.place(relx=0.1 ,rely = 0.5)

        from joueur import Joueur
        button_changer_page = ctk.CTkButton(frame_page, text = "Aller au joueur" , command =lambda: self.controlleur.changer_page(Joueur))
        button_changer_page.place(relx = 0.7 , rely = 0.7)
