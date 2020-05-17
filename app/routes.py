#!/usr/bin/python
# -*- coding: utf-8 -*-
#Import de Flask et de la fonction render_template depuis le 
#module flask.
#Import de la variable request pour récupérer des informations depuis le formulaire
from flask import render_template, request, flash, redirect, url_for
from .app import app, db, login
from sqlalchemy import or_, and_, update
from sqlalchemy import distinct
from flask_login import login_user, current_user, logout_user
from flask_paginate import Pagination
from .modeles.utilisateurs import User
from .constantes import LETTRES_PAR_PAGE
from flask import flash, redirect, request
from .modeles.donnees import Authorship, Lettre, Correspondance, Destinataire, Institution_Conservation, Image_Numerisee

#Chemin vers la page d'accueil

#Le décorateur crée une association entre l'URL donnée
#comme argument et la fonction. On définit ensuite une route 
#qui renvoie le contenu de la réponse liée à une requête. 
@app.route("/")
#Fonction render_template qui prend commme premier argument 
#le chemin du template et ensuite des arguments nommés utilisés 
#comme des variables dans les templates.
def accueil(exemple=None):
	lettres = Lettre.query.filter(Lettre.date_envoie_lettre).all()
	return render_template("pages/accueil.html", nom="Epistautograpy", lettres=lettres)


#Chemins vers les indexs 

@app.route("/index_lettres")
def index_lettres():
	lettres = Lettre.query.order_by(Lettre.id_lettre).all()
	return render_template("pages/index_lettres.html", nom="Epistautograpy", lettres=lettres)

@app.route("/index_dates")
def index_dates():
	dates = Lettre.query.order_by(Lettre.date_envoie_lettre).all()
	return render_template("pages/index_dates.html", nom="Epistautograpy", dates=dates, lettre=lettre)

@app.route("/index_destinataires")
def index_destinataires():
	destinataires = Destinataire.query.order_by(Destinataire.identite_destinataire).distinct().all()
	return render_template("pages/index_destinataires.html", nom="Epistautograpy", destinataires=destinataires, destinataire=destinataire)

@app.route("/index_contresignataires")
def index_contresignataires():
	contresignataires = Lettre.query.with_entities(Lettre.contresignataire_lettre).distinct().order_by(Lettre.contresignataire_lettre).all()
	return render_template("pages/index_contresignataires.html", nom="Epistautograpy", contresignataires=contresignataires)

@app.route("/index_institutions_conservations")
def index_institutions_conservations():
	institutions = Institution_Conservation.query.order_by(Institution_Conservation.nom_institution_conservation).distinct().all()
	return render_template("pages/index_institutions_conservations.html", nom="Epistautograpy", institutions=institutions, institution_conservation=institution)


#Chemin vers les pages de contenu

#Création d'une route avec l'identifiant associé à chaque lettre dans la 
#base de données. On a conditionné le type de l'identifiant qui ne peut être
#qu'un entier.
@app.route("/lettre/<int:id_lettre>")
def lettre(id_lettre):

	"""Création d'une page de résultat vers une lettre
	:param id_lettre: Clé primaire dans la table Lettre
	:type id_lettre: integer
	:returns: création de la page
	:rtype: page HTML de la lettre souhaitée"""
	
	#Après avoir récupérer les valeurs d'attributs de la table Lettre, on filtre les autres
	#tables qui ont une clé étrangère correspondant au paramètre id_lettre, pour récupérer
	#les informations adéquates
	unique_lettre = Lettre.query.get(id_lettre)
	destinataire = Destinataire.query.filter(db.and_(Destinataire.id_destinataire==Correspondance.destinataire_id,Correspondance.lettre_id==Lettre.id_lettre, Lettre.id_lettre==id_lettre)).first()
	institution_conservation = Institution_Conservation.query.filter(db.and_(Institution_Conservation.id_institution_conservation==Lettre.institution_id, Lettre.id_lettre==id_lettre)).first()
	image_numerisee = Image_Numerisee.query.filter(db.and_(Image_Numerisee.lettre_id==Lettre.id_lettre, Lettre.id_lettre==id_lettre)).first()
	
	return render_template("pages/lettre.html", nom="Epistautograpy", lettre=unique_lettre, contresignataire=contresignataire, destinataire=destinataire, institution_conservation=institution_conservation, institution=institution, image_numerisee=image_numerisee)

