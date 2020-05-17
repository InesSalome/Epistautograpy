#!/usr/bin/python
# -*- coding: utf-8 -*-
#Import d'informations si besoin depuis le fichier concerné.
from .. app import db
from flask import url_for
import datetime
from sqlalchemy import create_engine, Column, Integer, String,update


#Tables pour faire les jointures

Correspondance = db.Table('correspondance',
	db.Column('destinataire_id', db.Integer, db.ForeignKey('destinataire.id_destinataire'), primary_key=True),
	db.Column('lettre_id', db.Integer, db.ForeignKey('lettre.id_lettre'), primary_key=True)
	)

Authorship = db.Table('authorship',
	db.Column('id_authorship', db.Integer, nullable=True, autoincrement=True, primary_key=True),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id_user')),
	db.Column('lettre_id', db.Integer, db.ForeignKey('lettre.id_lettre')),
	db.Column('date_authorship',db.DateTime, default=datetime.datetime.utcnow)
	)

#Tables de relation

class Authorship(db.Model):
	__tablename__ = "authorship"
	__table_args__ = {'extend_existing': True}
	id_authorship = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
	lettre_id = db.Column(db.Integer, db.ForeignKey('lettre.id_lettre'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'))
	date_authorship = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	user = db.relationship("User", back_populates="authorships")

	def author_to_json(self):
		return {
			"author": self.user.to_jsonapi_dict(),
			"on": self.authorship_date
		}


class Correspondance(db.Model):
	__tablename__= "correspondance"
	__table_args__ = {'extend_existing': True}
	destinataire_id = db.Column(db.Integer, db.ForeignKey('destinataire.id_destinataire'), primary_key=True)
	lettre_id = db.Column(db.Integer, db.ForeignKey('lettre.id_lettre'), primary_key=True)

	def ajout_correspondance(destinataire_id,lettre_id):   
		"""
		Retourne un couple d'identifiants pour définir une nouvelle relation lorqu'une nouvelle correpondance est rentrée via le formulaire
		:param destinataire_id; Id du destinataire
		:type destinataire_id: integer
		:param lettre_id; Id de la lettre
		:type lettre_id: integer
		:return: tuple d'identifiants
		:rtype: integers
		"""   

		destinataire_id=ajout_destinataire
		lettre_id=ajout_lettre

#Création de notre modèle

class Destinataire(db.Model) :
	__tablename__ = "destinataire"
	id_destinataire  = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	type_destinataire = db.Column(db.String(45))
	titre_destinataire = db.Column(db.Text)
	identite_destinataire = db.Column(db.Text)
	date_naissance = db.Column(db.Text)
	date_deces = db.Column(db.Text)
	lien_infos_destinataire = db.Column(db.Text)
	correspondance = db.relationship("Lettre", secondary="correspondance", backref="destinataire", lazy="dynamic", cascade='all, delete, delete-orphan', single_parent="True")

	def get_id(self):
		"""
		Retourne l'id de l'objet actuellement utilisé
		:return: Id du destinataire
		:rtype: int
		"""				
		return(self.id_destinataire)

	@staticmethod
	def ajout_destinataire(type_destinataire, titre, identite, date_naissance, date_deces, lien_bio):
		"""
		Rajout de données via le formulaire.
		S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur.
		Sinon, elle renvoie True et les données sont enregistrées dans la base.
		:param type: type de destinataire, institution ou noblesse
		:type type: string
		:param titre: titre assigné à un destinataire issu de la noblesse
		:type titre: string
		:param identite: nom du destinataire ou de l'institution à qui s'adresse la lettre
		:type identite: string
		"""

		# Définition des paramètres obligatoires : s'ils manquent, cela crée une liste d'erreurs
		erreurs = []
		if not type_destinataire:
			erreurs.append("Le champ type de destinataire est vide")
		if not identite:
			erreurs.append("Le champ identite est vide")
		if not type_destinataire=="institution" or type_destinataire=="noblesse":
			erreurs.append("Le champ identite ne correspond pas aux données attendues : institution ou noblesse.")
		#On vérifie que la longueur des caractères des dates ne dépasse pas la limite de 10 (format AAAA-MM-JJ)
		if date_naissance==True and date_deces==True:
			if not len(date_naissance)==10 and len(date_deces)==10:
				erreurs.append("Les dates doivent être écrites au format suivant : AAAA-MM-JJ")   
		# On vérifie que le/la destinataire n'a pas déjà été enregistré(e)
		if identite==Destinataire.identite_destinataire:
			erreurs.append("Le/La destinataire a déjà été enregistré(e) dans la base de données")

		# Si on a au moins une erreur
		if len(erreurs) > 0:
			return False, erreurs

		# On crée une nouvelle lettre dans la table Destinataire
		new_destinataire = Destinataire(
			type_destinataire=type_destinataire,
			titre_destinataire=titre,
			identite_destinataire=identite,
			date_naissance=date_naissance,
			date_deces=date_deces,
			lien_infos_destinataire=lien_bio
		)

		try:
			# On l'ajoute au transport vers la base de données
			db.session.add(new_destinataire)
			# On envoie le paquet
			db.session.commit()
			return( True, new_destinataire)

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
			return False, [str(erreur)]

	@staticmethod
	def supprimer_destinataire(id_destinataire):
		"""
		Fonction qui supprime un destinataire
		:param id_destinataire: id du destinataire
		:return: Booléen
		"""
		destinataire_a_supprimer = Destinataire.query.get(id_destinataire)
	# récupération d'une collection dans la BDD

		try:
			db.session.delete(delete_collection)
		# suppression de la collection de la BDD
			db.session.commit()
			return True

		except Exception as erreur:
			return False, [str(erreur)]

	def to_jsonapi_dict(self):
		"""
		It ressembles a little JSON API format but it is not completely compatible

		:return:
		"""
		return {
			"type": "destinataire",
			"id": self.id_destinataire,
			"attributes": {
				"type": self.type_destinataire,
				"titre": self.titre_destinataire,
				"identite": self.identite_destinataire,
				"naissance": self.date_naissance,
				"deces": self.date_deces,
				"lien_infos_destinataire": self.lien_infos_destinataire
			},
			"links": {
				"self": url_for("destinataire", id_destinataire=self.id_destinataire, _external=True),
				"json": url_for("api_destinataires_single", id_destinataire=self.id_destinataire, _external=True)
			},
			"relationships": {
				 "editions": [
					 author.author_to_json()
					 for author in self.authorships
				 ]
			}
		}

class Institution_Conservation(db.Model) :
	__tablename__ = "institution_conservation"
	id_institution_conservation = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	nom_institution_conservation = db.Column(db.String(45))
	latitude_institution_conservation = db.Column(db.Float)
	longitude_institution_conservation = db.Column(db.Float)

	def get_id(self):
		"""
		Retourne l'id de l'objet actuellement utilisé
		:return: Id de l'institution de conservation
		:rtype: int
		"""
		return(self.id_institution_conservation)

	@staticmethod
	def ajout_institution(nom, latitude, longitude):
		"""
		Rajout de données via le formulaire.
		S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur.
		Sinon, elle renvoie True et les données sont enregistrées dans la base.
		:param nom: nom de l'institution
		:type nom: string
		"""

		# Définition des paramètres obligatoires : s'ils manquent, cela crée une liste d'erreurs
		erreurs = []
		if not nom:
			erreurs.append("Le champ nom est vide")
		# On vérifie que l'institution n'a pas déjà été enregistrée
		if nom==Institution_Conservation.nom_institution_conservation:
			erreurs.append("L'institution a déjà été enregistrée dans la base de données")

		# Si on a au moins une erreur
		if len(erreurs) > 0:
			return False, erreurs

		# On crée une nouvelle lettre dans la base Lettre
		new_institution = Institution_Conservation(
			nom_institution_conservation=nom,
			latitude_institution_conservation=latitude,
			longitude_institution_conservation=longitude
		)

		try:
			# On l'ajoute au transport vers la base de données
			db.session.add(new_institution)
			# On envoie le paquet
			db.session.commit()
			return( True, new_institution)

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
			return False, [str(erreur)]


	@staticmethod
	def supprimer_institution(id_institution_conservation):
		"""
		Fonction qui supprime une institution
		:param id_institution: id de l'institution
		:return: Booléen
		"""
		institution_a_supprimer = Institution_Conservation.query.get(id_institution_conservation)
	# récupération d'une collection dans la BDD

		try:
			db.session.delete(delete_collection)
		# suppression de la collection de la BDD
			db.session.commit()
			return True

		except Exception as erreur:
			return False, [str(erreur)]

	def to_jsonapi_dict(self):
		"""
		It ressembles a little JSON API format but it is not completely compatible

		:return:
		"""
		return {
			"type": "institution_conservation",
			"id": self.id_institution_conservation,
			"attributes": {
				"nom": self.nom_institution_conservation,
				"latitude": self.latitude_institution_conservation,
				"longitude": self.longitude_institution_conservation
			},
			"links": {
				"self": url_for("institution_conservation", id_institution_conservation=self.id_institution_conservation, _external=True),
				"json": url_for("api_institutions_single", id_institution_conservation=self.id_institution_conservation, _external=True)
			},
			"relationships": {
				 "editions": [
					 author.author_to_json()
					 for author in self.authorships
				 ]
			}
		}

class Lettre(db.Model) :
	__tablename__ = "lettre"
	id_lettre = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	date_envoie_lettre = db.Column(db.Text)
	lieu_ecriture_lettre = db.Column(db.String(45))
	objet_lettre = db.Column(db.Text)
	contresignataire_lettre = db.Column(db.String(45))
	langue_lettre = db.Column(db.String(45))
	pronom_personnel_employe_lettre = db.Column(db.String(45))
	cote_lettre = db.Column(db.String(45))
	statut_lettre = db.Column(db.String(45))
	institution_id = db.Column(db.Integer, db.ForeignKey('institution_conservation.id_institution_conservation'))
	lien_image_lettre = db.Column(db.Text)
	authorships = db.relationship("User", secondary="authorship", backref="lettre", lazy="dynamic")
	correspondance = db.relationship("Destinataire", secondary="correspondance", backref="lettre", lazy="dynamic", cascade='all, delete, delete-orphan', single_parent="True")

	def get_id(self):
		"""
		Retourne l'id de l'objet actuellement utilisé
		:return: Id de la lettre
		:rtype: int
		"""
		return(self.id_lettre)

	@staticmethod
	def ajout_lettre(objet, contresignataire, date, lieu, langue, pronom, cote, statut, lien, institution, destinataire):
		"""
		Rajout de données via le formulaire.
		Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur.
		Sinon, elle renvoie True et les données sont enregistrées dans la base.
		:param objet: Objet de la lettre
		:type objet: string
		:param contresignataire: Nom du contresigataire de la lettre
		:type contresignataire: string
		:param date: date d'envoie de la lettre
		:type date: string
		:param lieu: lieu d'envoie de la lettre
		:type lieu: string
		:param langue: langue d'écriture de la lettre
		:type langue: string
		:param pronom: pronom personnel employé dans la lettre
		:type pronom: string
		:param cote: cote de la lettre
		:type cote: string
		:param statut: statut de la lettre, originale ou copie
		:type statut: string
		:param lien: url vers la lettre numérisée
		:type lien: string
		:param institution_id: clé étrangère de l'institution de conservation
		:type institution_id: integer
		"""

		# Définition des paramètres obligatoires : s'ils manquent, cela crée une liste d'erreurs
		erreurs = []
		if not contresignataire:
			erreurs.append("Le champ contresignataire est vide")
		if not date:
			erreurs.append("Le champ date est vide")
		if not lieu:
			erreurs.append("Le champ lieu est vide")
		if not cote:
			erreurs.append("Le champ cote est vide")
		if not statut:
			erreurs.append("Le champ statut est vide")
		#if statut!="Orig." or statut!="Copie":
			#erreurs.append("Le champ statut ne correspond pas aux données attendues : Orig. ou Copie")
		# On vérifie que la lettre n'a pas déjà été enregistrée
		if date==Lettre.date_envoie_lettre and cote==Lettre.cote_lettre:
			erreurs.append("La lettre a déjà été renseignée dans notre base de données")

		# Si on a au moins une erreur
		if len(erreurs) > 0:
			return False, erreurs

		#On vérifie que l'instituion et le destinataire ont déjà été enregistrés dans la base
		#En faisant les liens adéquats entre la lettre, son institution de conservation et son/sa destinataire
		if institution == True :
			if institution == Institution_Conservation.query.filter(Institution_Conservation.nom_institution_conservation):
				Lettre.institution_id = Institution_Conservation.query.get(id_institution_conservation)
			else:
				return False,[str("L'institution de conservation n'a pas été enregistrée préalablement")]
		if destinataire == True :
			if destinataire == Destinataire.query.filter(Destinataire.identite_destinataire):
				Lettre.correspondance = Lettre.query.get(db.and_(Lettre.id_lettre==Correspondance.lettre_id, Correspondance.destinataire_id==Destinataire.id_destinataire))
			else:
				return False, [str("Le ou la destinataire n'a pas été enregistré préalablement")]

		# On crée une nouvelle lettre dans la base Lettre
		new_lettre = Lettre(
			date_envoie_lettre=date,
			lieu_ecriture_lettre=lieu,
			objet_lettre=objet,
			contresignataire_lettre=contresignataire,
			langue_lettre=langue,
			pronom_personnel_employe_lettre=pronom,
			cote_lettre=cote,
			statut_lettre=statut,
			lien_image_lettre=lien,
			institution_id=institution,
			correspondance=destinataire
		)

		try:
			# On l'ajoute au transport vers la base de données
			db.session.add(new_lettre)
			# On envoie le paquet
			db.session.commit()
			return( True, new_lettre)

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
			return False, [str(erreur)]

	@staticmethod
	def supprimer_lettre(id_lettre):
		"""
		Fonction qui supprime une lettre
		:param id_lettre: id de la lettre
		:return: Booléen
		"""
		lettre_a_supprimer = Lettre.query.get(id_lettre)

		try:
			db.session.delete(delete_collection)
		# suppression de la collection de la BDD
			db.session.commit()
			return True

		except Exception as erreur:
			return False, [str(erreur)]


	def to_jsonapi_dict(self):
		"""
		It ressembles a little JSON API format but it is not completely compatible

		:return:
		"""
		return {
			"type": "lettre",
			"id": self.id_lettre,
			"attributes": {
				"date": self.date_envoie_lettre,
				"lieu": self.lieu_ecriture_lettre,
				"objet": self.objet_lettre,
				"contresignataire": self.contresignataire_lettre,
				"langue": self.langue_lettre,
				"pronom": self.pronom_personnel_employe_lettre,
				"cote": self.cote_lettre,
				"statut": self.statut_lettre,
				"lien_image_lettre": self.lien_image_lettre
			},
			"links": {
				"self": url_for("lettre", id_lettre=self.id_lettre, _external=True),
				"json": url_for("api_lettres_single", id_lettre=self.id_lettre, _external=True)
			},
			"relationships": {
				 "editions": [
					 author.author_to_json()
					 for author in self.authorships
				 ]
			}
		}

class Image_Numerisee(db.Model):
	__tablename__ = "image_numerisee"
	id_image_numerisee = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	url_image_numerisee = db.Column(db.Text)
	reference_bibliographique_image_numerisee = db.Column(db.Text)
	lettre_id = db.Column(db.Integer, db.ForeignKey('lettre.id_lettre'))

	def get_id(self):
		"""
		Retourne l'id de l'objet actuellement utilisé
		:return: Id de l'image numérisée
		:rtype: int
		"""
		return(self.id_image_numerisee)

	def to_jsonapi_dict(self):
		"""
		It ressembles a little JSON API format but it is not completely compatible

		:return:
		"""
		return {
			"type": "image_numerisee",
			"id": self.id_image_numerisee,
			"attributes": {
				"lien": self.url_image_numerisee,
				"reference": self.reference_bibliographique_image_numerisee
			},
			"links": {
				"self": url_for("image_numerisee", id_image_numerisee=self.id_image_numerisee, _external=True),
				"json": url_for("api_images_single", id_image_numerisee=self.id_image_numerisee, _external=True)
			},
			"relationships": {
				 "editions": [
					 author.author_to_json()
					 for author in self.authorships
				 ]
			}
		}