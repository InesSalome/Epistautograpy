#Fichier qui permet d'utiliser ce qui est dans l'application Epistautograpy.
from app.app import app
#Lancement d'un serveur de test. On met une condition pour vérifier
#que ce fichier est celui qui est couramment exécuté. Cela permet
#d'éviter de lancer la fonction quand on importe ce fichier depuis
#une autre. 
if __name__ == "__main__":
    app.run(debug=True)