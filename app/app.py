#Import de Flask et de la fonction render_template depuis le
#module flask
from flask import Flask, render_template

#Import de SQLAlchemy depuis la version flask_sqlalchemy, qui permet d'interagir avec la base de données
from flask_sqlalchemy import SQLAlchemy

#Import d'un package pour faciliter la migration de la base de données en cas de modifications
#de la structure des données
from flask_migrate import Migrate

#Import du package pour gérer les sessions utilisateurs
from flask_login import LoginManager

#Import du module pour faire des transactions sécurisées
from .constantes import SECRET_KEY


#Import du package os permettant de communqiuer avec les différents systèmes d'exploitation (Mac, Ubuntu, etc.).
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

#Configuration du secret pour sécuriser les transactions
app.config['SECRET_KEY'] = SECRET_KEY

#Configuration de la base de données 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./epistautograpy.sqlite'

#Configuration pour signaler les modifications dans la base de données
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initiation de l'objet SQLAlchemy
db = SQLAlchemy(app)

#Initation de l'objet Migrate
migrate = Migrate(app, db)

# On met en place la gestion d'utilisateurs.rices
login = LoginManager(app)

#Import des pages correspondantes depuis le fichier routes.py
from .routes import accueil, index_lettres, index_dates, index_destinataires, index_contresignataires, index_institutions_conservations, formulaire_lettre, formulaire_destinataire, formulaire_institution, modification_lettre, modification_destinataire, modification_institution, suppression_lettre, suppression_destinataire, suppression_institution, recherche, rechercheavancee, lettre, date, destinataire, contresignataire, institution, inscription, connexion, deconnexion, cgu, about
from .gestion_erreurs import not_found, gone, internal_server_error


#Fonction pour créer toutes les tables et qu'elles soient reconnues lors du lancement de l'application
def init_db():
	print("Initialisation de la base de données en cours")
	db.drop_all()
	print("Création des tables de la base de données")
	db.create_all()

