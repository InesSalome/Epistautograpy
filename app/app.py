#!/usr/bin/python
# -*- coding: utf-8 -*-
#Import de Flask et de la fonction render_template depuis le 
#module flask.
from flask import Flask, render_template
#Import de SQLAlchemy depuis la version flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
#Import d'un package pour faciliter la migration de la base de données en cas de modifications
#de la structure des données
from flask_migrate import Migrate
#Import du package pour gérer les sessions utilisateurs
from flask_login import LoginManager
#Import du module pour faire des transactions sécurisées
from .constantes import SECRET_KEY

#Import du package os permettant de faire des opérations liées au système.
import os
import os.path
#Stockage du chemin du fichier courant
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
#Stockages des chemins vers les dossiers templates et statics.
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

#Création de l'application en tant qu'instance de la classe Flask, elle-même
#importée du package flask.
#Nommage de l'application, obligatoire dans Flask pour faire tourner
#plusieurs applications sur le même serveur. 
app = Flask(
	"Application",
	template_folder=templates,
    static_folder=statics
)
#Configuration du secret
app.config['SECRET_KEY'] = SECRET_KEY
#Configuration de la base de données 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./epistautograpy.db'
#Configuration pour signaler les modifications dans la base de données
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#Initiation de l'objet SQLAlchemy avec la variable application tout en
#le stockant dans la variable db.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# On met en place la gestion d'utilisateur-rice-s
login = LoginManager(app)

#Import des pages correspondantes depuis le dossier routes.
from .routes import accueil, lettre, index_lettres, index_dates, index_destinataires, index_contresignataires, index_institution_conservation, formulaire, recherche, rechercheavancee, inscription, connexion, deconnexion, formulaire_lettre, formulaire_destinataire, formulaire_institution, formulaire_image, about

#Fonction pour créer toutes les tables et qu'elles soient reconnues lors du lancement de l'application
def init_db():
	db.create_all()

if __name__ == '__main__':
	init_db()

