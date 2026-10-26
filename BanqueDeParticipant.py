import pandas as pd
import Participant
from Participant import Participant

class BanqueDeParticipant :
    def __init__(self, fichier) :
        self.banqueParticipant: list[Participant] = []

        # passer les participants d'un csv à un framework
        participantDF = pd.read_csv(fichier)

        # mettre les participants comme objet Participant
        # du dataframe à la liste
        for _, row in participantDF.iterrows() :
            id = row['id']
            nom = row['nom']
            categorie = row['categorie']
            nbTournoi = row['nbTournoi']
            victoire = row['victoire']
            defaite = row['defaite']
            nulle = row['nulle']
            pointsPour = row['pointsPour']
            pointsContre = row['pointsContre']

            
            participantEnCours = Participant(id, nom, categorie,nbTournoi, victoire, defaite, nulle, pointsPour, pointsContre)
            print(participantEnCours)   
            self.banqueParticipant.append(participantEnCours)
            

    # obtenir une liste des joueurs selon leurs catégories
    def trierParticipantUneCategorie(self, categorie):
        participantDeCategorie = []
        for participant in self.banqueParticipant :
            if participant.categorie == categorie :
                participantDeCategorie.append(participant)

        return participantDeCategorie

    # trouver un participant selon son id
    def rechercherParticipantid(self, id) :
        for participant in self.banqueParticipant :
            if participant.id == id :
                return participant

        return None