#Import d'informations si besoin depuis le fichier concerné.
from .. app import db
#Import de url_for pour construire des liens internes à l'application
from flask import url_for
#Module datetime pour pouvoir spécfier un format de date
import datetime
#Import de fonctions pour faire fonctionner la base de données
from sqlalchemy import create_engine, Column, Integer, String, update

#Tables de relation

class Authorship(db.Model):
	__tablename__ = "authorship"
	__table_args__ = {'extend_existing': True}
	id_authorship = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
	lettre_id = db.Column(db.Integer, db.ForeignKey('lettre.id_lettre'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'))
	date_authorship = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	user = db.relationship("User", back_populates="authorships")
	lettre = db.relationship("Lettre", back_populates="authorships_lettre")

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
	correspondance = db.relationship("Lettre", secondary="correspondance", backref="destinataire", lazy="dynamic", cascade='all, delete, delete-orphan', single_parent="True")

	def get_id(self):
		"""
		Retourne l'id de l'objet actuellement utilisé
		:returns: Id du destinataire
		:rtype: int
		"""				
		return(self.id_destinataire)

	@staticmethod
	def ajout_destinataire(type_destinataire, titre, identite, date_naissance, date_deces, lien_bio):
		"""
		Rajout de données via le formulaire.
		S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur.
		Sinon, elle renvoie True et les données sont enregistrées dans la base.
		:param type_destinataire: type de destinataire, institution ou noblesse
		:type type_destinataire: str
		:param titre: titre assigné à un destinataire issu de la noblesse
		:type titre: str
		:param identite: nom du destinataire ou de l'institution à qui s'adresse la lettre
		:type identite: str
		:param date_naissance: date de naissance du destinataire
		:type date_naissance: str
		:param date_deces: date de deces du destinataire
		:type date_deces: str
		:param lien_bio: URL vers une page de biographie
		:type lien_bio: str	
		"""

		# Définition des paramètres obligatoires : s'ils manquent, cela crée une liste d'erreurs
		erreurs = []
		if not type_destinataire:
			erreurs.append("Le champ type de destinataire est vide")
		if not identite:
			erreurs.append("Le champ identite est vide")
		if type_destinataire!="institution" or type_destinataire!="noblesse":
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
			lien_infos_destinataire=lien_bio,
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
	def miseajour_destinataire(id_destinataire, type_destinataire, titre, identite, date_naissance, date_deces, lien_bio):
		"""
		Fonction qui permet de modifier les données d'un destinataire dans la base de données
		:param id_destinataire: id du destinataire
		:type id_destinataire: int
		:param type_destinataire : institution ou noblesse
		:type type_destinataire : str
		:param titre: titre de noblesse
		:type titre: str
		:param identite: nom de la personne ou de l'institution
		:type identite: str
		:param date_naissance: date de naissance de la personne
		:type date_naissance: str
		:param date_deces: date de décès de la personne
		:type date_deces: str
		:param lien_bio: URL vers une page de biographie
		:type lien_bio: str
		:returns: Ajout de données dans la base ou refus en cas d'erreurs
		:rtype: Booléen
		"""
		errors=[]
		if not type_destinataire:
			errors.append("Le champ Type de destinataire est vide.")
		#if  type_destinataire!="noblesse" or  type_destinataire!="institution":
			#errors.append("Le champ Type de destinataire ne correspond pas aux données attendues : institution ou noblesse")
		if type_destinataire=="noblesse":
			if not titre:
				errors.append("Le champ Titre du destinataire est vide.")

		if len(errors) > 0:
			return False, errors

		# récupération du destinataire dans la base de données
		miseajour_destinataire = Destinataire.query.filter(Destinataire.id_destinataire)
		
		# vérification qu'au moins un champ est modifié
		if  type_destinataire == Destinataire.type_destinataire\
			and  titre == Destinataire.titre_destinataire \
			and  identite == Destinataire.identite_destinataire \
			and  date_naissance == Destinataire.date_naissance \
			and  date_deces == Destinataire.date_deces \
			and  lien_bio == Destinataire.lien_infos_destinataire :
			errors.append("Aucune modification n'a été réalisée")

		if len(errors) > 0:
			return False, errors
		
		else:
			# mise à jour des données
			 type_destinataire == Destinataire.type_destinataire
			 titre == Destinataire.titre_destinataire 
			 identite == Destinataire.identite_destinataire 
			 date_naissance == Destinataire.date_naissance 
			 date_deces == Destinataire.date_deces
			 lien_bio == Destinataire.lien_infos_destinataire

		try:
			# On les ajoute au transport vers la base de données
			db.session.add(miseajour_destinataire)
			# On envoie le paquet
			db.session.commit()
			return True, miseajour_destinataire

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
			return False, [str(erreur)]

	@staticmethod
	def supprimer_destinataire(nom_destinataire):
		"""
		Fonction qui supprime un destinataire
		:param nom_destinataire: identité du destinataire
		:type nom_destinataire: str
		:returns: Suppression des données ou refus en cas d'erreurs
		:rtype: Booléen
		"""
		# récupération du destinataire dans la base de données
		nom_destinataire = Destinataire.query.filter(Destinataire.identite_destinataire)
	

		try:
			#Suppression du destinataire dans la base de données
			db.session.delete(supprimer_destinataire)
			db.session.commit()
			return True

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
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
		:returns: Id de l'institution de conservation
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
		:type nom: str
		:param latitude: latitude de l'institution
		:type latitude: float
		:param longitude: longitude de l'institution
		:type longitude: float
		:returns: Ajout de données dans la base ou refus en cas d'erreurs
		:rtype: Booléen
		"""

		# Définition des paramètres obligatoires : s'ils manquent, cela crée une liste d'erreurs
		erreurs = []
		if not nom:
			erreurs.append("Le champ nom est vide.")
		if not latitude:
			erreurs.append("Le champ latitude est vide.")
		if not longitude:
			erreurs.append("Le champ longitude est vide.")
		# On vérifie que l'institution n'a pas déjà été enregistrée
		if nom==Institution_Conservation.nom_institution_conservation:
			erreurs.append("L'institution a déjà été enregistrée dans la base de données.")

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
			return(True, new_institution)

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
			return False, [str(erreur)]

	@staticmethod
	def miseajour_institution(id_institution_conservation, nom, latitude, longitude):
		"""
		Fonction qui permet de modifier les données d'une institution dans la base de données
		:param id_institution_conservation: id de l'institution
		:typ id_institution_conservation: int
		:param nom: nom de l'institution
		:type nom: str
		:param latitude: latitude de l'emplacement de l'institution
		:type latitude: float
		:param longitude:longitude de l'emplacement de l'institution
		:type longitude: float
		:returns: Ajout de données dans la base ou refus en cas d'erreurs
		:rtype: Booléen
		"""
		errors=[]
		if not nom:
			errors.append("Le champ Nom de l'institution est vide.")
		
		if len(errors) > 0:
			return False, errors

		# récupération de l'institution dans la base de données
		miseajour_institution = Institution_Conservation.query.filter(Institution_Conservation.id_institution_conservation)
		
		# vérification qu'au moins un champ est modifié
		if  nom == Institution_Conservation.nom_institution_conservation \
			and  latitude == Institution_Conservation.latitude_institution_conservation \
			and  longitude == Institution_Conservation.longitude_institution_conservation :
			errors.append("Aucune modification n'a été réalisée")

		if len(errors) > 0:
			return False, errors
		
		else:
			#Mise à jour des données
			 nom == Institution_Conservation.nom_institution_conservation 
			 latitude ==  Institution_Conservation.latitude_institution_conservation
			 longitude == Institution_Conservation.longitude_institution_conservation


		try:
			# On les ajoute au transport vers la base de données
			db.session.add(miseajour_institution)
			# On envoie le paquet
			db.session.commit()
			return True, miseajour_institution

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
			return False, [str(erreur)]

	@staticmethod
	def supprimer_institution(nom_institution_conservation):
		"""
		Fonction qui supprime une institution
		:param nom_institution_conservation: nom de l'institution
		:type nom_institution_conservation: str
		:returns: Suppression des données ou refus en cas d'erreurs
		:rtype: Booléen
		"""

		# récupération d'une institution dans la base de données
		nom_institution_conservation = Institution_Conservation.query.filter(Institution_Conservation.nom_institution_conservation)

		try:
			#Suppression de l'institution dans la base de données
			db.session.delete(supprimer_institution)
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
	authorships_lettre = db.relationship("Authorship", back_populates="lettre")
	correspondance = db.relationship("Destinataire", secondary="correspondance", backref="lettre", lazy="dynamic", cascade="all, delete, delete-orphan", single_parent="True")

	def get_id(self):
		"""
		Retourne l'id de l'objet actuellement utilisé
		:return: Id de la lettre
		:rtype: int
		"""
		return(self.id_lettre)

	@staticmethod
	def ajout_lettre(objet, contresignataire, date, lieu, langue, pronom, cote, statut, lien):
		"""
		Rajout de données via le formulaire.
		S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur.
		Sinon, elle renvoie True et les données sont enregistrées dans la base.
		:param objet: Objet de la lettre
		:type objet: str
		:param contresignataire: Nom du contresigataire de la lettre
		:type contresignataire: str
		:param date: date d'envoie de la lettre
		:type date: str
		:param lieu: lieu d'envoie de la lettre
		:type lieu: str
		:param langue: langue d'écriture de la lettre
		:type langue: str
		:param pronom: pronom personnel employé dans la lettre
		:type pronom: str
		:param cote: cote de la lettre
		:type cote: str
		:param statut: statut de la lettre, originale ou copie
		:type statut: str
		:param lien: url vers la lettre numérisée
		:type lien: str
		:param institution_id: clé étrangère de l'institution de conservation
		:type institution_id: int
		:param destinataire: tuple regroupant les id de la lettre et du destianataire qui sont liés par une correspondance
		:type destinataire: int
		:returns: Ajout de données dans la base ou refus en cas d'erreurs
		:rtype: Booléen
		"""

		# Définition des paramètres obligatoires : s'ils manquent, cela crée une liste d'erreurs
		erreurs = []
		if not contresignataire:
			erreurs.append("Le champ contresignataire est vide.")
		if not date:
			erreurs.append("Le champ date est vide.")
		if not lieu:
			erreurs.append("Le champ lieu est vide.")
		if not cote:
			erreurs.append("Le champ cote est vide.")
		if not statut:
			erreurs.append("Le champ statut est vide.")
		if statut!="Orig." or statut!="Copie":
			erreurs.append("Le champ statut ne correspond pas aux données attendues : Orig. ou Copie.")
		#On vérifie que la lettre n'a pas déjà été enregistrée
		if date==Lettre.date_envoie_lettre and cote==Lettre.cote_lettre:
			erreurs.append("La lettre a déjà été renseignée dans notre base de données.")

		# Si on a au moins une erreur
		if len(erreurs) > 0:
			return False, erreurs

		#On vérifie que l'instituion et le destinataire ont déjà été enregistrés dans la base
		#En faisant les liens adéquats entre la lettre, son institution de conservation et son/sa destinataire
		if institution == True :
			if institution == Institution_Conservation.query.filter(Institution_Conservation.nom_institution_conservation):
				Lettre.institution_id = Institution_Conservation.query.get(id_institution_conservation)
			else:
				return False,[str("L'institution de conservation n'a pas été enregistrée préalablement.")]
		if destinataire == True :
			if destinataire == Destinataire.query.filter(Destinataire.identite_destinataire):
				Lettre.correspondance = Lettre.query.get(db.and_(Lettre.id_lettre==Correspondance.lettre_id, Correspondance.destinataire_id==Destinataire.id_destinataire))
			else:
				return False, [str("Le ou la destinataire n'a pas été enregistré préalablement.")]

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
			lien_image_lettre=lien
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
	def miseajour_lettre(id_lettre, date, lieu, objet, contresignataire, langue, pronom, cote, statut, lien_lettre):
		"""
		Fonction qui permet de modifier les données d'une lettre dans la base de données
		:param id_lettre: id de la lettre
		:type id_lettre: int
		:param date: date d'envoie de la lettre
		:type date: str
		:param lieu: lieu d'envoie de la lettre
		:type lieu: str
		:param objet: objet de la lettre
		:type objet: str
		:param contresignataire: contresignataire de la lettre
		:type contresignataire: str
		:param langue: langue de la lettre
		:type langue: str
		:param pronom: pronom personnel employé dans la lettre
		:type pronom: str
		:param cote: cote de la lettre
		:type cote: str
		:param statut: statut de la lettre
		:type statut: str
		:param lien_lettre: lien vers la lettre numérisée
		:type lien_lettre: str
		:returns: Ajout de données dans la base ou refus en cas d'erreurs
		:rtype: Booléen
		"""

		# Définition des paramètres obligatoires : s'ils manquent, cela crée une liste d'erreurs
		errors=[]
		if not date:
			errors.append("Le champ Date d'envoie de la lettre est vide.")
		if not contresignataire:
			errors.append("Le champ Nom du contresignataire est vide.")
		if not cote:
			errors.append("Le champ Cote est vide.")
		
		if len(errors) > 0:
			return False, errors

		# récupération de la lettre dans la base de données
		miseajour_lettre = Lettre.query.filter(Lettre.id_lettre)
		
		# vérification qu'au moins un champ est modifié
		if  date == Lettre.date_envoie_lettre \
			and  lieu == Lettre.lieu_ecriture_lettre \
			and  objet == Lettre.objet_lettre \
			and  contresignataire == Lettre.contresignataire_lettre \
			and  langue == Lettre.langue_lettre \
			and  pronom == Lettre.pronom_personnel_employe_lettre \
			and  cote == Lettre.cote_lettre \
			and  statut == Lettre.statut_lettre \
			and  lien_lettre == Lettre.lien_image_lettre :

			errors.append("Aucune modification n'a été réalisée.")

		if len(errors) > 0:
			return False, errors
		
		else:
			# Mise à jour des données
			date == Lettre.date_envoie_lettre
			lieu == Lettre.lieu_ecriture_lettre
			objet == Lettre.objet_lettre 
			contresignataire == Lettre.contresignataire_lettre 
			langue == Lettre.langue_lettre 
			pronom == Lettre.pronom_personnel_employe_lettre 
			cote == Lettre.cote_lettre 
			statut == Lettre.statut_lettre 
			lien_lettre == Lettre.lien_image_lettre

		try:
			# On l'ajoute au transport vers la base de données
			db.session.add(miseajour_lettre)
			# On envoie le paquet
			db.session.commit()
			return True, miseajour_lettre

		except Exception as erreur:
			# On annule les requêtes de la transaction en cours en cas d'erreurs
			db.session.rollback()
			return False, [str(erreur)]

	@staticmethod
	def supprimer_lettre(id_lettre):
		"""
		Fonction qui supprime une lettre
		:param id_lettre: id de la lettre
		:type id_lettre: int
		:returns: Suppression des données ou refus en cas d'erreurs
		:rtype: Booléen
		"""

		# récupération d'une lettre dans la base de données
		id_lettre = Lettre.query.filter(Lettre.id_lettre)

		try:
			# suppression de la lettre de la base de données
			db.session.delete(id_lettre)
			db.session.commit()
			return True

		except Exception as erreur:
			# raise erreur
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
		:returns: Id de l'image numérisée
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