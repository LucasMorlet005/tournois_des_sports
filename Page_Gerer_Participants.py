import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class Page_Gerer_Participants(ctk.CTkFrame):
    def __init__ (self, master=None , controlleur= None):
            super().__init__(master)
            self.master = master
            self.controlleur = controlleur 
            self.participants = self.controlleur.mes_participants #juste pour avoir la liste avec un nom plus court, et puisqe 
            self.noms_participants = [p.nom for p in self.participants]  #la liste des nom pour la combobox des noms
            self.categories = list(set(p.categorie for p in self.participants)) # la liste des categories pour la combobox des categories

            #dictionnaire pour la combobox des noms et categorie
            self.recherche_combine_dict = {participant.nom : participant.categorie for participant in self.participants} 
             #liste pour la combobox des noms et categorie
            self.valeurs_recherche_combinee =  self.transformer_dictionnaire_en_liste(self.recherche_combine_dict,5)

            #variable qui est la valeur entrée dans la combobox de noms , mise ici pour que toutes les fonctions y ai accès
            self.recherche_nom = tk.StringVar()
            #variable qui est la valeur entrée dans la combobox de categories , mise ici pour que toutes les fonctions y ai accès
            self.recherche_categorie = tk.StringVar()

            self.show_page()
       


    def mettre_a_jour_participant_choisi(self):

            #On prends par défaut le joueur dans la combobox combiné comme joueur sélectionné
        self.participant_choisi = self.recherche_combine_combobox.get()


        if self.participant_choisi == "":
            print("Aucun joueur n'a été selectionné")
            from accueil import Accueil
            self.controlleur.changer_page( Accueil)

            #On split la varible en 2, le nom et la catégorie, pour n'utiliser que le prénom et le nom
        self.liste_participant_et_categorie = self.participant_choisi.split()
        nom_complet = self.liste_participant_et_categorie[0] + " " + self.liste_participant_et_categorie[1]
            #on cherche le participant ayant le meme nom dans notre banque de participant, puis on met à jour le participant_actuel
        self.controlleur.participant_actuel = self.participants.rechercherParticipantNom(nom_complet)
   



            #fonction pour transformer un dicitonnaire en liste pour l'affichage de la combobox qui combine le nom et la categorie
    def transformer_dictionnaire_en_liste(self,dictionnaire, nbr_espaces): 
        espaces = nbr_espaces * " "
        return [ f"{a}{espaces}{b}"   for a , b in dictionnaire.items() ]
    


        #fonction pour mettre à jour la combobox de participants quand l'utilisateur tape son nom 
    def uptade_liste_noms(self , *args):
            #mettre la liste de noms a jour selon ce que l'utilisateur a entré
         self.nouvelle_liste_noms = [ participant for participant in self.noms_participants if self.recherche_nom.get().lower() in participant.lower() ]
            #mettre à jour la combobox de nom
         self.liste_nom_combobox.configure(values = self.nouvelle_liste_noms)
            #mettre à jour la combobox qui combine nom et categorie 
         self.uptade_recherche_combine()



        #fonction pour mettre à jour la combobox de categories quand l'utilisateur tape la categorie
    def uptade_liste_categories(self , *args):
                #mettre la liste de categories a jour selon ce que l'utilisateur a entré
            self.nouvelle_liste_categories= [ categorie for categorie in self.categories if self.recherche_categorie.get().lower() in categorie.lower() ]
                #mettre à jour la combobox de categories
            self.liste_categorie_combobox.configure(values = self.nouvelle_liste_categories)
                #mettre à jour la combobox qui combine nom et categorie 
            self.uptade_recherche_combine()




        #fonction pour mettre à jour la combobox qui combine les 2 recherches
    def uptade_recherche_combine(self):

            #On va chercher ce que l'utilisateur a entré dans les combobox de nom et de categorie
        self.texte_nom = self.recherche_nom.get().lower()
        self.texte_cat = self.recherche_categorie.get().lower()

            #Vérifier si les deux entrées sont vide, dans ce cas on renvoit simplement la liste de base
        if(self.texte_nom == "" and self.texte_cat == ""):
             self.recherche_combine_combobox.configure(values = self.valeurs_recherche_combinee)
             return 0 

        
            #création du nouveau dictionnaire avec les éléments qui répondent aux 2 entrées de l'utilisateur
            #On vérifie entre les entrées et le dictionnaire de base
        self.nouveau_dictionnaire_recherche_combine = {
                    nom: categorie for nom, categorie in self.recherche_combine_dict.items()
                    if self.texte_nom in nom.lower() and self.texte_cat in categorie.lower()   }

            # On transforme le dictionnaire filtré en liste pour l.affichage
        self.nouvelle_liste_recherche_combine = self.transformer_dictionnaire_en_liste(
            self.nouveau_dictionnaire_recherche_combine, 5
        )

            #On met à jour la combobox 
        self.recherche_combine_combobox.configure(values=self.nouvelle_liste_recherche_combine)
            


         #affichage de la page
    def show_page(self):
            #le frame de la page
        self.frame_page = ctk.CTkFrame(self, width = 768 , height = 432, fg_color = "white")
        self.frame_page.place(x=0 , y=0 )

        #Le logo en haut à gauche
        try:
            image_pil = Image.open("images/logo.jpg")
        except:
             image_pil = None
             print("Aucunne image trouvée")
        self.bg_image = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(84, 72)) #création de L'image pour que ctk la comprenne
        self.label_logo = ctk.CTkLabel(self.frame_page, text="", image = self.bg_image ) #Label où l'on va mettre l'image
        self.label_logo.place(relx=0.05, rely=0.05) #placer l'image sur la frame
        
        #titre de la page
        self.label_titre_page = ctk.CTkLabel(self.frame_page, text ="Gestionnaire des participants",text_color="black" , font=("Arial",30 ,"bold"))
        self.label_titre_page.place(relx =0.5 ,rely =  0.13 , anchor = "center")

        #label pour la recherche par le nom
        self.label_recherche_nom = ctk.CTkLabel(self.frame_page, text = "Rechercher par nom:" , text_color="black" , font=("Arial", 15, "bold"))
        self.label_recherche_nom.place(relx =0.2 , rely = 0.45, anchor = "center")

        #combobox pour la recherche par les noms
            #apelle la fonction qui mets à jour la combobox quand l'entrée de l'utilisateur est modifié
        self.recherche_nom.trace_add("write", self.uptade_liste_noms)#non il ne faut pas mettre de parenthèse à self.uptade_liste_noms, demande pas pourquoi
            #combobox de noms des participants 
        self.liste_nom_combobox = ctk.CTkComboBox(self.frame_page, values = self.noms_participants, variable = self.recherche_nom , height = 35 , width= 175)
        self.liste_nom_combobox.place(relx = 0.2 , rely = 0.55 , anchor = "center")

        #label pour la recherche par la catégorie
        self.label_recherche_categorie = ctk.CTkLabel(self.frame_page, text = "Rechercher par catégorie:" , text_color="black" , font=("Arial", 15, "bold"))
        self.label_recherche_categorie.place(relx = 0.5, rely=0.45, anchor = "center")

        #combobox pour la recherche par la categorie
            #apelle la fonction qui met à jour la combobox quand l'entrée de l'utilisateur est modifié
        self.recherche_categorie.trace_add("write", self.uptade_liste_categories) #non il ne faut pas mettre de parenthèse à self.uptade_liste_categories, demande pas pourquoi
            #combobox des catégories 
        self.liste_categorie_combobox = ctk.CTkComboBox(self.frame_page, values = self.categories, variable = self.recherche_categorie , height = 35 , width= 175)
        self.liste_categorie_combobox.place(relx = 0.5, rely = 0.55, anchor = "center")



         #label pour la combobox qui combine les 2 recherches
        self.label_recherche_combine = ctk.CTkLabel(self.frame_page, text = "Résultats de vos recherches:\n Nom       Catégorie" , text_color="black" , font=("Arial", 15, "bold"))
        self.label_recherche_combine.place(relx = 0.82, rely=0.45, anchor = "center")
        

         #combobox qui combine les résultats des 2 autres combobox
            #ici on a pas de variable pour l'entrée, car ce n'est pas nécessaire et cela ferait des conflits
        self.recherche_combine_combobox = ctk.CTkComboBox(self.frame_page, values = self.valeurs_recherche_combinee , height = 35 , width= 175)
        self.recherche_combine_combobox.place(relx = 0.82, rely = 0.55, anchor = "center")
        

          #bouton pour créer un joueur
        #from 
        self.button_accueil = ctk.CTkButton(self.frame_page, text = "Créer un joueur" , command = lambda: self.controlleur.changer_page( Accueil) , fg_color= "indigo")
        self.button_accueil.place(relx = 0.5 ,rely = 0.85 ,anchor = "center" )


           #bouton pour voir les statistique du joueur choisi
        self.button_accueil = ctk.CTkButton(self.frame_page, text = "Voir les statistique\n du joueur choisi" , command = lambda: self.voir_statistiques_joueur(), fg_color= "green")
        self.button_accueil.place(relx = 0.85 ,rely = 0.85 ,anchor = "center")



        #bouton pour retourner à l'accueil
        from accueil import Accueil
        self.button_accueil = ctk.CTkButton(self.frame_page, text = "Aller à l'ACCUEIL" , command = lambda: self.controlleur.changer_page( Accueil) , fg_color= "blue")
        self.button_accueil.place(relx = 0.15 ,rely = 0.85, anchor = "center")


    def voir_statistiques_joueur(self):
         self.mettre_a_jour_participant_choisi()
         from Page_statistiques_participant import page_visualiser_participant
         self.controlleur.changer_page( page_visualiser_participant)
