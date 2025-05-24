from uuid import uuid4

class game:
    def __init__(self, mot_secret):
        self.mot_secret = mot_secret.upper()
        self.utilisateurs = {}
        self.longueur_mot = len(self.mot_secret)

    def creer_utilisateur(self):
        identifiant = str(uuid4())
        self.utilisateurs[identifiant] = []
        return identifiant
    




    def utilisateur_valide(self, identifiant):
        return identifiant in self.utilisateurs
    





    def verifier_proposition(self, identifiant, proposition):
        proposition = proposition.upper()
        if len(proposition) != self.longueur_mot or not proposition.isalpha():
            return {"erreur": "Proposition invalide"}

        resultat = [""] * self.longueur_mot
        lettres_cibles = list(self.mot_secret)
        lettres_proposees = list(proposition)
        lettres_correctes = [False] * self.longueur_mot



        for i in range(self.longueur_mot):
            if lettres_proposees[i] == lettres_cibles[i]:
                resultat[i] = "Correct"
                lettres_correctes[i] = True

        for i in range(self.longueur_mot):
            if resultat[i]:
                continue
            lettre = lettres_proposees[i]
            nombre_dans_mot = sum(lettres_cibles[j] == lettre and not lettres_correctes[j] for j in range(self.longueur_mot))
            deja_proposee = sum(lettres_proposees[k] == lettre and resultat[k] == "Mal placée" for k in range(i))

            if nombre_dans_mot > deja_proposee:
                resultat[i] = "Mal placée"
            else:
                resultat[i] = "Incorrect"

        self.utilisateurs[identifiant].append((proposition, resultat))
        return {"proposition": proposition, "retour": resultat}
    

    

    def recuperer_etat(self, identifiant):
        if not self.utilisateur_valide(identifiant):
            return {"erreur": "Utilisateur inconnu"}

        termine = any("".join(retour) == "Correct" * self.longueur_mot for _, retour in self.utilisateurs[identifiant])
        return {
            "tentatives": self.utilisateurs[identifiant],
            "termine": termine
        }
