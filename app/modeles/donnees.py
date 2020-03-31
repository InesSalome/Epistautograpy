#!/usr/bin/python
# -*- coding: utf-8 -*-
#Import d'informations si besoin depuis le fichier concerné.
from .. app import db
from flask import url_for
import datetime
from sqlalchemy import update
from sqlalchemy import Column, Integer, String


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
	correspondance = db.relationship("Lettre", secondary="correspondance", backref="destinataire", lazy="dynamic")

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
	correspondance = db.relationship("Destinataire", secondary="correspondance", backref="lettre", lazy="dynamic")

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