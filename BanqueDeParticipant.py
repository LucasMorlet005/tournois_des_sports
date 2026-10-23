import pandas as pd
import Participant
from Participant import Participant

class BanqueParticipant :
    def __init__(self, fichier) :
        self.banqueParticipant: list[Participant] = []

        # passer les participants d'un csv à un framework
        participantDF = pd.read_csv(fichier)

        # mettre les participants comme objet Participant
        # du dataframe à la liste
        for _, row in participantDF.iterrows() :
            id = row[0]
            nom = row[1]
            categorie = row[2]
            nbTournoi = row[3]
            victoire = row[4]
            defaite = row[5]
            nulle = row[6]
            pointsPour = row[7]
            pointsContre = row[8]
            
            participantEnCours = Participant(id, nom, categorie,nbTournoi, victoire, defaite, nulle, pointsPour, pointsContre)
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