@app.route("/date/<date_envoie_lettre>")
def date(date_envoie_lettre):

	"""Création d'une page de résultat depuis une date vers la lettre correspondante
	:param date_envoie_lettre: Attribut dans la table Lettre
	:type date_envoie_lettre: string
	:returns: création de la page
	:rtype: page HTML de la lettre souhaitée"""

	unique_date = Lettre.query.get(date_envoie_lettre)
	lettres = Lettre.query.filter(db.and_(Lettre.id_lettre==Lettre.id_lettre, Lettre.date_envoie_lettre==date_envoie_lettre)).order_by(Lettre.id_lettre).all()

	return render_template("pages/date.html", nom="Epistautograpy", date=unique_date, lettres=lettres)

@app.route("/destinataire/<int:id_destinataire>")
def destinataire(id_destinataire):

	"""Création d'une page de résultat vers un destinataire
	:param id_destinataire: Clé primaire dans la table Destinataire
	:type id_destinataire: integer
	:returns: création de la page
	:rtype: page HTML du destinataire souhaité"""

	#Après avoir récupérer les valeurs d'attributs de la table Destinataire, on filtre les autres
	#tables qui ont une clé étrangère correspondant au paramètre id_destinataire pour récupérer
	#les informations adéquates
	unique_destinataire = Destinataire.query.get(id_destinataire)
	lettres_recues = Lettre.query.filter(db.and_(Lettre.id_lettre==Lettre.id_lettre, Lettre.id_lettre==Correspondance.lettre_id, Correspondance.destinataire_id==Destinataire.id_destinataire, Destinataire.id_destinataire==id_destinataire)).order_by(Lettre.id_lettre).all()
	
	return render_template("pages/destinataire.html", nom="Epistautograpy", destinataire=unique_destinataire, lettres_recues=lettres_recues)

@app.route("/contresignataire/<contresignataire_lettre>")
def contresignataire(contresignataire_lettre):

	"""Création d'une page de résultat type pour les lettres signées par un même contresignataire
	:param nom_contresignataire: Nom du contresignataire indiqué dans la table Lettre
	:type id_lettre: string
	:returns: création de la page
	:rtype: page HTML de la lettre souhaitée"""

	unique_contresignataire = Lettre.query.get(contresignataire_lettre)
	lettres_signees = Lettre.query.filter(db.and_(Lettre.id_lettre==Lettre.id_lettre, Lettre.contresignataire_lettre==contresignataire_lettre)).order_by(Lettre.id_lettre).all()

	return render_template("pages/contresignataire.html", nom="Epistautograpy", contresignataire=unique_contresignataire, lettres_signees=lettres_signees, lettre=lettre)

@app.route("/institution/<int:id_institution_conservation>")
def institution(id_institution_conservation):

	"""Création d'une page de résultat vers une institution avec la liste des lettres qu'elle conserve
	:param id_institution_conservation: Clé primaire dans la table Institution_Conservation
	:type id_institution_conservation: integer
	:returns: création de la page
	:rtype: page HTML de l'institution souhaitée"""

	#Après avoir récupérer les valeurs d'attributs de la table Institution_Conservation, on filtre les autres
	#tables qui ont une clé étrangère correspondant au paramètre id_institution_conservation, pour récupérer
	#les informations adéquates
	unique_institution = Institution_Conservation.query.get(id_institution_conservation)
	lettres_conservees = Lettre.query.filter(db.and_(Lettre.id_lettre==Lettre.id_lettre, Lettre.institution_id==Institution_Conservation.id_institution_conservation, Institution_Conservation.id_institution_conservation==id_institution_conservation)).order_by(Lettre.id_lettre).all()
	
	return render_template("pages/institution.html", nom="Epistautograpy", institution=unique_institution, lettres_conservees=lettres_conservees, institution_conservation=institution)


