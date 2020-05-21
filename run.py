#Fichier qui permet de lancer l'application Epistautograpy.
from app.app import app, init_db

#Lancement d'un serveur de test. On met une condition pour vérifier
#que ce fichier est celui qui est couramment exécuté. Cela permet
#d'éviter de lancer la fonction quand on importe ce fichier depuis
#une autre. Rajout d'une ligne d'appel pour créer la base de 
#données au lancement de l'application.
if __name__ == "__main__":
	init_db
	app.run(debug=True)