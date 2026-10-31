import random
from pathlib import Path
import pandas as pd


class BanqueTournois:

    # Colonnes utilisees dans les deux fichiers CSV
    COL_T = ["id", "nom", "categorie", "nbRondes", "participants"]
    COL_M = ["tournoi_id", "ronde", "a", "b", "resultat"]

    # Initialiser la banque et charger les tournois existants
    def __init__(self, fichier="tournois.csv", fichier_matchs="matchs.csv"):
        self.fichier = Path(fichier)
        self.fichier_matchs = Path(fichier_matchs)
        self.tournois = []
        self.charger()

    # Charger les informations des tournois et des matchs
    def charger(self):
        if self.fichier.exists():
            df_t = pd.read_csv(self.fichier, dtype=str).fillna("")
        else:
            df_t = pd.DataFrame(columns=self.COL_T)

        if self.fichier_matchs.exists():
            df_m = pd.read_csv(self.fichier_matchs, dtype=str).fillna("")
        else:
            df_m = pd.DataFrame(columns=self.COL_M)

        self.tournois = []

        # Reconstruire chaque tournoi a partir des donnees CSV
        for _, ligne in df_t.iterrows():
            participants = [
                int(x)
                for x in ligne["participants"].split(";")
                if x.strip()
            ]

            tournoi = {
                "id": int(ligne["id"]),
                "nom": ligne["nom"],
                "categorie": ligne["categorie"],
                "nbRondes": int(ligne["nbRondes"]),
                "participants": participants,
                "rondes": []
            }

            # Recuperer les matchs appartenant a ce tournoi
            matchs = df_m[
                df_m["tournoi_id"] == str(tournoi["id"])
            ]

            numeros = sorted(
                set(int(x) for x in matchs["ronde"])
            )

            for numero in numeros:
                lignes = matchs[
                    matchs["ronde"] == str(numero)
                ]

                ronde = []

                for _, m in lignes.iterrows():
                    ronde.append({
                        "a": int(m["a"]),
                        "b": int(m["b"]) if m["b"] else None,
                        "resultat": m["resultat"] or None
                    })

                tournoi["rondes"].append(ronde)

            self.tournois.append(tournoi)

    # Sauvegarder les tournois et les matchs dans deux CSV
    def sauvegarder(self):
        donnees_t = []
        donnees_m = []

        for tournoi in self.tournois:
            donnees_t.append({
                "id": tournoi["id"],
                "nom": tournoi["nom"],
                "categorie": tournoi["categorie"],
                "nbRondes": tournoi["nbRondes"],
                "participants": ";".join(
                    map(str, tournoi["participants"])
                )
            })

            # Enregistrer chaque match avec son numero de ronde
            for numero, ronde in enumerate(tournoi["rondes"], start=1):
                for match in ronde:
                    donnees_m.append({
                        "tournoi_id": tournoi["id"],
                        "ronde": numero,
                        "a": match["a"],
                        "b": match["b"] if match["b"] is not None else "",
                        "resultat": match["resultat"] or ""
                    })

        pd.DataFrame(
            donnees_t, columns=self.COL_T
        ).to_csv(self.fichier, index=False)

        pd.DataFrame(
            donnees_m, columns=self.COL_M
        ).to_csv(self.fichier_matchs, index=False)

    # Creer et enregistrer un nouveau tournoi
    def enregistrer(self, nom, categorie, participants, nbRondes=3):
        nom = nom.strip()
        categorie = categorie.strip()
        participants = [int(p) for p in participants]

        # Verifier les informations fournies
        if not nom or not categorie:
            raise ValueError("Nom et categorie obligatoires.")

        if len(participants) < 2:
            raise ValueError("Il faut au moins 2 joueurs.")

        if len(participants) != len(set(participants)):
            raise ValueError("Un joueur est en double.")

        if not 1 <= nbRondes <= 30:
            raise ValueError("Entre 1 et 30 rondes.")

        # Empecher deux tournois avec le meme nom
        for tournoi in self.tournois:
            if tournoi["nom"].casefold() == nom.casefold():
                raise ValueError("Ce tournoi existe deja.")

        tournoi = {
            "id": max(
                (t["id"] for t in self.tournois),
                default=0
            ) + 1,
            "nom": nom,
            "categorie": categorie,
            "participants": participants,
            "nbRondes": nbRondes,
            "rondes": []
        }

        self.tournois.append(tournoi)
        self.sauvegarder()

        return tournoi

    # Rechercher un tournoi selon son nom ou sa categorie
    def rechercher(self, recherche=""):
        recherche = recherche.strip().casefold()

        return [
            t for t in self.tournois
            if recherche in t["nom"].casefold()
            or recherche in t["categorie"].casefold()
        ]

    # Calculer les statistiques des joueurs du tournoi
    def statistiques(self, tournoi):
        stats = {
            p: {
                "points": 0,
                "v": 0,
                "n": 0,
                "d": 0,
                "repos": 0,
                "adversaires": []
            }
            for p in tournoi["participants"]
        }

        # Parcourir les resultats de toutes les rondes
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

                stats[a]["adversaires"].append(b)
                stats[b]["adversaires"].append(a)

                # Victoire du joueur A
                if resultat == "A":
                    stats[a]["points"] += 2
                    stats[a]["v"] += 1
                    stats[b]["d"] += 1

                # Victoire du joueur B
                elif resultat == "B":
                    stats[b]["points"] += 2
                    stats[b]["v"] += 1
                    stats[a]["d"] += 1

                # Match nul : 1 point par joueur
                elif resultat == "N":
                    stats[a]["points"] += 1
                    stats[b]["points"] += 1
                    stats[a]["n"] += 1
                    stats[b]["n"] += 1

        return stats

    # Calculer le classement avec les points et le Buchholz
    def classement(self, tournoi):
        stats = self.statistiques(tournoi)

        # Buchholz : somme des points des adversaires rencontres
        buchholz = {
            p: sum(
                stats[adv]["points"]
                for adv in info["adversaires"]
            )
            for p, info in stats.items()
        }

        # Trier les joueurs selon les points puis le Buchholz
        joueurs = sorted(
            tournoi["participants"],
            key=lambda p: (
                -stats[p]["points"],
                -buchholz[p],
                p
            )
        )

        # Construire un DataFrame pour l'affichage
        donnees = []

        for p in joueurs:
            donnees.append({
                "ID": p,
                "Points": stats[p]["points"],
                "V": stats[p]["v"],
                "N": stats[p]["n"],
                "D": stats[p]["d"],
                "Buchholz": buchholz[p]
            })

        return pd.DataFrame(donnees)

    # Verifier si tous les matchs de la ronde sont termines
    def ronde_terminee(self, tournoi):
        return bool(tournoi["rondes"]) and all(
            m["resultat"] is not None
            for m in tournoi["rondes"][-1]
        )

    # Generer une ronde suisse simplifiee
    def prochaine_ronde(self, tournoi):
        if len(tournoi["rondes"]) >= tournoi["nbRondes"]:
            raise ValueError("Toutes les rondes sont terminees.")

        if tournoi["rondes"] and not self.ronde_terminee(tournoi):
            raise ValueError("Termine tous les matchs avant de continuer.")

        stats = self.statistiques(tournoi)
        joueurs = tournoi["participants"].copy()

        # Premiere ronde aleatoire, autres rondes selon les points
        random.shuffle(joueurs)

        if tournoi["rondes"]:
            joueurs.sort(
                key=lambda p: stats[p]["points"],
                reverse=True
            )

        ronde = []

        # Si le nombre de joueurs est impair, attribuer un repos
        if len(joueurs) % 2 != 0:
            repos = next(
                (
                    p for p in reversed(joueurs)
                    if stats[p]["repos"] == 0
                ),
                joueurs[-1]
            )

            joueurs.remove(repos)

            ronde.append({
                "a": repos,
                "b": None,
                "resultat": "REPOS"
            })

        # Memoriser les confrontations precedentes
        rencontres = {
            frozenset((m["a"], m["b"]))
            for r in tournoi["rondes"]
            for m in r
            if m["b"] is not None
        }

        # Chercher des appariements sans repetition
        essais = [0]

        def apparier(restants):
            if not restants:
                return []

            essais[0] += 1

            # Limiter les recherches pour ne pas bloquer la fenetre
            if essais[0] > 15000:
                return None

            a = restants[0]

            # Prioriser les adversaires ayant un score semblable
            options = sorted(
                restants[1:],
                key=lambda b: abs(
                    stats[a]["points"] - stats[b]["points"]
                )
            )

            for b in options:
                if frozenset((a, b)) in rencontres:
                    continue

                suite = apparier([
                    p for p in restants[1:]
                    if p != b
                ])

                if suite is not None:
                    return [(a, b)] + suite

            return None

        paires = apparier(joueurs)

        # Si aucun appariement sans repetition n'est trouve,
        # accepter certaines repetitions
        if paires is None:
            paires = []
            restants = joueurs.copy()

            while restants:
                a = restants.pop(0)

                b = min(
                    restants,
                    key=lambda p: (
                        frozenset((a, p)) in rencontres,
                        abs(stats[a]["points"] - stats[p]["points"])
                    )
                )

                restants.remove(b)
                paires.append((a, b))

        # Ajouter les matchs a la nouvelle ronde
        for a, b in paires:
            ronde.append({
                "a": a,
                "b": b,
                "resultat": None
            })

        tournoi["rondes"].append(ronde)
        self.sauvegarder()

        return ronde

    # Enregistrer ou modifier le resultat d'un match
    def enregistrer_resultat(self, tournoi, indice, resultat):
        if resultat not in (None, "A", "B", "N"):
            raise ValueError("Resultat invalide.")

        if not tournoi["rondes"]:
            raise ValueError("Aucune ronde commencee.")

        match = tournoi["rondes"][-1][indice]

        if match["b"] is None:
            raise ValueError("Un repos ne peut pas etre modifie.")

        match["resultat"] = resultat
        self.sauvegarder()