#Chemins vers pages dynamiques 

#La page est disponible à la fois pour les méthodes http GET et POST
@app.route("/formulaire_lettre", methods=["GET", "POST"])
def formulaire_lettre():
	listeobjetlettre = Lettre.query.with_entities(Lettre.objet_lettre).distinct()
	listedatelettre = Lettre.query.with_entities(Lettre.date_envoie_lettre).distinct()
	listelieulettre = Lettre.query.with_entities(Lettre.lieu_ecriture_lettre).distinct()
	listecontresignataire = Lettre.query.with_entities(Lettre.contresignataire_lettre).distinct()
	listelangue = Lettre.query.with_entities(Lettre.langue_lettre).distinct()
	listepronom = Lettre.query.with_entities(Lettre.pronom_personnel_employe_lettre).distinct()
	listecote = Lettre.query.with_entities(Lettre.cote_lettre).distinct()
	listestatut = Lettre.query.with_entities(Lettre.statut_lettre).distinct()
	listelien = Lettre.query.with_entities(Lettre.lien_image_lettre).distinct()


	#Une fois le formulaire envoyé, on passe en méthode http POST
	if request.method=="POST":

		# On applique la fonction ajout_lettre définie dans le fichier donnees.py
		status, donnees_lettre = Lettre.ajout_lettre(
		date=request.form.get("Date", None),
		lieu= request.form.get("Lieu", None),
		objet=request.form.get("Objet", None),
		contresignataire=request.form.get("Contresignataire", None),
		langue=request.form.get("Langue", None),
		pronom=request.form.get("Pronom", None),
		cote=request.form.get("Cote", None),
		statut=request.form.get("Statut", None),
		lien=request.form.get("Lien", None),
		institution=request.form.get("Institution", None),
		destinataire=request.form.get("Destinataire", None)
		)

		if status is True:
			flash("Ajout réussi", "success")
			return redirect(url_for("index_lettres"))

		else:
			flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees_lettre), "error")
			return render_template("pages/formulaire_lettre.html")


	return render_template("pages/formulaire_lettre.html", nom="Epistautograpy", listeobjetlettre=listeobjetlettre, listedatelettre=listedatelettre,
		listelieulettre=listelieulettre, listecontresignataire=listecontresignataire, listelangue=listelangue,
		listepronom=listepronom, listecote= listecote, listestatut=listestatut)


@app.route("/formulaire_destinataire", methods=["GET", "POST"])
def formulaire_destinataire():
	listetypedestinataire = Destinataire.query.with_entities(Destinataire.type_destinataire).distinct()
	listetitredestinataire = Destinataire.query.with_entities(Destinataire.titre_destinataire).distinct()
	listeidentitedestinataire = Destinataire.query.with_entities(Destinataire.identite_destinataire).distinct()
	listedatenaissance	= Destinataire.query.with_entities(Destinataire.date_naissance).distinct()
	listedatedeces	= Destinataire.query.with_entities(Destinataire.date_deces).distinct()
	listelienbio = Destinataire.query.with_entities(Destinataire.lien_infos_destinataire).distinct()

	#Une fois le formulaire envoyé, on passe en méthode http POST
	if request.method=="POST":

		## On applique la fonction ajout_destinataire définie dans le fichier donnees.py
		status, donnees_destinataire=Destinataire.ajout_destinataire(
		type_destinataire=request.form.get("Type_destinataire", None),
		titre=request.form.get("Titre_destinataire", None),
		identite=request.form.get("Identite_destinataire", None),
		date_naissance=request.form.get("Date_Naissance", None),
		date_deces=request.form.get("Date_Deces", None),
		lien_bio=request.form.get("Lien_Bio", None)
		)

		if status is True:
			flash("Ajout réussi", "success")
			return redirect(url_for("index_destinataires"))

		else:
			flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees_destinataire), "error")
			return render_template("pages/formulaire_destinataire.html")

	return render_template("pages/formulaire_destinataire.html", nom="Epistautograpy", listetypedestinataire=listetypedestinataire,
		listetitredestinataire=listetitredestinataire, listeidentitedestinataire=listeidentitedestinataire)



