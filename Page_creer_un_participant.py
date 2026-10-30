import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from BanqueDeParticipant import BanqueDeParticipant





class page_creer_participant(ctk.CTkFrame):
        def __init__ (self, master=None , controlleur= None):
                super().__init__(master)
                self.master = master
                self.controlleur = controlleur 
                self.categories = list(set(p.categorie for p in self.controlleur.mes_participants.banqueParticipant)) # la liste des categories pour la combobox des categories
                        #variable qui est la valeur entrée dans la combobox de categories , mise ici pour que toutes les fonctions y ai accès
                self.recherche_categorie = tk.StringVar()
                self.nom_entree = tk.StringVar()
                self.show_page()




               #fonction pour mettre à jour la combobox de categories quand l'utilisateur tape la categorie
        def uptade_liste_categories(self , *args):
                        #mettre la liste de categories a jour selon ce que l'utilisateur a entré
                self.nouvelle_liste_categories= [ categorie for categorie in self.categories if self.recherche_categorie.get().lower() in categorie.lower() ]
                        #mettre à jour la combobox de categories
                self.combobox_ecrire_categorie.configure(values = self.nouvelle_liste_categories)
                      



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

                        #label "choisir le nom"
                self.label_ecrire_nom= ctk.CTkLabel(self.frame_page, text ="NOM",text_color="black" , font=("Arial",17 ,"bold"),  height = 35 , width= 175)
                self.label_ecrire_nom.place(relx =0.3 ,rely =  0.4 , anchor = "center")

                self.entry_nom = ctk.CTkEntry(self.frame_page , placeholder_text= "écrire le nom" , textvariable = self.nom_entree)
                self.entry_nom.place(relx =0.3 ,rely =  0.52 , anchor = "center")



                        #label "choisir la catégorie"
                self.label_ecrire_categorie= ctk.CTkLabel(self.frame_page, text ="CATEGORIE",text_color="black" , font=("Arial",17 ,"bold"))
                self.label_ecrire_categorie.place(relx =0.7 ,rely =  0.4 , anchor = "center")

                        #combobox pour la recherche par la categorie
                        #apelle la fonction qui met à jour la combobox quand l'entrée de l'utilisateur est modifié
                self.recherche_categorie.trace_add("write", self.uptade_liste_categories) #non il ne faut pas mettre de parenthèse à self.uptade_liste_categories, demande pas pourquoi
                        #combobox des catégories 
                self.combobox_ecrire_categorie = ctk.CTkComboBox(self.frame_page, values = self.categories, variable = self.recherche_categorie , height = 35 , width= 175)
                self.combobox_ecrire_categorie.place(relx = 0.7, rely = 0.52, anchor = "center")



                  #bouton pour créer le participant
                self.button_creer_participant = ctk.CTkButton(self.frame_page, text = "CRÉER" ,font=("Arial",25 ,"bold") ,   command = lambda: self.creer_participant() , fg_color= "blue" , height = 35 , width= 175)
                self.button_creer_participant.place(relx = 0.5 ,rely = 0.75 , anchor = "center")


                #bouton pour retourner à l'accueil
                from accueil import Accueil
                self.button_accueil = ctk.CTkButton(self.frame_page, text = "Aller à l'ACCUEIL" , command = lambda: self.controlleur.changer_page( Accueil) , fg_color= "blue" , width=140, height=28)
                self.button_accueil.place(relx = 0.15 ,rely = 0.85, anchor = "center")



                # bouton pour aller à la page gérer les joueurs
                from Page_Gerer_Participants import Page_Gerer_Participants
                button_aller_page_participant = ctk.CTkButton(self.frame_page, text="Gérer les joueurs", command=lambda: self.controlleur.changer_page(Page_Gerer_Participants), fg_color= "blue" , width=140, height=28)
                button_aller_page_participant.place(relx = 0.8, rely = 0.85, anchor = "center")


        def creer_participant(self):
                self.nom =  self.nom_entree.get()
                self.categorie = self.recherche_categorie.get()

                if(self.nom == ""):
                        print("Tu dois entrer un nom !")
                        return 0
                if(self.categorie == ""):
                        print("Tu dois entrer une categorie !")
                        return 0

                if not self.nom.isalnum():
                        print("Nom d'utilisateur invalide, les caractères autre que les lettres sont interdits")
                        return 0

                if not self.categorie.isalnum():
                        print("Nom d'utilisateur invalide, les caractères autres que les lettres sont interdits")
                        return 0
                        
                
                
                self.id = self.controlleur.mes_participants.banqueParticipant[-1].id +1
                self.controlleur.mes_participants.creerParticipant(self.id,self.nom,self.categorie ,self.controlleur.mes_participants.banqueParticipant)
                self.recherche_categorie.set("")
                self.nom_entree.set("")
                print("Votre participant a bien été créé !")
                