from app.app import db, login, config_app
from app.modeles.utilisateurs import User
from unittest import TestCase

# pour lancer les tests, utilisation de Nose2 (à importer) qui permet de lancer des tests unitaires grâce à la commande 
# nose2 -v dans le terminal quand on est placé au niveau de l'app
# il faut également passer l'application en mode test, en indiquant dans le fichier app.py : def config_app(config_name="test") 
# et dans le fichier run.py : if __name__ == "__main__": app = config_app("test")

class TestUser(TestCase):
	def setUp(self):
	# méthode appelée avant l'exécution de chaque test
		self.app = config_app('test')
		# génération de l'application (mode test) en appelant la fonction config_app("test")
		self.db = db
		# génération de la BDD 
		self.client = self.app.test_client()
		# génération d'un client de test pour faire des requêtes
		self.db.create_all(app=self.app)

	def tearDown(self):
	# méthode appelée une fois le test terminé
		self.db.drop_all(app=self.app)

	def test_registration(self):
		"""test qui permet de tester l'inscription d'un·e utilisateur·rice """
		with self.app.app_context():
		# commande qui permet au code ci-dessous de s'executer en ayant accès à current_app (un proxy qui permet 
		# d'accéder à l'application sans avoir besoin de l'importer)
			status, user = User.creer("C8", "charles.valois@chartes.psl.eu", "Charles de Valois", "charlot98")
			# création d'un utilisateur test
			query = User.query.filter(User.user_email == "charles.valois@chartes.psl.eu").first()
			# on recherche cet utilisateur (ici par son email) afin de pouvoir ensuite tester les données rentrées
			# (on vérifie si elles ont bien été enregistrées)
		print(user, status)
		self.assertEqual(query.user_name, "Charles de Valois")
		# assertEqual vérifie que les deux paramètres sont égaux
		self.assertEqual(query.user_login, "C8")
		self.assertNotEqual(query.user_password, "charlot98")
		# on vérifie que le mot de passe entré n'est pas égal à celui dans la BDD (il doit être hasché)
		self.assertTrue(status)
		# on vérifie que les données ont bien été envoyées

	def test_invalid_registration(self):
		""" test qui permet de tester si l'application renvoie bien une erreur quand le mot de passe est trop court """
		with self.app.app_context():
			status, user = User.creer("C8", "charles.valois@chartes.psl.eu", "Charles de Valois", "charlot")
			query = User.query.filter(User.user_email == "charles.valois@chartes.psl.eu").first()
		self.assertGreaterEqual(len(query.user_password), 6)
		# on vérifie que le mot de passe comprend au moins 6 lettres
		self.assertFalse(status)
		# on vérifie qu'il y a bien une erreur, renvoyant ainsi False

	def test_registration_login(self):
		"""test qui permet de vérifier si un·e utilisateur·rice peut bien se connecter une fois qu'il/elle a créé un compte"""
		with self.app.app_context():
			status, create = User.creer("mesme", "jehan.mesme@chartes.psl.eu", "Jehan Mesme", "jeannot83")
			login = User.identification("mesme", "jeannot83")
		self.assertEqual(create, login)
		# on vérifie que les données enregistrées et celles rentrées pour se connecter sont bien les mêmes
		self.assertTrue(status)
		# on vérifie que les données sont bien envoyées