@app.route("/formulaire_institution", methods=["GET", "POST"])
def formulaire_institution():	
	listenominstitution = Institution_Conservation.query.with_entities(Institution_Conservation.nom_institution_conservation).distinct()
	listelatitude = Institution_Conservation.query.with_entities(Institution_Conservation.latitude_institution_conservation).distinct()
	listelongitude = Institution_Conservation.query.with_entities(Institution_Conservation.longitude_institution_conservation).distinct()

	#Une fois le formulaire envoyé, on passe en méthode http POST
	if request.method=="POST":

		# On applique la fonction ajout_institution définie dans le fichier donnees.py
		status, donnees_institution=Institution_Conservation.ajout_institution(
			nom=request.form.get("Nom", None),
			latitude=request.form.get("Latitude", None),
			longitude=request.form.get("Longitude", None)
			)

		if status is True:
			flash("Ajout réussi", "success")
			return redirect(url_for("index_institutions_conservations"))
		else:
			flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees_institution), "error")
			return render_template("pages/formulaire_institution.html")

	return render_template("pages/formulaire_institution.html", nom="Epistautograpy", listenominstitution=listenominstitution)


@app.route("/suppression_lettre", methods=["POST", "GET"])
def suppression_lettre():
	""" 
	Route pour supprimer une lettre dans la base
	:return : affichage du template supprimer_lettre.html ou redirection
	"""

	listenumerolettre = Lettre.query.with_entities(Lettre.id_lettre).distinct()

	if request.method == "POST":
		status = Lettre.supprimer_lettre(
            id_lettre=request.form.get("Lettre_a_supprimer", None)
        )

		if status is True:
			flash("Suppression réussie !", "success")
			return redirect("/index_lettres")
		else:
			flash("Echec de la suppression...", "danger")
			return redirect("/index_lettres")
	else:
		return render_template("pages/suppression_lettre.html", nom="Epistautograpy", listenumerolettre=listenumerolettre, lettre=lettre)


@app.route("/suppression_destinataire", methods=["POST", "GET"])
def suppression_destinataire():
	""" 
	Route pour supprimer un destintaire dans la base
	:return : affichage du template supprimer_destinataire.html ou redirection
	"""
	listedestinataire = Destinataire.query.with_entities(Destinataire.identite_destinataire).distinct()

	if request.method == "POST":
		statut = Destinataire.supprimer_destinataire(
			id_destinataire=request.form.get("Destinataire_a_supprimer", None)
		)

		if statut is True:
			flash("Suppression réussie !", "success")
			return redirect("/index_destinataires")
		else:
			flash("Echec de la suppression...", "danger")
			return redirect("/index_destinataires")
	else:
		return render_template("pages/suppression_destinataire.html", nom="Epistautograpy", listedestinataire=listedestinataire, destinataire=destinataire)


@app.route("/suppression_institution", methods=["POST", "GET"])
def suppression_institution():
	""" 
	Route pour supprimer une institution dans la base
	:return : affichage du template supprimer_institution.html ou redirection
	"""
	listeinstitution = Institution_Conservation.query.with_entities(Institution_Conservation.nom_institution_conservation).distinct()

	if request.method == "POST":
		statut = Institution_Conservation.supprimer_institution(
			id_institution_conservation=request.form.get("Institution_a_supprimer", None)
		)

		if statut is True:
			flash("Suppression réussie !", "success")
			return redirect("/index_institutions_conservations")
		else:
			flash("Echec de la suppression...", "danger")
			return redirect("/index_institutions_conservations")
	else:
		return render_template("pages/suppression_institution.html", nom="Epistautograpy", listeinstitution=listeinstitution, institution_conservation=institution)


