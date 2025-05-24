from fastapi import APIRouter, Query, Cookie
from fastapi.responses import JSONResponse
from coeur.jeu import PartieMot
from uuid import uuid4
import random

routeur_api = APIRouter()

liste_mots_possibles = ["arbre", "chien", "fleur", "table", "livre", "pomme", "rouge", "plage",    "verre"]

mot_a_deviner = random.choice(liste_mots_possibles)
partie = PartieMot(mot_a_deviner)


@routeur_api.get("/initialiser-session")
async def initialiser_session():
    jeton_session = str(uuid4())
    reponse = JSONResponse({"session": jeton_session})
    reponse.set_cookie("session", jeton_session, httponly=True, samesite="Lax", max_age=3600)
    return reponse

@routeur_api.get("/connexion")
async def connecter_utilisateur(
    cle_query: str = Query(alias="session"),
    cle_cookie: str = Cookie(alias="session")
):
    if cle_query != cle_cookie:
        return {"erreur": "Jetons de session non concordants"}
    
    identifiant_utilisateur = partie.creer_utilisateur()
    reponse = JSONResponse({"identifiant": identifiant_utilisateur})
    reponse.set_cookie("identifiant", identifiant_utilisateur, httponly=True, samesite="None", max_age=3600)
    return reponse




@routeur_api.get("/proposer")
async def faire_proposition(
    mot: str,
    identifiant_query: str = Query(alias="identifiant"),
    identifiant_cookie: str = Cookie(alias="identifiant")
):
    if identifiant_query != identifiant_cookie:
        return {"erreur": "Identifiants non valides"}

    if not partie.utilisateur_valide(identifiant_query):
        return {"erreur": "Utilisateur inconnu"}

    return partie.verifier_proposition(identifiant_query, mot)






@routeur_api.get("/etat")
async def recuperer_etat_partie(
    identifiant_query: str = Query(alias="identifiant"),
    identifiant_cookie: str = Cookie(alias="identifiant")
):
    if identifiant_query != identifiant_cookie:
        return {"erreur": "Identifiants non valides"}

    return partie.recuperer_etat(identifiant_query)
