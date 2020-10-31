#Import de fonctions pour sécuriser la création de comptes.
from werkzeug.security import generate_password_hash, check_password_hash
#Configuration pour tester si l'utilisateur est connecté, actif ou anonyme.
from flask_login import UserMixin

from .. app import db, login

#Méthode pour mettre à jour la base de données
from sqlalchemy import update

class User(UserMixin, db.Model):
	__tablename__ = "user"
	id_user = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	nom_user = db.Column(db.Text, nullable=False)
	login_user = db.Column(db.String(45), nullable=False)
	email_user = db.Column(db.Text, nullable=False)
	password_user = db.Column(db.String(64), nullable=False)
	authorships = db.relationship("Authorship", back_populates="user")

	# Fonction qui retourne un utilisateur selon l'id donné.
	def get_id(self):
		"""
		Retourne l'id de l'objet actuellement utilisé
		:returns: ID de l'utilisateur
		:rtype: int
		"""
		return self.id_user

	#Méthode static pour appeler et enregistrer la fonction sous la responsabilité de la classe User
	@staticmethod
	#Fonction pour vérifier la validité de l'identification de l'utilisateur
	def identification(login, motdepasse):
		"""
		Identification d'un.e utilisateur.trice 
		:param login: Login de l'utilisateur
		:type login: str
		:param motdepasse: Mot de passe envoyé par l'utilisateur
		:type motdepasse: str
		:returns: Si réussite, données de l'utilisateur ; si échec, None
		:rtype: Booléen
		"""
		utilisateur = User.query.filter(User.login_user == login).first()
		if utilisateur and check_password_hash(utilisateur.password_user, motdepasse):
			return utilisateur
		return None

	@staticmethod
	def creer(login, email, nom, motdepasse):
		"""
		Création d'un compte utilisateur.rice
		:param login: Login de l'utilisateur-rice
		:type login: str
		:param email: Email de l'utilisateur-rice
		:type email: str
		:param nom: Nom de l'utilisateur-rice
		:type nom: str
		:param motdepasse: Mot de passe de l'utilisateur-rice (Minimum 6 caractères)
		:type motdepasse: str
		:returns: création d'un compte
		:rtype: Booléen
		"""
		erreurs = []
		if not login:
			erreurs.append("Le login fourni est vide")
		if not email:
			erreurs.append("L'email fourni est vide")
		if not nom:
			erreurs.append("Le nom fourni est vide")
		if not motdepasse or len(motdepasse) < 6:
			erreurs.append("Le mot de passe fourni est vide ou trop court")

		# On vérifie que personne n'a utilisé cet email ou ce login
		uniques = User.query.filter(
			db.or_(User.email_user == email, User.login_user == login)
		).count()
		if uniques > 0:
			erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")

		# Si on a au moins une erreur
		if len(erreurs) > 0:
			return False, erreurs

		# On crée un utilisateur
		utilisateur = User(
			nom_user=nom,
			login_user=login,
			email_user=email,
			password_user=generate_password_hash(motdepasse)
		)

		try:
			# On l'ajoute au transport vers la base de données
			db.session.add(utilisateur)
			# On envoie le paquet
			db.session.commit()

			# On renvoie l'utilisateur
			return True, utilisateur

		except Exception as erreur:
			return False, [str(erreur)]


#Fonction pour récupérer un utilisateur selon son identifiant
@staticmethod
@login.user_loader
def trouver_utilisateur_via_id(id_user):
	"""
	Permet de récupérer un·e utilisateur·rice en fonction de son identifiant
	:return: ID de l'utilisateur·rice
	:rtype: int
	"""
	return User.query.get(int(id_user))