@app.route("/recherche", methods=["GET","POST"])
def recherche():

	# RECUPERATION DES PARAMETRES DE RECHERCHE INDIQUES PAR L'UTILISATEUR
	# On utilise .get ici pour partager les résultats de recherche de manière simple
	#  et qui nous permet d'éviter un if long en mettant les deux conditions entre parenthèses
	# On stocke les mots clefs recherchés par l'utilisateur présents dans les arguments de l'URL
	keyword = request.args.get("keyword", None)

	# GESTION DE LA VALEUR DE PAGE COURANTE
	page = request.args.get("page", 1)
	#Association d'une page de résultat à un numéro de page ; s'il n'y a pas de résultats
	#retour automatique à la première page de résultats.
	if isinstance(page, str) and page.isdigit():
		page = int(page)
	else:
		page = 1

	# On crée une liste vide de résultat (qui restera vide par défaut
	#   si on n'a pas de mot clé)
	resultats = []

	# On fait de même pour le titre de la page
	titre = "Recherche"
	if keyword :
		resultats = Lettre.query.filter(or_(
			Lettre.id_lettre.like("%{}%".format(keyword)),
			Lettre.objet_lettre.like("%{}%".format(keyword)),
			Lettre.date_envoie_lettre.like("%{}%".format(keyword)),
			Lettre.lieu_ecriture_lettre.like("%{}%".format(keyword)),
			Lettre.contresignataire_lettre.like("%{}%".format(keyword)),
			Lettre.correspondance.any(Destinataire.type_destinataire.like("%{}%".format(keyword))),
			Lettre.correspondance.any(Destinataire.titre_destinataire.like("%{}%".format(keyword))),
			Lettre.correspondance.any(Destinataire.identite_destinataire.like("%{}%".format(keyword))))

			).paginate(page=page, per_page=LETTRES_PAR_PAGE)

		titre = "Résultat pour la recherche `" + keyword + "`"
	else:
		titre = "Résultat de la recherche"
	
	return render_template("pages/recherche.html", nom="Epistautograpy", titre=titre, keyword=keyword, resultats=resultats)


