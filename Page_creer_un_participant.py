import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk





class page_creer_participant(ctk.CTkFrame):
     def __init__ (self, master=None , controlleur= None):
                super().__init__(master)
                self.master = master
                self.controlleur = controlleur 
                self.show_page()



     def recuperer_participant_choisi():
             from Page_créer_un_participant import page_creer_participant
             
             
     


     def show_page(self):
            self.frame_page = ctk.CTkFrame(self, width = 768 , height = 432, fg_color = "white")
            self.frame_page.place(x=0 , y=0 )
    
            #Le logo en haut à gauche
            image_pil = Image.open("images/logo.jpg")
            self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(84, 72))
            self.label_logo = ctk.CTkLabel(self.frame_page, text="", image = self.bg_image )
            self.label_logo.place(relx=0.05, rely=0.05)
            
            #titre de la page
            self.label_titre_page = ctk.CTkLabel(self.frame_page, text ="Créer un joueur",text_color="black" , font=("Arial",30 ,"bold"))
            self.label_titre_page.place(relx =0.5 ,rely =  0.13 , anchor = "center")
