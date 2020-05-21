#Gestion des erreurs les plus courantes

from flask import render_template

from ..app import app

#En cas de page introuvable : 
@app.errorhandler(404)
def not_found(erreur):
    return render_template("pages/error/404.html"), 404

#En cas d'éléments supprimés :
@app.errorhandler(410)
def gone(erreur):
    return render_template("pages/error/410.html"), 410

#En cas d'une erreur de serveur interne :
@app.errorhandler(500)
def internal_server_error(erreur):
    return render_template("pages/error/500.html"), 500