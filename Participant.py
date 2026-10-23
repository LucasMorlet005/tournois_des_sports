class Participant :
    def __init__(self, id, nom, categorie, nbTournoi=0, victoire=0, defaite=0, nulle=0, pointsPour=0, pointsContre=0):
        self.id = id
        self.nom = nom
        self.categorie = categorie

        self.nbTournoi = nbTournoi
        self.fiche = [victoire, defaite, nulle] #victoire, défaite, égalité
        self.points = [pointsPour, pointsContre] # points pour, point contre

    def __init__(self, id, nom, categorie):
        self.__init__(id, nom, categorie, 0, 0, 0, 0, 0, 0)


    def calculerDifferenciel(self) :
        # le différentiel est la différence entre les points pour et les points contre
        return self.points[0] - self.points[1]

    def calculerPourcentageVictoire(self) :
        # une victoire vaut 2 points, une égalité 1 et une défaite aucun.
        # le pourcentage de victoire est le ratio de points sur
        # la possibilité totale de points (2 par  matchs)

        return (self.fiche[0] * 2 + self.fiche[1]) / (2 * (self.fiche[0] + self.fiche[1] + self.fiche[2]))

    def __string__(self) :
        return f"{self.nom} : {self.calculerPourcentageVictoire} % de victoire."