@app.route('/rechercheavancee', methods=["GET","POST"])
def rechercheavancee ():
	# GESTION DE LA VALEUR DE PAGE COURANTE
	page = request.args.get("page", 1)

	if isinstance(page, str) and page.isdigit():
		page = int(page)
	else:
		page = 1

	#Conditions si la méthode http "POST" est utilisée. Contraitement à la méthode "GET" 
	#qui inscrit les données dans l'URL, la méthode "POST" envoie un en-tête et un corps de message
	#au serveur avec les données entrées dans le champ de formulaire. Les données n'apparaissent donc pas dans l'URL.
	if request.method == "POST":

	# On crée une liste vide de résultat (qui restera vide par défaut
	# si on n'a pas de mot clé)
		resultats = []
		titre = "Recherche"
		keyword = request.form.get("keyword", None)

	# RECUPERATION DES PARAMETRES DE RECHERCHE INDIQUES PAR L'UTILISATEUR
	# On utilise .get ici pour partager les résultats de recherche de manière simple
	#  et qui nous permet d'éviter un if long en mettant les deux conditions entre parenthèses
	# On stocke les mots clefs recherchés par l'utilisateur présents dans les arguments de l'URL
	
		#Lettre
		numero=request.form.get("Numero_lettre", None)
		objet=request.form.get("Objet_lettre", None)
		contresignataire=request.form.get("Contresignataire_lettre", None)
		date=request.form.get("Date_lettre", None)
		lieu= request.form.get("Lieu_lettre", None)
		langue=request.form.get("Langue_lettre", None)
		pronom=request.form.get("Pronom_lettre", None)
		cote=request.form.get("Cote_lettre", None)
		statut=request.form.get("Statut_lettre", None)
		#Destinataire
		type_destinataire=request.form.get("Type_destinataire", None)
		titre_destinataire=request.form.get("Titre_destinataire", None)
		identite=request.form.get("Identite_destinataire", None)
		#Institution
		nom_institution=request.form.get("Nom_institution", None)

		if numero :
			resultats=Lettre.query.filter(Lettre.id_lettre.like("%{}%".format(numero)))
		if objet:
			resultats=Lettre.query.filter(Lettre.objet_lettre.like("%{}%".format(objet)))
		if contresignataire:
			resultats=Lettre.query.filter(Lettre.contresignataire_lettre.like("%{}%".format(contresignataire)))
		if date:
			resultats=Lettre.query.filter(Lettre.date_envoie_lettre.like("%{}%".format(date)))
		if lieu:
			resultats=Lettre.query.filter(Lettre.lieu_ecriture_lettre.like("%{}%".format(lieu)))
		if langue:
			resultats=Lettre.query.filter(Lettre.langue_lettre.like("%{}%".format(langue)))
		if pronom:
			resultats=Lettre.query.filter(Lettre.pronom_personnel_employe_lettre.like("%{}%".format(pronom)))
		if cote:
			resultats=Lettre.query.filter(Lettre.cote_lettre.like("%{}%".format(cote)))
		if statut:
			resultats=Lettre.query.filter(Lettre.statut_lettre.like("%{}%".format(statut)))
		if type_destinataire:
			resultats=Lettre.query.filter(Lettre.correspondance.any(Destinataire.type_destinataire.like("%{}%".format(type_destinataire))))
		if titre_destinataire:
			resultats=Lettre.query.filter(Lettre.correspondance.any(Destinataire.titre_destinataire.like("%{}%".format(titre_destinatatire))))
		if identite:
			resultats=Lettre.query.filter((Lettre.correspondance.any(Destinataire.identite_destinataire.like("%{}%".format(identite)))))
		if nom_institution:
			resultats=Institution_Conservation.query.filter((Institution_Conservation.nom_institution_conservation.like("%{}%".format(nom_institution))))

		resultats = resultats.paginate(page=page)

		return render_template("pages/recherche.html", titre=titre, keyword=keyword, resultats=resultats, page=page)

	return render_template("pages/rechercheavancee.html", nom="Epistautograpy")


@app.route("/register", methods=["GET", "POST"])
#Route appelant les différentes fonctions de l'identification et de la création
#de comptes séparées dans utilisateurs.py
def inscription():
	""" Route gérant les inscriptions
	"""
# Si on est en POST, cela veut dire que le formulaire a été envoyé
	if request.method == "POST":
		statut, donnees = User.creer(
			login=request.form.get("login", None),
			email=request.form.get("email", None),
			nom=request.form.get("nom", None),
			motdepasse=request.form.get("motdepasse", None)
		)
		if statut is True:
			flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
			return redirect("/")
		else:
			flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
			return render_template("pages/inscription.html")
	else:
		return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():   
	if current_user.is_authenticated is True:
		flash("Vous êtes déjà connecté-e", "info")
		return redirect(url_for("accueil"))
# Si on est en POST, cela veut dire que le formulaire a été envoyé
	if request.method == "POST":
		utilisateur = User.identification(
			login=request.form.get("login", None),
			motdepasse=request.form.get("motdepasse", None)
		)
		if utilisateur:
			flash("Connexion effectuée", "success")
			login_user(utilisateur)
			return redirect(url_for("accueil"))
		else:
			flash("Les identifiants n'ont pas été reconnus", "error")

	return render_template("pages/connexion.html")


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
	if current_user.is_authenticated is True:
		logout_user()
	flash("Vous êtes déconnecté-e", "info")
	return redirect("/")


#Chemin vers la page "Conditions générales d'utilisation"

@app.route('/cgu')
def cgu():
	return render_template("pages/cgu.html", nom="Epistautograpy")


#Chemin vers page "à propos"

@app.route('/about')
def about():
	return render_template("pages/apropos.html", nom="Epistautograpy")

