#Génération du chemin actuel de l'application

#Module pour intéragir avec le système d'exploitation sur lequel Python est activé
import os

#Récupération du nom de dossier qui comprend le fichier avec ce code, et récupération du chemin absolu de ce fichier 
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
print(chemin_actuel)

templates = os.path.join(chemin_actuel, "app", "templates")
print(templates)