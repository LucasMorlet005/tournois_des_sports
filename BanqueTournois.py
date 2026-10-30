import json
import random
from pathlib import Path
import pandas as pd


class BanqueTournois:
    # Constructeur : charger les tournois sauvegardes dans le fichier JSON
    def __init__(self, fichier="tournois.json"):
        self.fichier = Path(fichier)
        self.tournois = []

        if self.fichier.exists():
            with open(self.fichier, "r", encoding="utf-8") as f:
                self.tournois = json.load(f)

    # Enregistrer les tournois pour les conserver apres la fermeture
    def sauvegarder(self):
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(self.tournois, f, indent=4, ensure_ascii=False)

    # Creer un tournoi avec une categorie et une liste de participants
    def enregistrer(self, nom, categorie, participants, nbRondes=3):
        nom = nom.strip()
        categorie = categorie.strip()
        participants = [int(p) for p in participants]

        # Verifier les informations entrees par l'utilisateur
        if not nom or not categorie:
            raise ValueError("Le nom et la categorie sont obligatoires.")

        if len(participants) < 2:
            raise ValueError("Il faut au moins 2 participants.")

        if len(participants) != len(set(participants)):
            raise ValueError("Un participant est en double.")

        if nbRondes < 1:
            raise ValueError("Il faut au moins une ronde.")

        # Empecher deux tournois d'avoir le meme nom
        for tournoi in self.tournois:
            if tournoi["nom"].lower() == nom.lower():
                raise ValueError("Ce tournoi existe deja.")

        nouveau = {
            "id": max((t["id"] for t in self.tournois), default=0) + 1,
            "nom": nom,
            "categorie": categorie,
            "participants": participants,
            "nbRondes": nbRondes,
            "rondes": []
        }

        self.tournois.append(nouveau)
        self.sauvegarder()

        return nouveau

    # Rechercher un tournoi selon son nom ou sa categorie
    def rechercher(self, recherche=""):
        recherche = recherche.strip().lower()

        return [
            tournoi for tournoi in self.tournois
            if recherche in tournoi["nom"].lower()
            or recherche in tournoi["categorie"].lower()
        ]

    # Calculer les statistiques de chaque joueur du tournoi
    def statistiques(self, tournoi):
        stats = {
            pid: {
                "points": 0,
                "victoires": 0,
                "defaites": 0,
                "nulles": 0,
                "repos": 0,
                "adversaires": []
            }
            for pid in tournoi["participants"]
        }

        # Parcourir toutes les rondes et leurs resultats
        for ronde in tournoi["rondes"]:
            for match in ronde:
                a = match["a"]
                b = match["b"]
                resultat = match["resultat"]

                # Un repos donne automatiquement 2 points
                if b is None:
                    stats[a]["points"] += 2
                    stats[a]["repos"] += 1
                    continue

                # Garder l'historique des adversaires
                stats[a]["adversaires"].append(b)
                stats[b]["adversaires"].append(a)

                # Une victoire donne 2 points
                if resultat == "A":
                    stats[a]["points"] += 2
                    stats[a]["victoires"] += 1
                    stats[b]["defaites"] += 1

                elif resultat == "B":
                    stats[b]["points"] += 2
                    stats[b]["victoires"] += 1
                    stats[a]["defaites"] += 1

                # Un match nul donne 1 point a chaque joueur
                elif resultat == "N":
                    stats[a]["points"] += 1
                    stats[b]["points"] += 1
                    stats[a]["nulles"] += 1
                    stats[b]["nulles"] += 1

        return stats

    # Calculer le classement selon les points et le departage Buchholz
    def classement(self, tournoi):
        stats = self.statistiques(tournoi)

        # Buchholz : somme des points des adversaires rencontres
        buchholz = {}

        for pid, info in stats.items():
            buchholz[pid] = sum(
                stats[adversaire]["points"]
                for adversaire in info["adversaires"]
            )

        # Trier d'abord selon les points, ensuite selon le Buchholz
        joueurs = sorted(
            tournoi["participants"],
            key=lambda pid: (
                -stats[pid]["points"],
                -buchholz[pid],
                pid
            )
        )

        # Construire un DataFrame avec Pandas pour le classement
        donnees = []

        for rang, pid in enumerate(joueurs, 1):
            donnees.append({
                "Rang": rang,
                "ID": pid,
                "Points": stats[pid]["points"],
                "Victoires": stats[pid]["victoires"],
                "Nulles": stats[pid]["nulles"],
                "Defaites": stats[pid]["defaites"],
                "Buchholz": buchholz[pid]
            })

        return pd.DataFrame(donnees)

    # Verifier si tous les matchs de la derniere ronde sont termines
    def ronde_terminee(self, tournoi):
        if not tournoi["rondes"]:
            return False

        return all(
            match["resultat"] is not None
            for match in tournoi["rondes"][-1]
        )

    # Generer une nouvelle ronde selon un systeme suisse simplifie
    def prochaine_ronde(self, tournoi):
        if len(tournoi["rondes"]) >= tournoi["nbRondes"]:
            raise ValueError("Toutes les rondes sont terminees.")

        if tournoi["rondes"] and not self.ronde_terminee(tournoi):
            raise ValueError("Tous les matchs doivent etre termines.")

        stats = self.statistiques(tournoi)
        joueurs = list(tournoi["participants"])
        matchs = []

        # Memoriser les rencontres des rondes precedentes
        rencontres = set()

        for ronde in tournoi["rondes"]:
            for match in ronde:
                if match["b"] is not None:
                    rencontres.add(
                        frozenset((match["a"], match["b"]))
                    )

        # Premiere ronde aleatoire
        if not tournoi["rondes"]:
            random.shuffle(joueurs)

        else:
            # Rondes suivantes : classer selon le nombre de points
            random.shuffle(joueurs)
            joueurs.sort(
                key=lambda pid: stats[pid]["points"],
                reverse=True
            )

        # Si le nombre de joueurs est impair, donner un repos
        if len(joueurs) % 2 != 0:
            repos = next(
                (
                    pid for pid in reversed(joueurs)
                    if stats[pid]["repos"] == 0
                ),
                joueurs[-1]
            )

            joueurs.remove(repos)

            matchs.append({
                "a": repos,
                "b": None,
                "resultat": "REPOS"
            })

        # Chercher des paires sans repetition, si possible
        def apparier(restants):
            if not restants:
                return []

            joueur1 = restants[0]

            # Prioriser les joueurs avec un score semblable
            adversaires = sorted(
                restants[1:],
                key=lambda pid: abs(
                    stats[joueur1]["points"] - stats[pid]["points"]
                )
            )

            for joueur2 in adversaires:
                paire = frozenset((joueur1, joueur2))

                if paire in rencontres:
                    continue

                autres = [
                    pid for pid in restants[1:]
                    if pid != joueur2
                ]

                suite = apparier(autres)

                if suite is not None:
                    return [(joueur1, joueur2)] + suite

            return None

        paires = apparier(joueurs)

        # Si aucune combinaison parfaite n'est possible,
        # accepter certaines rencontres deja jouees
        if paires is None:
            paires = []

            while joueurs:
                joueur1 = joueurs.pop(0)

                joueur2 = min(
                    joueurs,
                    key=lambda pid: (
                        frozenset((joueur1, pid)) in rencontres,
                        abs(
                            stats[joueur1]["points"]
                            - stats[pid]["points"]
                        )
                    )
                )

                joueurs.remove(joueur2)
                paires.append((joueur1, joueur2))

        # Creer les matchs de la nouvelle ronde
        for joueur1, joueur2 in paires:
            matchs.append({
                "a": joueur1,
                "b": joueur2,
                "resultat": None
            })

        tournoi["rondes"].append(matchs)
        self.sauvegarder()

        return matchs

    # Enregistrer ou modifier le resultat d'un match
    def enregistrer_resultat(self, tournoi, indice, resultat):
        if resultat not in ("A", "B", "N", None):
            raise ValueError("Resultat invalide.")

        if not tournoi["rondes"]:
            raise ValueError("Aucune ronde en cours.")

        match = tournoi["rondes"][-1][indice]

        if match["b"] is None:
            raise ValueError("Impossible de modifier un repos.")

        match["resultat"] = resultat
        self.sauvegarder()
