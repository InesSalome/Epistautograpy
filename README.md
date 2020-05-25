# Epistautograpy

Epistautograpy est une application web permettant de naviguer dans une collection de lettres de Charles VIII *via* des recherches simples ou à facette. Elle s'inscrit dans une étude sur le rôle du contreseing et de l'autographie dans les lettres de Charles VIII, mais aussi l'éclairage que le numérqiue peut apporter à ces analyses. Elle a été réalisée par Gwenaëlle Patat dans le cadre du Master 2 de l'École des Chartes "Technologies Numériques appliquées à l'Histoire", selon les consignes suivantes : 

>Au choix, en travail individuel:

>Les sujets (la matière source) seront à valider par mes soins d'ici le 1er décembre.

>* une application avec base de données relationnelle, comprenant formulaire pour ajout, suppression, édition. Il doit être possible de naviguer dans la collection, d'y faire une recherche simple voire complexe, un index peut être ajouté.

>* une application utilisant des fichiers TEI pour présenter le corpus, faisant usage de la librairie lxml ou équivalent pour proposer des index et des tables des matières. XSL peut être utilisé, mais doit l'être dynamiquement. L'usage de fichiers TEI disponibles dans d'autres projets, celui d'années précédentes est possible.

>* un ensemble de notebooks python permettant la récupération automatique de données, la visualisation de ces données suivant les critères choisis (ex: 1000 manuscrits de la BNF répartis par taille, période, etc.) et une analyse de ces données si elles sont textuelles. Pour ce sujet, il sera recommandé de suivre un cours en auditeur libre en master HN ou avec les AP2.

>* Une proposition originale reprenant ces schémas: exemple, une base de données mise à disposition via une API, avec des données collectées ailleurs (Exemple: API DTS de documents de wikisource).

>Le code sera noté en fonction:

>* de sa propreté;
>* de son fonctionnement;
>* de sa documentation (installation et fonctions);
>* de sa validité (la beauté du design ne sera pas prise en compte);
>* de son architecture;
>* et bien sûr des consignes.

>Des points bonus seront accordés si:

>des tests sont proposés, validant le fonctionnement de l'application ou de l'analyse.

>Le devoir sera à rendre sous la forme d'un repository git, dont la gouvernance sera transférée, en fin de devoir, à l'organisation TNAH-Chartes. Tout retard équivaudra à 2 points en moins par jour.


## Description des fonctionnalités de l'application

Epistautograpy permet de consulter des lettres de Charles VIII grâce à des recherches simples ou avancées. Les filtres ont été pensés pour pouvoir mieux visualiser quelles lettres ont été contresignées par quel secrétaire, mais aussi quel destinataire est le plus sollicité, à quelle date, etc. L'application propose donc l'accès à :

* un index des dates d'envoie des lettres
* un index des destinataires
* un index des contresignataires
* un index des institutions de conservation
* bien évidemment, un index des lettres recensées

Il est aussi possible pour les utilisateurs de s'inscrire et de participer à l'enrichissement des lettres répertoriées en remplissant un formulaire, en modifiant des données ou en en supprimant. 

__Développement du projet__

  Ce projet a été développé grâce au langage de programmation python3 et au framework d'application web Flask. Il s’appuie sur une base de données réalisée avec les logiciels MySQLWorkbench et DB Browser for SQLite. Le graphisme de l’application a été réalisé grâce à Bootstrap.


## Comment lancer Epistautograpy ?

* Installer Python3
* Cloner ce dépôt Git : git clone https://github.com/InesSalome/Epistautograpy.git; rentrer dedans
* Installer, configurer et lancer un environnement virtuel avec Python3 : virtualenv -p python3 env pour l'installation, source env/bin/activate pour le lancement
* Installer les requirements.txt : pip install -r requirements.txt
* Lancer l'application avec la commande python3 run.py
